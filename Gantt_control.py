#---------------------------class ------------------------------------
# -*- coding: utf-8; py-indent-offset:4 -*-
"""

Copyright (C) ***

##############################################################################
"""
import local_strage
import json
import pandas as pd
from selenium import webdriver
import os

module_path = os.path.dirname(__file__)

class gantt(object):
    '''
    自分自身が使いやすい環境を構築する
    '''
    def __init__(self,pro_name="default"):
        self.driver = webdriver.Chrome('chromedriver')
        self.driver.get('http://localhost:1337/')
        self.storage = local_strage.LocalStorage(self.driver)
        self.data_path = os.path.join(module_path,"data")
        self.pro = pro_name
    
    def save_data(self,pro_name):
        self.pro = pro_name
        task = self.storage["task"]
        task =json.loads(task)
        self.df_task = pd.DataFrame(task)
        df_dic = self.df_task[["id"]].copy()
        df_dic["sin_id"] = f"{self.pro}_" + (df_dic.index + 1).astype("str")
        df_dic = df_dic.astype("str")
        dic = dict(df_dic.set_index("id")["sin_id"])
        self.df_task = self.df_task.astype("str")
        self.df_task["id"] = self.df_task["id"].map(dic)
        self.df_task["parent"] = self.df_task["parent"].map(dic)
        self.df_task.to_csv(os.path.join(self.data_path,f"{self.pro}.csv"),index=False)
        self.df_task.to_excel(os.path.join(self.data_path,f"{self.pro}.xlsx"),index=False)
        self.driver.refresh()

    def db_to_gantt(self,pro_name):
        self.pro = pro_name
        df_task_edit = pd.read_csv(os.path.join(self.data_path,f"{self.pro}.csv"))
        df_task_edit["kind_task"] = df_task_edit["kind_task"].astype("str")
        out_json = df_task_edit.to_json(orient='records')
        self.storage.set("task", out_json)
        self.driver.refresh()

    def quit(self):
        self.driver.quit()
        self.driver.refresh()
    
    def clear_all(self):
        self.storage.clear()
        self.driver.refresh()
