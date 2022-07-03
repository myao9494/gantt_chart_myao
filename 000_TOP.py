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

# # link

# [github](https://github.com/myao9494/gantt_chart_myao)

# # factory

# ## 予定を作成する

import pendulum

date = pendulum.datetime(2022,7,21)
yotei = "部活"
id_num =48

out = f'[{str(id_num)},"{yotei}",new Date({date.year},{date.month-1},{date.day})],'







import pandas as pd

# +

a = "3 4 3"
b = "5 4 3 2"
c = "1 2 3 4"
d = "1 2 2 1"
# -

a = "3 5 1"
b= "0 1 1 1 1"
c = "0 0 1 1 1"
d = "0 0 0 1 1"

li = []

li.append( b.split(" "))
li.append( c.split(" "))
li.append( d.split(" "))

df = pd.DataFrame(li).astype("int")

df

top = int(a.split(" ")[0])-1
gyo =  int(a.split(" ")[2])

gyo

out = 0
yoko_1 = top-1
yoko_2 = top+1
for i in range(gyo):
#     print(i)
    if i == 0:
        temp = df.iloc[0,top]
    else:
        temp = df.iloc[i,yoko_1:yoko_2+1].sum()
        yoko_1 = yoko_1-1
        if yoko_1 <0:
            yoko_1 = 0
        yoko_2 = yoko_2+1
    print(temp,yoko_1,yoko_2)
    out = out +temp
print(out)



df.iloc[i,yoko_1:yoko_2+1].sum()

df.iloc[0,1:6].sum()

df.iloc[2,1:6]

df.iloc[1,[tg-1]





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




