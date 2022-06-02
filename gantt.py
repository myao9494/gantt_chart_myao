# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

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




