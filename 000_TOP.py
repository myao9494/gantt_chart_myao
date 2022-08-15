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

# # 予定を入れる 

# glideへ入れる

import sys;sys.path.append("../mylib");import gss
import pendulum
df = gss.create_df()

# チョク

sch_date = (2022,8,23,7,0,"部活(23~26日)")
sch_date

# 文字

from Reminder_data_from_ambiguous_information import remind_make; 
sch_date = remind_make.main("明日誕生日",pendulum.now())
sch_date

# 入力

i=len(df)+2
date = pendulum.datetime(year=int(sch_date[0]),month=int(sch_date[1]),day=int(sch_date[2]),hour=int(sch_date[3]),minute=int(sch_date[4]))

worksheet.update_cell(i, 2, str(date)[:-6]+".000Z")
worksheet.update_cell(i, 3, sch_date[5])
worksheet.update_cell(i, 4, "True")

# ## glideからgatttへ入れる

import sys;sys.path.append("../mylib");import gss;gss.print_week_schedule();import pandas  as pd

import DB_python ,my_utility; self = DB_python.db_con();df = self.create_db();df_sc = df[["id","text","task_schedule"]].copy().dropna();df_sc = df_sc[df_sc["task_schedule"]!=""]
qg = my_utility.qgid_local(df_sc);qg


df_sc_edit = qg.get_changed_df();df_comp, df_add_index, _, df_del_index, _ = my_utility.df_compare(df_sc,df_sc_edit)

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

# # 日付をずらす

import DB_python ; obj = DB_python.db_con()

taisho_start = "2022-8-15"
nobasu_day = -7
obj.move_task(taisho_start,nobasu_day)

# # factory
