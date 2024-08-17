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

# ! open .

# ! code .

# # 日付をずらす

# +
import DB_python ; obj = DB_python.db_con()

taisho_start = "2024-7-29"
nobasu_day = 7
obj.move_task(taisho_start,nobasu_day)
# -

# # GSSからgatttへ入れる

import DB_python ,my_utility; self = DB_python.db_con();df = self.create_db();df_sc = df[["id","text","task_schedule"]].copy().dropna();df_sc = df_sc[df_sc["task_schedule"]!=""]
import sys;sys.path.append("../mylib");import gss_my;gss_my.print_schedule(60,df_sc)

qg = my_utility.qgid_local(df_sc);qg


df_sc_edit = qg.get_changed_df()

df_sc_edit



df_comp, df_add_index, _, df_del_index, _ = my_utility.df_compare(df_sc,df_sc_edit)

df_comp

df_add_index

df_del_index

for index in list(df_comp.index):
    print(index)
    taisho = df_sc_edit.loc[[index]]
    out = self.to_db(taisho,"task_schedule")

if len(df_add_index) != 0:
    out = self.to_db(df_add_index,"task_schedule")

if len(df_del_index) != 0:
    df_del_index["task_schedule"] = ""
    out = self.to_db(df_del_index,"task_schedule")

# # 買物リスト
#
# 以下のサイトから買物リストをコピーして、コードを実行する。結果、クリップボードに入るので、GSSへ貼り付ける
#
# https://www.amazon.co.jp/alexaquantum/sp/alexaShoppingList?ref=nav_asl

import pyperclip
import pandas as pd
text = pyperclip.paste()
text

# +
# textから買物リストを作成する
items_corrected = []
for block in text.strip().split('\n\n'):
    lines = block.split('\n')
    if len(lines) > 0 and "追加されました" not in lines[0]:  # 「追加されました」を含まない最初の行をアイテムとして認識
        items_corrected.append(lines[0].strip())
        
nuki_list = ['メインコンテンツにスキップ','すべてのカテゴリー', 'お客様の閲覧履歴に含まれている商品を閲覧した人は、こんな商品も見ています', 'トップへ戻る']
for i in nuki_list:
    try:
        items_corrected.remove(i)
    except:
        pass
    
# データフレームを作成する
shopping_list_df = pd.DataFrame({
    '商品名': items_corrected,
    'temp_1': [""]* len(items_corrected),
    'temp_2': ["買物"]* len(items_corrected),
    '急がない': [True] * len(items_corrected)  # 各商品にTrueを設定
})

shopping_list_df.to_clipboard(index=False,header=False)

# -
# # [四季報](http://localhost:8888/notebooks/stock_app/TOP.ipynb)



