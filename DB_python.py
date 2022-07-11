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

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String,DATETIME
from sqlalchemy.dialects.mysql import insert
import pandas as pd
# import utility

class db_con(object):
    '''
    pythonからmysqlのDBへアクセスする
    '''
    def __init__(self):
        pd.set_option("display.max_colwidth",10000)
        pd.set_option('display.max_rows', 500)
        self.user="root"
        self.password=""
        self.host="localhost"
        self.port=3306
        self.database_1 ="gantt_howto_node"
        self.url_1 = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_1}?charset=utf8'
        self.engine_1 = create_engine(self.url_1,echo=False)

    def create_db(self):
        query = "select * from gantt_tasks"
        self.df = pd.read_sql(query,con=self.engine_1)
        return self.df

    def move_task(self,taisho_start,nobasu_day):
#         if not hasattr(self,"df"):
        self.create_db()
        df_taisho = self.df.copy()
        df_taisho = df_taisho[df_taisho["start_date"]==taisho_start]
        df_taisho["start_date"] = df_taisho["start_date"] + pd.Timedelta(days = nobasu_day)
        
        if len(df_taisho) != 0:
            metadata_1 = MetaData()
            metadata_1.bind = self.engine_1
            menus = Table(
              'gantt_tasks', metadata_1,
              Column('id', Integer, primary_key=True),
              Column('start_date', DATETIME),
            )

            conn = self.engine_1.connect()

            for index in range(len(df_taisho)):
                rec = df_taisho.iloc[index:index+1][["id","start_date"]].to_dict("records")
                insert_stmt = insert(menus).values(rec)
                on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
                    start_date=insert_stmt.inserted.start_date
                )
                conn.execute(on_duplicate_key_stmt)
#                 print(index,rec)
            conn.close()
        else:
            print("０件でした")

# ## test

# +
# self = db_con()

# # self.create_db()

# taisho_start = "2022-07-11"
# nobasu_day = -7
# self.move_task(taisho_start,nobasu_day)


