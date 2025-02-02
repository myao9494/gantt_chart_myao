gantt.config.undo = true;
gantt.config.undo_steps = 10;

var undoStack = [];
var redoStack = [];

gantt.attachEvent("onAfterTaskAdd", function(id, task) {
    undoStack.push({
        type: "add",
        task: gantt.copy(task)
    });
    redoStack = [];
    return true;
});

gantt.attachEvent("onAfterTaskUpdate", function(id, task) {
    var oldTask = gantt.getTask(id);
    undoStack.push({
        type: "update",
        task: gantt.copy(task),
        oldTask: gantt.copy(oldTask)
    });
    redoStack = [];
    return true;
});

gantt.attachEvent("onAfterTaskDelete", function(id, task) {
    undoStack.push({
        type: "delete",
        task: gantt.copy(task)
    });
    redoStack = [];
    return true;
});

gantt.undo = function() {
    var action = undoStack.pop();
    if (!action) return;

    redoStack.push(action);

    switch(action.type) {
        case "add":
            gantt.deleteTask(action.task.id);
            break;
        case "update":
            gantt.updateTask(action.task.id, action.oldTask);
            break;
        case "delete":
            gantt.addTask(action.task);
            break;
    }
};

gantt.redo = function() {
    var action = redoStack.pop();
    if (!action) return;

    undoStack.push(action);

    switch(action.type) {
        case "add":
            gantt.addTask(action.task);
            break;
        case "update":
            gantt.updateTask(action.task.id, action.task);
            break;
        case "delete":
            gantt.deleteTask(action.task.id);
            break;
    }
};
