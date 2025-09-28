var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');
var fs = require('fs').promises;
var Promise = require('bluebird');
require("date-format-lite");

var port = 1337;
var app = express();
var mysql = require('mysql2/promise');

var cookieSession = require("cookie-session");
app.set('trust proxy', 1)
app.use(
	cookieSession({
		name: "__session",
		keys: ["key1"],
		maxAge: 24 * 60 * 60 * 100,
		secure: true,
		httpOnly: true,
		sameSite: 'none'
	})
);

// var sqlite3 = require('sqlite3');
// let db_3 = new sqlite3.Database('gantt_howto_node.db', sqlite3.OPEN_READWRITE, (err) => 
// { if (err) { console.error(err.message); } console.log('Connected to the ocs_athlete database.'); }); 

var db = mysql.createPool({
	host: '127.0.0.1',
	port: 3306,
	user: 'root',
	password: '',
	database: 'gantt_howto_node',
	waitForConnections: true,
	connectionLimit: 10,
	queueLimit: 0
});

// momentの依存関係を条件付きで読み込む
let moment;
try {
    moment = require('moment-timezone');
} catch (e) {
    // moment-timezoneが利用できない場合は、基本的なDate操作を行う関数を定義
    moment = function(date) {
        return {
            tz: function() {
                return this;
            },
            format: function(format) {
                if (!date) return '';
                const d = new Date(date);
                if (format === "YYYY-MM-DD") {
                    return d.toISOString().split('T')[0];
                }
                return d.toISOString();
            },
            clone: function() {
                return moment(date);
            },
            add: function(number, unit) {
                const d = new Date(date);
                if (unit === 'days') {
                    d.setDate(d.getDate() + number);
                }
                return moment(d);
            }
        };
    };
}

app.use(express.static(path.join(__dirname, "public")));
app.use(bodyParser.urlencoded({extended: true}));

const CSV_TASK_COLUMNS = [
    "id",
    "text",
    "start_date",
    "end_date",
    "duration",
    "progress",
    "parent",
    "kind_task",
    "ToDo",
    "task_schedule",
    "folder",
    "url_adress",
    "mail",
    "memo",
    "hyperlink",
    "color",
    "textColor",
    "owner_id",
    "sortorder",
    "edit_date"
];

const CSV_LINK_COLUMNS = ["id", "source", "target", "type"];
const BACKUP_DIR = path.join(__dirname, 'backup');
const DATA_IMPORT_DIR = path.join(__dirname, 'データ読み込み');

async function saveCsvBackup(fileName, content) {
	try {
		await fs.mkdir(BACKUP_DIR, { recursive: true });
		await fs.writeFile(path.join(BACKUP_DIR, fileName), content, 'utf8');
	} catch (error) {
		console.error(`Failed to save CSV backup ${fileName}:`, error);
	}
}

class ImportError extends Error {
	constructor(message, status, responseBody) {
		super(message);
		this.name = 'ImportError';
		this.status = status || 400;
		this.responseBody = responseBody || { error: message };
	}
}

function handleImportError(res, error, fallbackMessage) {
	if (error instanceof ImportError) {
		const body = error.responseBody || { error: error.message };
		if (!body.error) {
			body.error = error.message;
		}
		res.status(error.status || 400).json(body);
		return;
	}
	res.status(500).json({ error: fallbackMessage, details: error && error.message ? error.message : undefined });
}

app.listen(port, function () {
	console.log("Server is running on port " + port + "...");
});

app.get("/data", async function (req, res) {
	try {
		const [tasks] = await db.query("SELECT * FROM gantt_tasks ORDER BY sortorder ASC");
		const [links] = await db.query("SELECT * FROM gantt_links");

		for (var i = 0; i < tasks.length; i++) {
			// start_dateをMomentオブジェクトに変換（タイムゾーンの変更なし）
			tasks[i].start_date = moment(tasks[i].start_date);

			// progressが1でない場合は、durationを使ってend_dateを計算
			if (tasks[i].progress != 1) {
				tasks[i].end_date = tasks[i].start_date.clone().add(tasks[i].duration, 'days');
			} else if (tasks[i].end_date) {
				// progressが1で、end_dateが設定されている場合は、そのend_dateを使用
				tasks[i].end_date = moment(tasks[i].end_date);
			} else {
				// progressが1で、end_dateが設定されていない場合は、start_dateと同じにする
				tasks[i].end_date = tasks[i].start_date.clone();
			}

			// start_dateとend_dateをISO 8601形式の文字列に変換
			tasks[i].start_date = tasks[i].start_date.format();
			tasks[i].end_date = tasks[i].end_date.format();

			// durationを数値に変換
			tasks[i].duration = parseInt(tasks[i].duration, 10);
			tasks[i].open = true;

			// console.log(`Task ID: ${tasks[i].id}, Start Date: ${tasks[i].start_date}, Duration: ${tasks[i].duration}, Progress: ${tasks[i].progress}, End Date: ${tasks[i].end_date}`);
		}

		// end_dateの値をログに出力
		// console.log("Tasks with end_date:", tasks.map(task => ({ id: task.id, end_date: task.end_date })));

		res.send({
			data: tasks,
			collections: {links: links}
		});

	} catch (error) {
		sendResponse(res, "error", null, error);
	}
});


app.get("/data/export/tasks.csv", async function (req, res) {
	try {
		const [tasks] = await db.query("SELECT * FROM gantt_tasks ORDER BY sortorder ASC");
		const csvRows = tasks.map((task) => {
			return CSV_TASK_COLUMNS.map((column) => formatForCsv(task[column]));
		});
		const csv = buildCsv(CSV_TASK_COLUMNS, csvRows);
		const timestamp = moment(new Date()).tz('Asia/Tokyo').format('YYYYMMDD_HHmmss');
		const filename = `gantt_tasks_${timestamp}.csv`;
		const csvWithBom = '\uFEFF' + csv;
		await saveCsvBackup(filename, csvWithBom);
		res.setHeader('Content-Type', 'text/csv; charset=utf-8');
		res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
		res.send(csvWithBom);
	} catch (error) {
		res.status(500).json({ error: 'CSV export failed', details: error.message });
	}
});

app.get("/data/export/links.csv", async function (req, res) {
	try {
		const [links] = await db.query("SELECT * FROM gantt_links ORDER BY id ASC");
		const csvRows = links.map((link) => {
			return CSV_LINK_COLUMNS.map((column) => formatForCsv(link[column]));
		});
		const csv = buildCsv(CSV_LINK_COLUMNS, csvRows);
		const timestamp = moment(new Date()).tz('Asia/Tokyo').format('YYYYMMDD_HHmmss');
		const filename = `gantt_links_${timestamp}.csv`;
		const csvWithBom = '\uFEFF' + csv;
		await saveCsvBackup(filename, csvWithBom);
		res.setHeader('Content-Type', 'text/csv; charset=utf-8');
		res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
		res.send(csvWithBom);
	} catch (error) {
		res.status(500).json({ error: 'CSV export failed', details: error.message });
	}
});


async function createDatabaseBackup() {
	const timestamp = moment(new Date()).tz('Asia/Tokyo').format('YYYYMMDD_HHmmss');
	const [tasks] = await db.query("SELECT * FROM gantt_tasks ORDER BY sortorder ASC");
	const taskRows = tasks.map((task) => {
		return CSV_TASK_COLUMNS.map((column) => formatForCsv(task[column]));
	});
	const taskCsv = '\uFEFF' + buildCsv(CSV_TASK_COLUMNS, taskRows);
	const taskFilename = `gantt_tasks_${timestamp}.csv`;
	await saveCsvBackup(taskFilename, taskCsv);

	const [links] = await db.query("SELECT * FROM gantt_links ORDER BY id ASC");
	const linkRows = links.map((link) => {
		return CSV_LINK_COLUMNS.map((column) => formatForCsv(link[column]));
	});
	const linkCsv = '\uFEFF' + buildCsv(CSV_LINK_COLUMNS, linkRows);
	const linkFilename = `gantt_links_${timestamp}.csv`;
	await saveCsvBackup(linkFilename, linkCsv);

	return {
		timestamp: timestamp,
		taskFilename: taskFilename,
		linkFilename: linkFilename
	};
}

app.post("/data/backup", async function (req, res) {
	try {
		const files = await createDatabaseBackup();
		res.json({ status: 'ok', files: files });
	} catch (error) {
		res.status(500).json({ error: 'Database backup failed', details: error.message });
	}
});

app.post("/data/import/tasks.csv", express.text({ type: ["text/csv", "text/plain", "application/vnd.ms-excel"] }), async function (req, res) {
	try {
		const result = await importTasksFromCsvText(req.body);
		res.json({ status: 'ok', inserted: result.inserted });
	} catch (error) {
		handleImportError(res, error, 'CSV import failed');
	}
});

app.post("/data/import/links.csv", express.text({ type: ["text/csv", "text/plain", "application/vnd.ms-excel"] }), async function (req, res) {
	try {
		const result = await importLinksFromCsvText(req.body);
		res.json({ status: 'ok', inserted: result.inserted });
	} catch (error) {
		handleImportError(res, error, 'CSV import failed');
	}
});

app.post("/data/import/directory", async function (req, res) {
	try {
		const summary = await importCsvFromDirectory();
		res.json({ status: 'ok', summary: summary });
	} catch (error) {
		handleImportError(res, error, 'ディレクトリからのデータ読み込みに失敗しました');
	}
});


// add new task
app.post("/data/task", async function (req, res) { // adds new task to database
	var task = getTask(req.body);

	try {
		const [orderRows] = await db.query("SELECT MAX(sortorder) AS maxOrder FROM gantt_tasks");
		const maxOrder = Array.isArray(orderRows) && orderRows.length && orderRows[0].maxOrder != null
			? Number(orderRows[0].maxOrder)
			: 0;
		const orderIndex = maxOrder + 1;

		const [insertResult] = await db.query("INSERT INTO gantt_tasks(text, start_date, duration, progress, parent,kind_task,ToDo,task_schedule,folder,url_adress,mail,memo,hyperlink,color,textColor,owner_id,sortorder,edit_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
			[task.text, task.start_date, task.duration, task.progress, task.parent,task.kind_task,task.ToDo,task.task_schedule,task.folder,task.url_adress,task.mail,task.memo,task.hyperlink,task.color,task.textColor,task.owner_id, orderIndex,task.edit_date]);

		sendResponse(res, "inserted", insertResult && insertResult.insertId, null, req.body.id);
	} catch (error) {
		sendResponse(res, "error", null, error);
	}
});

// update task
app.put("/data/task/:id", async function (req, res) {
	var sid = req.params.id,
		target = req.body.target,
		task = getTask(req.body);

	var endDate = task.progress == 1 ? formatDateForMySQL(moment().add(1, 'days')) : task.end_date;

	try {
		await db.query("UPDATE gantt_tasks SET text = ?, start_date = ?,end_date = ?, duration = ?, progress = ?, parent = ?, kind_task = ?, ToDo = ?, task_schedule = ? ,folder = ?, url_adress = ?, mail = ?, memo = ?, hyperlink = ?, color = ?, textColor = ?, owner_id = ? , edit_date = ? WHERE id = ?",
			[task.text, task.start_date, endDate ,task.duration, task.progress, task.parent,task.kind_task,task.ToDo,task.task_schedule,task.folder,task.url_adress,task.mail,task.memo,task.hyperlink,task.color,task.textColor,task.owner_id,task.edit_date, sid]);

		await updateOrder(sid, target);

		sendResponse(res, "updated");
	} catch (error) {
		sendResponse(res, "error", null, error);
	}
});

async function updateOrder(taskId, target) {
	var nextTask = false;
	var targetId = target || "";

	if (!targetId)
		return;

	if (targetId.startsWith("next:")) {
		targetId = targetId.substr("next:".length);
		nextTask = true;
	}

	if (!targetId)
		return;

	const [rows] = await db.query("SELECT sortorder FROM gantt_tasks WHERE id = ?", [targetId]);
	if (!Array.isArray(rows) || !rows.length)
		return;

	var targetOrder = rows[0].sortorder != null ? Number(rows[0].sortorder) : 0;
	if (nextTask)
		targetOrder++;

	await db.query("UPDATE gantt_tasks SET sortorder = sortorder + 1 WHERE sortorder >= ? AND id <> ?",
		[targetOrder, taskId]);
	await db.query("UPDATE gantt_tasks SET sortorder = ? WHERE id = ?", [targetOrder, taskId]);
}

// delete task
app.delete("/data/task/:id", function (req, res) {
	var sid = req.params.id;
	db.query("DELETE FROM gantt_tasks WHERE id = ?", [sid])
		.then(function (result) {
			sendResponse(res, "deleted");
		})
		.catch(function (error) {
			sendResponse(res, "error", null, error);
		});
});

// add link
app.post("/data/link", function (req, res) {
	var link = getLink(req.body);

	db.query("INSERT INTO gantt_links(source, target, type) VALUES (?,?,?)",
		[link.source, link.target, link.type])
		.then(function (result) {
			sendResponse(res, "inserted", result.insertId, null, req.body.id);
		})
		.catch(function (error) {
			sendResponse(res, "error", null, error);
		});
});

// update link
app.put("/data/link/:id", function (req, res) {
	var sid = req.params.id,
		link = getLink(req.body);

	db.query("UPDATE gantt_links SET source = ?, target = ?, type = ? WHERE id = ?",
		[link.source, link.target, link.type, sid])
		.then(function (result) {
			sendResponse(res, "updated");
		})
		.catch(function (error) {
			sendResponse(res, "error", null, error);
		});
});

// delete link
app.delete("/data/link/:id", function (req, res) {
	var sid = req.params.id;
	db.query("DELETE FROM gantt_links WHERE id = ?",
		[sid])
		.then(function (result) {
			sendResponse(res, "deleted");
		})
		.catch(function (error) {
			sendResponse(res, "error", null, error);
		});
});


function supportsMomentValidation() {
	try {
		if (!moment || typeof moment !== 'function') {
			return false;
		}
		const probe = moment(new Date());
		return probe && typeof probe.isValid === 'function';
	} catch (err) {
		return false;
	}
}

const momentHasValidation = supportsMomentValidation();

function formatForCsv(value) {
	if (value === null || value === undefined) {
		return '';
	}
	if (value instanceof Date) {
		return formatDateForMySQL(value);
	}
	if (typeof value === 'string') {
		return value;
	}
	if (typeof value === 'number' && !Number.isFinite(value)) {
		return '';
	}
	return String(value);
}

function escapeCsvValue(value) {
	const text = value === null || value === undefined ? '' : value;
	if (typeof text !== 'string') {
		return escapeCsvValue(String(text));
	}
	if (text === '') {
		return '';
	}
	const needsQuotes = text.includes(',') || text.includes('\n') || text.includes('\r') || text.includes('"');
	if (!needsQuotes) {
		return text;
	}
	return '"' + text.replace(/"/g, '""') + '"';
}

function buildCsv(headerColumns, rows) {
	const headerLine = headerColumns.map(escapeCsvValue).join(',');
	const bodyLines = rows.map((row) => row.map(escapeCsvValue).join(','));
	return [headerLine].concat(bodyLines).join('\r\n');
}

async function importTasksFromCsvText(input) {
	const csvText = (input || '').trim();
	if (!csvText) {
		throw new ImportError('CSV data is empty', 400, { error: 'CSV data is empty' });
	}
	const rows = parseCsv(csvText);
	if (!Array.isArray(rows) || !rows.length) {
		throw new ImportError('CSV data is empty', 400, { error: 'CSV data is empty' });
	}
	const header = rows[0];
	if (!isExpectedHeader(header, CSV_TASK_COLUMNS)) {
		throw new ImportError('CSV header does not match expected format', 400, {
			error: 'CSV header does not match expected format',
			expected: CSV_TASK_COLUMNS
		});
	}
	const contentRows = rows.slice(1).filter((row) => Array.isArray(row) && row.some((cell) => (cell || '').trim() !== ''));
	const normalizedRows = contentRows.map((row) => normalizeTaskRow(row));
	const connection = await db.getConnection();
	try {
		await connection.beginTransaction();
		await connection.query('DELETE FROM gantt_tasks');
		if (normalizedRows.length) {
			await connection.query('ALTER TABLE gantt_tasks AUTO_INCREMENT = 1');
			await connection.query(
				'INSERT INTO gantt_tasks (id, text, start_date, end_date, duration, progress, parent, kind_task, ToDo, task_schedule, folder, url_adress, mail, memo, hyperlink, color, textColor, owner_id, sortorder, edit_date) VALUES ?'
				, [normalizedRows]
			);
			const [autoRows] = await connection.query('SELECT COALESCE(MAX(id), 0) + 1 AS nextId FROM gantt_tasks');
			const nextId = Array.isArray(autoRows) && autoRows.length ? autoRows[0].nextId : 1;
			await connection.query('ALTER TABLE gantt_tasks AUTO_INCREMENT = ?', [nextId]);
		}
		await connection.commit();
		return { inserted: normalizedRows.length };
	} catch (dbError) {
		await connection.rollback();
		throw dbError;
	} finally {
		connection.release();
	}
}

async function importLinksFromCsvText(input) {
	const csvText = (input || '').trim();
	if (!csvText) {
		throw new ImportError('CSV data is empty', 400, { error: 'CSV data is empty' });
	}
	const rows = parseCsv(csvText);
	if (!Array.isArray(rows) || !rows.length) {
		throw new ImportError('CSV data is empty', 400, { error: 'CSV data is empty' });
	}
	const header = rows[0];
	if (!isExpectedHeader(header, CSV_LINK_COLUMNS)) {
		throw new ImportError('CSV header does not match expected format', 400, {
			error: 'CSV header does not match expected format',
			expected: CSV_LINK_COLUMNS
		});
	}
	const contentRows = rows.slice(1).filter((row) => Array.isArray(row) && row.some((cell) => (cell || '').trim() !== ''));
	const normalizedRows = contentRows.map((row) => normalizeLinkRow(row));
	const connection = await db.getConnection();
	try {
		await connection.beginTransaction();
		await connection.query('DELETE FROM gantt_links');
		if (normalizedRows.length) {
			await connection.query('ALTER TABLE gantt_links AUTO_INCREMENT = 1');
			await connection.query(
				'INSERT INTO gantt_links (id, source, target, type) VALUES ?'
				, [normalizedRows]
			);
			const [autoRows] = await connection.query('SELECT COALESCE(MAX(id), 0) + 1 AS nextId FROM gantt_links');
			const nextId = Array.isArray(autoRows) && autoRows.length ? autoRows[0].nextId : 1;
			await connection.query('ALTER TABLE gantt_links AUTO_INCREMENT = ?', [nextId]);
		}
		await connection.commit();
		return { inserted: normalizedRows.length };
	} catch (dbError) {
		await connection.rollback();
		throw dbError;
	} finally {
		connection.release();
	}
}

async function importCsvFromDirectory() {
	await fs.mkdir(DATA_IMPORT_DIR, { recursive: true });
	const entries = await fs.readdir(DATA_IMPORT_DIR, { withFileTypes: true });
	const csvEntries = entries.filter((entry) => entry.isFile() && /\.csv$/i.test(entry.name));
	if (!csvEntries.length) {
		throw new ImportError('データ読み込みフォルダにCSVファイルがありません。', 404, {
			error: 'データ読み込みフォルダにCSVファイルがありません。'
		});
	}
	const files = [];
	for (const entry of csvEntries) {
		const filePath = path.join(DATA_IMPORT_DIR, entry.name);
		const content = await fs.readFile(filePath, 'utf8');
		const stats = await fs.stat(filePath);
		files.push({
			name: entry.name,
			path: filePath,
			content: content,
			type: detectCsvType(content),
			mtimeMs: stats.mtimeMs
		});
	}
	const selectLatestByType = (type) => {
		return files
			.filter((file) => file.type === type)
			.sort((a, b) => b.mtimeMs - a.mtimeMs)[0] || null;
	};
	const taskFile = selectLatestByType('tasks');
	if (!taskFile) {
		throw new ImportError('タスク用のCSVが見つかりません。', 404, {
			error: 'データ読み込みフォルダにタスクCSVが見つかりません。'
		});
	}
	const linkFile = selectLatestByType('links');
	const ignoredFiles = files.filter((file) => file.type === null).map((file) => file.name);
	const taskResult = await importTasksFromCsvText(taskFile.content);
	let linkResult = null;
	let skippedLinks = false;
	if (linkFile) {
		linkResult = await importLinksFromCsvText(linkFile.content);
	} else {
		skippedLinks = true;
	}
	return {
		directory: DATA_IMPORT_DIR,
		taskFile: taskFile.name,
		tasksInserted: taskResult.inserted,
		linkFile: linkFile ? linkFile.name : null,
		linksInserted: linkResult ? linkResult.inserted : 0,
		skippedLinks: skippedLinks,
		ignoredFiles: ignoredFiles
	};
}

function detectCsvType(csvContent) {
	const text = (csvContent || '').trim();
	if (!text) {
		return null;
	}
	const rows = parseCsv(text);
	if (!Array.isArray(rows) || !rows.length) {
		return null;
	}
	const header = rows[0];
	if (isExpectedHeader(header, CSV_TASK_COLUMNS)) {
		return 'tasks';
	}
	if (isExpectedHeader(header, CSV_LINK_COLUMNS)) {
		return 'links';
	}
	return null;
}

function parseCsv(text) {
	const result = [];
	let row = [];
	let field = '';
	let inQuotes = false;
	let i = 0;
	const input = text.replace(/^\uFEFF/, '');
	while (i < input.length) {
		const char = input[i];
		if (inQuotes) {
			if (char === '"') {
				if (i + 1 < input.length && input[i + 1] === '"') {
					field += '"';
					i++;
				} else {
					inQuotes = false;
				}
			} else {
				field += char;
			}
		} else if (char === '"') {
			inQuotes = true;
		} else if (char === ',') {
			row.push(field);
			field = '';
		} else if (char === '\r') {
			// skip, handle on \n
		} else if (char === '\n') {
			row.push(field);
			result.push(row);
			row = [];
			field = '';
		} else {
			field += char;
		}
		i++;
	}
	row.push(field);
	result.push(row);
	return result;
}

function isExpectedHeader(inputHeader, expectedHeader) {
	if (!Array.isArray(inputHeader) || inputHeader.length !== expectedHeader.length) {
		return false;
	}
	for (let i = 0; i < expectedHeader.length; i++) {
		if ((inputHeader[i] || '').trim() !== expectedHeader[i]) {
			return false;
		}
	}
	return true;
}

function normalizeTaskRow(row) {
	const mapped = {};
	CSV_TASK_COLUMNS.forEach((column, index) => {
		mapped[column] = row[index] !== undefined ? row[index].trim() : '';
	});

	return [
		parseIntegerOrNull(mapped.id),
		emptyToNull(mapped.text),
		parseDateTime(mapped.start_date),
		parseDateTime(mapped.end_date),
		parseIntegerWithDefault(mapped.duration, 1),
		parseFloatWithDefault(mapped.progress, 0),
		parseIntegerOrNull(mapped.parent),
		emptyToNull(mapped.kind_task),
		emptyToNull(mapped.ToDo),
		emptyToNull(mapped.task_schedule),
		emptyToNull(mapped.folder),
		emptyToNull(mapped.url_adress),
		emptyToNull(mapped.mail),
		emptyToNull(mapped.memo),
		emptyToNull(mapped.hyperlink),
		emptyToNull(mapped.color),
		emptyToNull(mapped.textColor),
		parseIntegerOrNull(mapped.owner_id),
		parseIntegerOrNull(mapped.sortorder),
		emptyToNull(mapped.edit_date)
	];
}

function normalizeLinkRow(row) {
	return [
		parseIntegerOrNull(row[0] !== undefined ? row[0].trim() : ''),
		parseIntegerOrNull(row[1] !== undefined ? row[1].trim() : ''),
		parseIntegerOrNull(row[2] !== undefined ? row[2].trim() : ''),
		emptyToNull(row[3] !== undefined ? row[3].trim() : '')
	];
}

function emptyToNull(value) {
	return value === undefined || value === null || value === '' ? null : value;
}

function parseIntegerOrNull(value) {
	if (value === undefined || value === null || value === '') {
		return null;
	}
	const number = Number(value);
	return Number.isNaN(number) ? null : Math.trunc(number);
}

function parseIntegerWithDefault(value, defaultValue) {
	const parsed = parseIntegerOrNull(value);
	return parsed === null ? defaultValue : parsed;
}

function parseFloatWithDefault(value, defaultValue) {
	if (value === undefined || value === null || value === '') {
		return defaultValue;
	}
	const number = Number(value);
	return Number.isNaN(number) ? defaultValue : number;
}

function parseDateTime(value) {
	const trimmed = (value || '').trim();
	if (!trimmed) {
		return null;
	}
	if (momentHasValidation) {
		try {
			const formats = ['YYYY-MM-DD HH:mm:ss', 'YYYY/MM/DD HH:mm:ss', 'YYYY-MM-DD', 'YYYY/MM/DD'];
			for (const format of formats) {
				const candidate = moment(trimmed, format, true);
				if (candidate && typeof candidate.isValid === 'function' && candidate.isValid()) {
					if (typeof candidate.tz === 'function') {
						return candidate.tz('Asia/Tokyo').format('YYYY-MM-DD HH:mm:ss');
					}
					return candidate.format('YYYY-MM-DD HH:mm:ss');
				}
			}
			const isoCandidate = moment(trimmed);
			if (isoCandidate && typeof isoCandidate.isValid === 'function' && isoCandidate.isValid()) {
				if (typeof isoCandidate.tz === 'function') {
					return isoCandidate.tz('Asia/Tokyo').format('YYYY-MM-DD HH:mm:ss');
				}
				return isoCandidate.format('YYYY-MM-DD HH:mm:ss');
			}
		} catch (err) {
			// ignore moment parsing errors and fall back to native Date
		}
	}
	const nativeDate = new Date(trimmed);
	if (!Number.isNaN(nativeDate.getTime())) {
		return formatDateForMySQL(nativeDate);
	}
	return trimmed;
}


function getTask(data) {
    return {
        text: data.text,
        start_date: moment(data.start_date).tz('Asia/Tokyo').format("YYYY-MM-DD"),
        end_date: data.end_date ? moment(data.end_date).tz('Asia/Tokyo').format("YYYY-MM-DD") : null,
        duration: data.duration,
        progress: data.progress || 0,
        parent: data.parent === '' ? null : data.parent,
        kind_task: data.kind_task,
        ToDo: data.ToDo,
        task_schedule: data.task_schedule,
        folder: data.folder,
        url_adress: data.url_adress,
        mail: data.mail,
        memo: data.memo,
        hyperlink: data.hyperlink,
        color: data.color,
        textColor: data.textColor,
        owner_id: data.owner_id === '' ? 0 : data.owner_id, // 空の場合は0を設定
        edit_date: data.edit_date
    };
}

function getLink(data) {
	return {
		source: data.source,
		target: data.target,
		type: data.type
	};
}

function sendResponse(res, action, tid, error, sid) {

	if (action == "error")
		console.log(error);

	var result = {
		action: action
	};
	if (tid !== undefined && tid !== null) {
		result.tid = tid;
		result.id = tid;
	}
	if (sid !== undefined && sid !== null)
		result.sid = sid;

	res.send(result);
}

// 日付をMySQLの形式に変換する関数を修正
function formatDateForMySQL(date) {
    return moment(date).tz('Asia/Tokyo').format('YYYY-MM-DD HH:mm:ss');
}
