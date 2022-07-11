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

taisho_start = "2022-6-27"
nobasu_day = 7
obj.move_task(taisho_start,nobasu_day)

# # 予定を作成する







import pendulum

date = pendulum.datetime(2022,7,21)
yotei = "部活"
id_num =48

out = f'[{str(id_num)},"{yotei}",new Date({date.year},{date.month-1},{date.day})],'





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




