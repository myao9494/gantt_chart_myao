# -*- coding: utf-8 -*-
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

# # link

# [github](https://github.com/myao9494/gantt_chart_myao)

# # factory

# ## 日付をずらす

import DB_python ; obj = DB_python.db_con()

taisho_start = "2022-7-4"
# taisho_start = "2022-7-11"
nobasu_day = 7
obj.move_task(taisho_start,nobasu_day)

# ## 予定を作成する

# 予定を確認

import DB_python ; self = DB_python.db_con()

df = self.create_db()

df_sc = df[["id","text","task_schedule"]].copy().dropna()
df_sc = df_sc[df_sc["task_schedule"]!=""]

df_sc

qg = DB_python.qgid_local(df_sc)

qg

# 予定を編集

import pandas  as pd

df_sc_edit = qg.get_changed_df()
df_sc.compare(df_sc_edit)



self.to_db(df_sc_edit.loc[8:9],"task_schedule")

# 新規作成

id_num = 15

id_num in list(df_sc_edit["id"])

if id_num  in list(df_sc["id"]):
    out = df_sc.loc[id_num,"task_schedule"] + "___" + yotei_str
    df_out = pd.DataFrame([[id_num,out]],columns=["id","task_schedule"])
    print(out)
else:
    out = yotei_str + "___" 
    df_out = pd.DataFrame([[id_num,out]],columns=["id","task_schedule"])

df_out

rec = df_out.iloc[0:1][["id", "task_schedule"]].to_dict("records")[0]

rec





 values(id=str(rec["id"]), data=rec["task_schedule"])



self.to_db(df_out,"task_schedule")

import pandas as pd





id_num = 107
yotei = "上西内科"
date = "2022-7-22"
length = 1
biko = ""

yotei_str = f"{date},{yotei},{str(length)},{biko}"

self.to_db()





import pendulum

date = pendulum.datetime(2022,7,21)
yotei = "部活"
id_num =48

out = f'[{str(id_num)},"{yotei}",new Date({date.year},{date.month-1},{date.day})],'



# +
import qgrid
import pandas as pd
url = 'https://github.com/chris1610/pbpython/blob/master/data/2018_Sales_Total_v2.xlsx?raw=True'
df = pd.read_excel(url)

widget = qgrid.show_grid(df)
# -

widget

# ## 過去

import Gantt_control
self = Gantt_control.gantt()

self.save_data("default")

# ガントへデータからエクセルへ

self.db_to_gantt("default")

# df_taskを編集

# ! code .

# 編集結果を取得

# df_task_edit = pd.read_csv("df_task.csv")


# データを戻す



# 完了したら閉じる



# 消す




