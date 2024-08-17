# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
from sqlalchemy import create_engine
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DATETIME
from sqlalchemy.dialects.mysql import insert
import pandas as pd
# import utility
import sys
from bs4 import BeautifulSoup
import re
from datetime import datetime,timedelta

sys.path.append("../mylib")


# -

class db_con(object):
    '''
    pythonからmysqlのDBへアクセスする
    '''

    def __init__(self):
        pd.set_option("display.max_colwidth", 10000)
        pd.set_option('display.max_rows', 500)
        self.user = "root"
        self.password = ""
        self.host = "localhost"
        self.port = 3306
        self.database_1 = "gantt_howto_node"
        self.url_1 = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_1}?charset=utf8'
        self.engine_1 = create_engine(self.url_1, echo=False)

    def create_db(self):
        query = "select * from gantt_tasks"
        self.df = pd.read_sql(query, con=self.engine_1)
        return self.df

    def move_task(self, taisho_start, nobasu_day):
        #         if not hasattr(self,"df"):
        self.create_db()
        df_taisho = self.df.copy()
        df_taisho = df_taisho[df_taisho["start_date"] == taisho_start]
        df_taisho = df_taisho[df_taisho["progress"] < 1]
        df_taisho["start_date"] = df_taisho["start_date"] + \
            pd.Timedelta(days=nobasu_day)
        out = self.to_db(df_taisho, "start_date")
        print(out)
        # 文字列から日付オブジェクトに変換
        taisho_start_date = datetime.strptime(taisho_start, "%Y-%m-%d")
        # 日数を加算
        extended_date = taisho_start_date + timedelta(days=nobasu_day)
        # 結果を表示
        print(extended_date.strftime("%Y-%m-%d"))

    def to_db(self, df_taisho, retu_mei):
        if len(df_taisho) != 0:
            metadata_1 = MetaData()
            metadata_1.bind = self.engine_1
            menus = Table(
                'gantt_tasks', metadata_1,
                Column('id', Integer, primary_key=True),
                Column(retu_mei, DATETIME),
            )

            conn = self.engine_1.connect()

            for index in range(len(df_taisho)):
                rec = df_taisho.iloc[index:index +
                                     1][["id", retu_mei]].to_dict("records")
                insert_stmt = insert(menus).values(rec)
                # on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
                #     start_date=insert_stmt.inserted.start_date
                # )
                command = f"conn.execute(insert_stmt.on_duplicate_key_update({retu_mei}=insert_stmt.inserted.{retu_mei}))"
                exec(command)
#                 print(index,rec)
            conn.close()
            out = f"{len(df_taisho)}件処理しました"
        else:
            out = "０件でした"
        return out


if __name__ == "__main__":
    try:
        get_ipython
        print("ss")
        obj = db_con()
        taisho_start = "2024-2-19"
        nobasu_day = 7
    except NameError:
        print("このコードはJupyter Notebook外で実行されています。")

# # factory

# +


def read_from_db(db_config: dict) -> pd.DataFrame:
    """
    データベースからgantt_tasksテーブルのデータを読み込み、データフレームとして返します。

    Args:
    - db_config (dict): データベース接続の詳細。キーにはhost, port, user, password, databaseが含まれます。

    Returns:
    - pd.DataFrame: gantt_tasksテーブルのデータを含むデータフレーム。
    """
    # SQLAlchemyエンジンを作成
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    # データベースからデータを読み込む
    df = pd.read_sql("SELECT * FROM gantt_tasks", engine)
    return df


def write_to_db(df: pd.DataFrame, db_config: dict) -> None:
    """
    指定されたデータフレームをデータベースのgantt_tasksテーブルに書き込みます。あ

    Args:
    - df (pd.DataFrame): 書き込みたいデータを含むデータフレーム。
    - db_config (dict): データベース接続の詳細。キーにはhost, port, user, password, databaseが含まれます。

    Returns:
    - None
    """
    # SQLAlchemyエンジンを作成
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    # データフレームをデータベースに書き込む
    df.to_sql('gantt_tasks', engine, if_exists='replace', index=False)


# +
def generate_relationship_id_using_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    データフレームから親子関係のIDを生成する関数（text列を使用）。

    Parameters:
    - df: pd.DataFrame
        'text'と'parent'の列を持つデータフレーム。

    Returns:
    - pd.DataFrame
        元のデータフレームに'relationship_id'の列が追加されたデータフレーム。
    """

    def get_path(text, relationships, df):
        """タスクのtextから親へのパスを取得"""
        path = [text]
        task_id = df[df['text'] == text]['id'].values[0]
        while relationships[task_id]['parent'] is not None:
            parent_id = relationships[task_id]['parent']
            parent_text = df[df['id'] == parent_id]['text'].values[0]
            path.insert(0, parent_text)
            task_id = parent_id
        return path

    # 親子関係を格納する辞書を初期化
    relationships = {}
    for _, row in df.iterrows():
        task_id = row['id']
        parent_id = row['parent']
        if parent_id == 0:
            relationships[task_id] = {'parent': None, 'children': []}
        else:
            if parent_id not in relationships:
                relationships[parent_id] = {
                    'parent': None, 'children': [task_id]}
            else:
                relationships[parent_id]['children'].append(task_id)
            relationships[task_id] = {'parent': parent_id, 'children': []}

    # "___"を使って親子関係のパスを構築
    df['relationship_id'] = df.apply(lambda row: '___'.join(
        get_path(row['text'], relationships, df)), axis=1)

    return df


def convert_to_str(val):
    """値を文字列に変換

    Args:
        val (Any): 変換する値

    Returns:
        str: 変換後の文字列
    """
    if pd.isnull(val) or val == "":  # NaN, NaT, または空の文字列の場合
        return 'NaN'

    # 値が数値の場合の変換
    if isinstance(val, (int, float)):
        if val == int(val):  # 浮動小数点数が整数の場合
            return str(int(val))
        return str(val)

    # datetime64[ns]タイプまたは文字列が日時フォーマットに見える場合
    if isinstance(val, pd.Timestamp) or (isinstance(val, str) and ("T" in val and "Z" in val or " " in val and ":" in val)):
        try:
            # ISOフォーマットや"2024-03-27 0:00:00" のようなフォーマットも正しく処理される
            return pd.to_datetime(val).strftime('%Y-%m-%d')
        except:
            return str(val)  # 有効な日時形式でない場合はそのままの文字列を返す

    return str(val)


def compare_dataframes(df1, df2, index_col="", df_name=[]):
    """
    2つのデータフレームを比較し、更新された行、追加された行、削除されるべき行を識別します。
    さらに、2つのデータフレーム間で共通および非共通の列に関する情報も出力します。

    Args:
    df1 (pd.DataFrame): 比較の基準となるデータフレーム
    df2 (pd.DataFrame): 比較されるデータフレーム
    df_name (list of str, optional): 'self'と'other'を置き換えるためのデータフレームの名前。デフォルトは空のリスト。

    Returns:
    df_common_updated (pd.DataFrame): df1にこれをupdateするとdf2になる(共通部分)
    added_df (pd.DataFrame): df2で新たに追加された行(df1にこれを足せばdf2になる(非共通部分))
    to_delete_df (pd.DataFrame): df1で存在し、df2で削除された行(df1からこれを消せばdf2になる(非共通部分))
    df_diff (pd.DataFrame): df1とdf2の間で差異がある行の情報
    common_col (Index): df1とdf2の共通の列の名前
    col_diff (tuple): df1とdf2で非共通の列の名前 (df1のみの列, df2のみの列)
    """

    # indexの指定があれば、index列のデータ型を統一してからindexとして設定する
    if index_col != "":
        # データ型を文字列に統一
        df1[index_col] = df1[index_col].astype(str)
        df2[index_col] = df2[index_col].astype(str)

        # indexとして設定
        df1 = df1.set_index(index_col, drop=False)
        df2 = df2.set_index(index_col, drop=False)

    # 共通の列のみ抽出
    common_col = df1.columns.intersection(df2.columns)
    non_common_columns_df1 = df1.columns.difference(df2.columns)
    non_common_columns_df2 = df2.columns.difference(df1.columns)

    df1_common = df1[common_col]
    df2_common = df2[common_col]

    # 各要素をconvert_to_str関数を使用して文字列に変換
    df1_common = df1_common.applymap(convert_to_str)
    df2_common = df2_common.applymap(convert_to_str)

    # df2の中でdf1にないインデックスを見つけ、その行をadded_dfとする
    added_df = df2.loc[df2.index.difference(df1.index)]

    # df1の中でdf2にないインデックスを見つけ、その行をto_delete_dfとする
    to_delete_df = df1.loc[df1.index.difference(df2.index)]

    # df1とdf2の両方に存在するインデックスを持つ行を見つける
    df1_common_index = df1_common.loc[df1_common.index.intersection(
        df2_common.index)]
    df2_common_index = df2_common.loc[df2_common.index.intersection(
        df1_common.index)]

    # df1_commonの中でdf2_commonと異なる部分を更新
    df_out = df1.copy()
    df_out.update(df2_common_index)

    df_common_updated = df_out.copy()
    df_diff = df1_common_index.sort_index()[list(
        df2_common_index.columns)].compare(df2_common_index.sort_index())
    col_diff = (non_common_columns_df1, non_common_columns_df2)

    if len(df_name) == 2:
        df_diff.columns = df_diff.columns.set_levels(df_diff.columns.levels[1].str.replace(
            'self', df_name[0]).str.replace('other', df_name[1]), level=1)

    return df_common_updated, added_df, to_delete_df, df_diff, common_col, col_diff


# +

def extract_js_object_from_html_as_dict(html_path: str, keyword: str) -> dict:
    """
    HTMLファイルから指定されたキーワードのJavaScriptオブジェクトを抽出して、Pythonの辞書として返す関数。

    Parameters:
    - html_path: str
        HTMLファイルのパス。
    - keyword: str
        抽出したいJavaScriptオブジェクトのキーワード。

    Returns:
    - dict
        抽出されたオブジェクトをPythonの辞書として返す。
    """

    # HTMLファイルを読み込む
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # スクリプトタグの中から指定されたキーワードを検索
    script_content = None
    for script in soup.find_all('script'):
        if script.string and keyword in script.string:
            script_content = script.string
            break

    if not script_content:
        return {}

    # 指定されたキーワードの部分を正規表現で抽出
    pattern = rf'{re.escape(keyword)}\s*=\s*(\[.*?\]);'
    match = re.search(pattern, script_content, re.DOTALL)

    if match:
        #         print(match.group(1))
        obj_string = match.group(1)
        # キーをクォートで囲む
        obj_string_quoted = re.sub(r'(\w+):', r'"\1":', obj_string)
        # Pythonの辞書として読み込む
        result_list = eval(obj_string_quoted)
#         print(result_list)
        # 指定された形式の辞書に変換
        result_dict = {str(item['key']): item['label'] for item in result_list}
    else:
        result_dict = {}

    return result_dict

# +
# self = db_con()

# # 関数を使用してrelationship_idを生成
# df = self.create_db()
# df_moto = df.copy()
# db_col = df.columns
# original_dtypes = df.dtypes

# result_df_text = generate_relationship_id_using_text(df)

# # 'relationship_id' 列を使用してソート
# sorted_df = result_df_text.sort_values(by='relationship_id')
# # 関数をテスト
# owner_dict = extract_js_object_from_html_as_dict(
#     'public/index.html', 'gantt.owners')
# #  担当者をIDから
# sorted_df["担当者"] = sorted_df["owner_id"].map(owner_dict)


# # "___"の数を数える
# num_underscores = sorted_df['relationship_id'].str.count("___")

# num_col = []
# # "___"の数に応じて新しい列にxを入れる

# for i in range(1, num_underscores.max() + 2):
#     col_name = str(i)
#     num_col.append(col_name)
#     sorted_df[col_name] = num_underscores.apply(
#         lambda x: 'x' if x == i - 1 else '')

# col_name

# sorted_df.columns

# a = ["text"]

# a.extend(num_col)
# a.extend(['start_date', 'duration', 'progress', 'kind_task',
#          'memo', 'color', 'textColor', '担当者', 'hyperlink'])

# sorted_df[a]

# テストデータ追加

# sorted_df = sorted_df.reset_index(drop=True)

# # # 85と104の間に行を追加するためのインデックスを取得
# index_85 = sorted_df.index[sorted_df['id'] == 147].tolist()[0]
# # index_104 = sorted_df.index[sorted_df['id'] == 208].tolist()[0]

# # 新しい行を作成し、textと3列のみ値を設定
# new_row = pd.Series(index=sorted_df.columns)
# new_row['text'] = 'テスト'
# new_row['3'] = 'x'

# # ID 85 と 104 の間の新しい行を削除
# # sorted_df = sorted_df.drop(index_104)

# # 新しい行を追加
# sorted_df = pd.concat([sorted_df.iloc[:index_85+1], new_row.to_frame().T,
#                       sorted_df.iloc[index_85+1:]]).reset_index(drop=True)

# sorted_df.iloc[index_85-1:index_85+3]  # 対象の範囲を表示して確認

# # id 列がNaNの行を新しく追加された行として識別
# new_rows = sorted_df[sorted_df['id'].isna()]

# # id 列のデータ型を数値に変換
# sorted_df['id'] = pd.to_numeric(sorted_df['id'], errors='coerce')

# # 新しい行の parent と relationship_id を設定
# new_rows = sorted_df[sorted_df['id'].isna()]

# # 今日の日付を取得
# today = datetime.today().strftime('%Y-%m-%d')

# for idx, row in new_rows.iterrows():
#     # 新しい行のxが位置する列の番号-1を取得
#     x_position = int(row[row == 'x'].index[0])
#     parent_position = x_position - 1

#     # その列にxが設定されている最も近い上の行を探す
#     parent_index = sorted_df.iloc[:idx][sorted_df[str(
#         parent_position)] == 'x'].index[-1]
#     parent_row = sorted_df.iloc[parent_index]

#     # その行のidとrelationship_idを新しい行のparentとrelationship_idに設定
#     sorted_df.at[idx, 'parent'] = parent_row['id']
#     sorted_df.at[idx, 'relationship_id'] = parent_row['relationship_id'] + \
#         '___' + row['text']

#     # 新しい行にルールに従って値を設定
#     sorted_df.loc[sorted_df['id'].isna(
#     ), 'start_date'] = sorted_df['start_date'].fillna(today)
#     sorted_df.loc[sorted_df['id'].isna(
#     ), 'duration'] = sorted_df['duration'].fillna(1)
#     sorted_df.loc[sorted_df['id'].isna(
#     ), 'progress'] = sorted_df['progress'].fillna(0)
#     sorted_df.loc[sorted_df['id'].isna(
#     ), 'kind_task'] = sorted_df['kind_task'].fillna(1)

#     # id の最大値を取得して、新しい行の 'id' 列に max_id + 1 を設定
#     max_id = sorted_df['id'].max()
#     sorted_df.at[idx, 'id'] = max_id + 1
#     max_sortorder = sorted_df['sortorder'].max()
#     sorted_df.at[idx, 'sortorder'] = max_sortorder + 1

# sorted_df = sorted_df.fillna("")

# sorted_df[sorted_df['id'] > max_id - len(new_rows)]  # 新しい行の確認

# sorted_df.to_clipboard()

# # 結果を確認
# sorted_df = sorted_df.astype(original_dtypes)

# df_common_updated, added_df, to_delete_df, df_diff, common_col, col_diff = compare_dataframes(
#     df_moto, sorted_df, "id")

# added_df

# to_delete_df

# df_diff

# db_config = {
#     "host": "localhost",
#     "port": 3306,  # default MySQL port
#     "user": "root",
#     "password": "",
#     "database": "gantt_howto_node"
# }

# write_to_db(sorted_df[db_col], db_config)

# ## スケジュール

# def extract_schedule_with_text_from_df_v3(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     DataFrameからtask_scheduleとtextカラムを抽出し、テーブル形式に変換する関数 (さらに修正版)

#     Args:
#     - df (pd.DataFrame): 入力のDataFrame

#     Returns:
#     - pd.DataFrame: 変換したテーブル形式のDataFrame
#     """

#     def convert_task_schedule(row):
#         items = str(row['task_schedule']).split('___')
#         records = []
#         for item in items:
#             parts = item.split(',')
#             if len(parts) >= 3:
#                 records.append({
#                     'original_id': row['id'],
#                     'pro_or_task': row['text'],
#                     'description': parts[1],
#                     'start_date': parts[0],
#                     'duration[days]': parts[2],
#                 })
#         return records

#     extracted_data = df.apply(convert_task_schedule, axis=1)
#     flat_data = [item for sublist in extracted_data for item in sublist]

#     return pd.DataFrame(flat_data)


# # テスト
# extracted_schedule_with_text_df_v3 = extract_schedule_with_text_from_df_v3(df)
# extracted_schedule_with_text_df_v3

# def update_original_df_with_text_v3(original_df: pd.DataFrame, edited_schedule_df: pd.DataFrame) -> pd.DataFrame:
#     """
#     編集後のテーブル形式のデータ（text列を含む）をもとに、オリジナルのDataFrameに変更を反映する関数 (さらに修正版)

#     Args:
#     - original_df (pd.DataFrame): オリジナルのDataFrame
#     - edited_schedule_df (pd.DataFrame): 編集後のテーブル形式のデータ

#     Returns:
#     - pd.DataFrame: 更新されたDataFrame
#     """

#     # start_dateのフォーマットを確認・修正する関数
#     def format_date(date_str):
#         try:
#             return pd.to_datetime(date_str).strftime('%Y-%m-%d')
#         except:
#             return date_str  # フォーマットできない場合はそのまま返す

#     edited_schedule_df['start_date'] = edited_schedule_df['start_date'].apply(
#         format_date)

#     # original_idでgroupbyして文字列を再構築
#     def rebuild_task_schedule(group):
#         return '___'.join([f"{row['start_date']},{row['description']},{row['duration[days]']}" for _, row in group.iterrows()])

#     new_task_schedule = edited_schedule_df.groupby(
#         'original_id').apply(rebuild_task_schedule)

#     # オリジナルのDataFrameを更新
#     updated_df = original_df.copy()
#     updated_df['task_schedule'] = updated_df['id'].map(new_task_schedule)

#     return updated_df


# # テスト
# # ここでは変換したデータをそのまま「編集後」として扱う
# edited_schedule_with_text_df_v3 = extracted_schedule_with_text_df_v3.copy()
# updated_df_with_text_v3 = update_original_df_with_text_v3(
#     df, edited_schedule_with_text_df_v3)
# updated_df_with_text_v3[['id', 'text', 'task_schedule']]


# # ! code .

# ## test

# df_taisho = pd.DataFrame([{'id': 107, 'task_schedule': '2022-7-22,上西内科,1,___'}
#                           ])

# df_taisho

# # self = db_con()

# # # self.create_db()

# # taisho_start = "2022-07-11"
# # nobasu_day = -7
# # self.move_task(taisho_start,nobasu_day)

# retu_mei = "task_schedule"

# metadata_1 = MetaData()
# metadata_1.bind = self.engine_1
# menus = Table(
#     'gantt_tasks', metadata_1,
#     Column('id', Integer, primary_key=True),
#     Column(retu_mei, DATETIME),
# )

# conn = self.engine_1.connect()

# rec = df_taisho.iloc[index:index+1][["id", retu_mei]].to_dict("records")
# insert_stmt = insert(menus).values(rec)

# command = f"on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update({retu_mei}=insert_stmt.inserted.{retu_mei})"

# exec(command)

# conn.execute(on_duplicate_key_stmt)
