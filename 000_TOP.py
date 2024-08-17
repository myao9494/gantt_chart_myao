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

# # GSSへ入れる

# 共通

# +
import sys;sys.path.append("../mylib");import gss_my
import pendulum
df = gss_my.create_df()
row=len(df)+2

def gss_my_input(row,sch_date):
    date = pendulum.datetime(year=int(sch_date[0]),month=int(sch_date[1]),day=int(sch_date[2]),hour=int(sch_date[3]),minute=int(sch_date[4]))
    gss_my.worksheet.update_cell(row, 2, str(date)[:-6]+".000Z")
    gss_my.worksheet.update_cell(row, 4, sch_date[5])
    gss_my.worksheet.update_cell(row, 5, "True")


# -

# # 連続で入れる

li =[1,2,3,5,6,8,12,14,16,19,22,23,24,25]

len(li)

for no ,i in enumerate(li):
    sch_date = (2024,7,i,7,0,"部活")
#     print(row)
    gss_my_input(row,sch_date)
    row = row + 1

# ### 単体で入れる

# 直接作成

sch_date = (2022,10,2,7,0,"部活(24~25日)")

gss_input(row,sch_date)

row = row + 1

# ### リストから

li = [
 '2024-11-18-7-0-権利確定日 逆日歩1日',
 '2024-11-27-7-0-権利確定日 逆日歩3日',
 '2024-12-18-7-0-権利確定日 逆日歩3日',
 '2024-12-26-7-0-権利確定日 逆日歩7日']

for i in li:
    sch_date = i.split("-")
#     print(sch_date)
    gss_input(row,sch_date)
    row = row + 1

# ### 文から作成

# +
from Reminder_data_from_ambiguous_information import remind_make; 

tex = "12/29" + "ピアノ休"
sch_date = remind_make.main(tex,pendulum.now())
sch_date
# -

# gssへ入力

gss_input(row,sch_date)
row = row + 1

# # 月初

# ## 会社メールに、70日間の予定を送信する

# +
from gss_my import *
day_num = 70

df = create_df()
df["開始日時"] = pd.to_datetime(df["開始日時"], utc=True)

df_c = df[df["開始日時"] > pendulum.today()].copy()
df_c = df_c[df_c["開始日時"] < pendulum.today().add(days=day_num)]

df_c.sort_values("開始日時")[['開始日時', '終了日時', '名称']].to_clipboard(index=False)

# + active=""
# 開始日時	終了日時	名称
# 2024-08-01 19:00:00+00:00	2024-08-01T20:00:00Z	郵便の配達
# 2024-08-02 17:30:00+00:00	2024-08-02T09:30:00Z	上西内科
# 2024-08-02 19:30:00+00:00	2024-8/2 20:30:00	オンライン数学ゼミ
# 2024-08-03 14:00:00+00:00	2024-08-03T17:30:00Z	第6回統一テスト
# 2024-08-04 19:30:00+00:00	2024-8/4 20:30:00	オンライン数学ゼミ
# 2024-08-05 08:15:00+00:00	2024-8/5 11:15:00	部活
# 2024-08-05 13:00:00+00:00	2024-08-05T14:00:00Z	免許の講習
# 2024-08-05 13:30:00+00:00	2024-8/5 20:30:00	オンライン数学ゼミ・総復習講座・英語・理科特訓
# 2024-08-06 13:30:00+00:00	2024-8/6 20:30:00	総復習講座・英語・理科特訓
# 2024-08-07 08:15:00+00:00	2024-8/7 11:15:00	部活
# 2024-08-08 13:30:00+00:00	2024-8/8 20:30:00	オンライン数学ゼミ・総復習講座・英語・理科特訓
# 2024-08-09 08:15:00+00:00	2024-8/9 11:15:00	部活
# 2024-08-09 19:30:00+00:00	2024-8/9 20:30:00	オンライン数学ゼミ
# 2024-08-10 13:30:00+00:00	2024-8/10 17:40:00	総復習講座・英語・理科特訓
# 2024-08-11 07:00:00+00:00	2024-08-11T08:00:00Z	8/11 合宿の買物_前日(おかし、昼食)
# 2024-08-11 12:00:00+00:00	2024-08-11T13:00:00Z	昼食 初盆集合
# 2024-08-12 07:00:00+00:00	2024/08/15 18:00:00	8月12日から3泊4日　合宿
# 2024-08-14 07:00:00+00:00	2024-08-14T08:00:00Z	楽天の株主優待申し込み期限 027768887
# 2024-08-16 07:00:00+00:00	2024-08-16T08:00:00Z	権利確定日 逆日歩1日
# 2024-08-16 17:00:00+00:00	2024-08-16T18:00:00Z	ピアノ休
# 2024-08-17 07:00:00+00:00	2024-08-17T08:00:00Z	アンソロピック解約
# 2024-08-18 13:30:00+00:00	2024-8/18 17:40:00	総復習講座・英語・理科特訓
# 2024-08-19 07:00:00+00:00	2024/08/20 8:00:00	Apple Music解約
# 2024-08-19 07:00:00+00:00	2024-08-19T08:00:00Z	出校日
# 2024-08-19 13:30:00+00:00	2024-8/19 20:30:00	総復習講座・英語・理科特訓
# 2024-08-20 08:15:00+00:00	2024-8/20 11:15:00	部活
# 2024-08-20 13:30:00+00:00	2024-8/20 20:30:00	総復習講座・英語・理科特訓
# 2024-08-21 08:15:00+00:00	2024-8/21 11:15:00	部活
# 2024-08-22 13:30:00+00:00	2024-8/22 20:30:00	内申対策講座
# 2024-08-23 08:15:00+00:00	2024-8/23 11:15:00	部活
# 2024-08-23 13:30:00+00:00	2024-8/23 20:30:00	内申対策講座
# 2024-08-26 08:15:00+00:00	2024-8/26 11:15:00	部活
# 2024-08-26 13:30:00+00:00	2024-8/26 20:30:00	内申対策講座
# 2024-08-27 07:00:00+00:00	2024-08-27T08:00:00Z	アマゾンのポイント確認
# 2024-08-27 08:15:00+00:00	2024-8/27 11:15:00	部活
# 2024-08-27 13:30:00+00:00	2024-8/27 20:30:00	内申対策講座
# 2024-08-28 07:00:00+00:00	2024-08-28T08:00:00Z	権利確定日 逆日歩3日
# 2024-08-28 08:15:00+00:00	2024-8/28 11:15:00	部活
# 2024-08-28 13:30:00+00:00	2024-8/28 17:05:00	内申対策講座
# 2024-08-31 07:00:00+00:00	2024-08-31T08:00:00Z	2024年8月31日U-NEXT株主優待期限
# 2024-09-01 07:00:00+00:00	2024-09-01T08:00:00Z	chocoZAPの申し込み株主優待
# 2024-09-02 07:00:00+00:00	2024-09-02T08:00:00Z	始業式
# 2024-09-03 00:00:00+00:00	2024-09-03T00:00:00Z	実力テスト
# 2024-09-03 07:00:00+00:00	2024/09/03 23:00:00	小牧プレミアム商品券販売開始
# 2024-09-12 07:00:00+00:00	2024-09-14T07:00:00Z	中間テスト
# 2024-09-18 07:00:00+00:00	2024-09-18T08:00:00Z	権利確定日 逆日歩4日
# 2024-09-18 17:30:00+00:00	2024/09/18 18:30:00	歯医者
# 2024-09-26 07:00:00+00:00	2024-09-26T08:00:00Z	権利確定日 逆日歩1日
# 2024-09-27 17:00:00+00:00	2024-09-27T18:00:00Z	ピアノ休
# 2024-10-01 07:00:00+00:00	2024-10-01T07:00:00Z	3年生進路説明会
# 2024-10-03 07:00:00+00:00	2024-10-03T08:00:00Z	体育祭
#
# -

# # 一年に一回

# ## ピアノの日

# +
from datetime import datetime, timedelta

# 2024年の金曜日の日付を求める
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

# 金曜日のリストを作成
fridays_2024 = []
while start_date <= end_date:
    if start_date.weekday() == 4:  # 金曜日は weekday() が 4
        fridays_2024.append(start_date)
    start_date += timedelta(days=1)

# フォーマットに合わせたピアノの予定リストを作成
piano_schedule = [[date.year, date.month, date.day, 17, 0, "ピアノ"] for date in fridays_2024]
# piano_schedule[:5]  # 最初の5件を表示して確認
piano_schedule
# -

li_piano = [
 [2024, 7, 5, 17, 0, 'ピアノ'],
 [2024, 7, 12, 17, 0, 'ピアノ'],
 [2024, 7, 19, 17, 0, 'ピアノ'],
 [2024, 7, 26, 17, 0, 'ピアノ'],
 [2024, 8, 2, 17, 0, 'ピアノ'],
 [2024, 8, 9, 17, 0, 'ピアノ'],
 [2024, 8, 16, 17, 0, 'ピアノ休'],
 [2024, 8, 23, 17, 0, 'ピアノ'],
 [2024, 8, 30, 17, 0, 'ピアノ'],
 [2024, 9, 6, 17, 0, 'ピアノ'],
 [2024, 9, 13, 17, 0, 'ピアノ'],
 [2024, 9, 20, 17, 0, 'ピアノ'],
 [2024, 9, 27, 17, 0, 'ピアノ休'],
 [2024, 10, 4, 17, 0, 'ピアノ'],
 [2024, 10, 11, 17, 0, 'ピアノ'],
 [2024, 10, 18, 17, 0, 'ピアノ'],
 [2024, 10, 25, 17, 0, 'ピアノ'],
 [2024, 11, 1, 17, 0, 'ピアノ休'],
 [2024, 11, 8, 17, 0, 'ピアノ'],
 [2024, 11, 15, 17, 0, 'ピアノ'],
 [2024, 11, 22, 17, 0, 'ピアノ'],
 [2024, 11, 29, 17, 0, 'ピアノ'],
 [2024, 12, 6, 17, 0, 'ピアノ'],
 [2024, 12, 13, 17, 0, 'ピアノ'],
 [2024, 12, 20, 17, 0, 'ピアノ'],
 [2024, 12, 27, 17, 0, 'ピアノ休']]

for i in li_piano:
    gss_input(row,i)
    row = row + 1



# # factory
#

# ## macのスケジュール

# +
import EventKit
import pandas as pd
from datetime import datetime

# Event Storeのインスタンスを作成
event_store = EventKit.EKEventStore.alloc().init()

# イベントのアクセス権限を確認/リクエスト
# access_granted = event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeEvent, None)

# if not access_granted:
#     print("Access to the Calendar is not granted.")
#     exit()

# 日付範囲を設定 (ここでは1年前から1年後まで)
start_date = EventKit.NSDate.dateWithTimeIntervalSinceNow_(-365*24*60*60)
end_date = EventKit.NSDate.dateWithTimeIntervalSinceNow_(365*24*60*60)
predicate = event_store.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, None)

# イベントを取得
events = event_store.eventsMatchingPredicate_(predicate)

# イベント情報を抽出してDataFrameに変換
event_data = []
for event in events:
    event_info = {
        'title': event.title(),
        'start_date': event.startDate(),
        'end_date': event.endDate(),
        'location': event.location() or ''
    }
    event_data.append(event_info)

df_events = pd.DataFrame(event_data)

# DataFrameの表示
# print(df_events)
# -
df_events

# +
import EventKit
import pandas as pd
from datetime import datetime

# Event Storeのインスタンスを作成
event_store = EventKit.EKEventStore.alloc().init()

# 以下の関数は、新しいイベントを追加します
def add_event(title, start_date, end_date, location=''):
    new_event = EventKit.EKEvent.eventWithEventStore_(event_store)
    new_event.setTitle_(title)
    new_event.setStartDate_(start_date)
    new_event.setEndDate_(end_date)
    new_event.setLocation_(location)
    
    error = None
    event_store.saveEvent_span_error_(new_event, EventKit.EKSpanThisEvent, error)
    
    if error:
        print(f"Error saving event: {error.localizedDescription()}")


# 以下の関数は、指定されたタイトルのイベントを削除します
def delete_event(title):
    predicate = event_store.predicateForEventsWithStartDate_endDate_calendars_(
        EventKit.NSDate.dateWithTimeIntervalSinceNow_(-365*24*60*60), 
        EventKit.NSDate.dateWithTimeIntervalSinceNow_(365*24*60*60), 
        None
    )
    events = event_store.eventsMatchingPredicate_(predicate)
    for event in events:
        if event.title() == title:
            event_store.removeEvent_span_error_(event, EventKit.EKSpanThisEvent, None)
            break

# 以下の関数は、指定されたタイトルのイベントを更新します
def update_event(old_title, new_title, new_start_date=None, new_end_date=None, new_location=None):
    predicate = event_store.predicateForEventsWithStartDate_endDate_calendars_(
        EventKit.NSDate.dateWithTimeIntervalSinceNow_(-365*24*60*60), 
        EventKit.NSDate.dateWithTimeIntervalSinceNow_(365*24*60*60), 
        None
    )
    events = event_store.eventsMatchingPredicate_(predicate)
    for event in events:
        if event.title() == old_title:
            event.setTitle_(new_title)
            if new_start_date:
                event.setStartDate_(new_start_date)
            if new_end_date:
                event.setEndDate_(new_end_date)
            if new_location:
                event.setLocation_(new_location)
            event_store.saveEvent_span_error_(event, EventKit.EKSpanThisEvent, None)
            break


# -

# 使用例:
# 新しいイベントを追加
add_event('Meeting', EventKit.NSDate.date(), EventKit.NSDate.dateWithTimeIntervalSinceNow_(3600), 'Office')

# +
# イベントを削除
delete_event('Meeting')

# イベントを更新
update_event('Old Meeting Title', 'New Meeting Title')

# +
# イベントの追加
add_event('Meeting', EventKit.NSDate.date(), EventKit.NSDate.dateWithTimeIntervalSinceNow_(3600), 'Office')

# イベントの取得と表示
predicate = event_store.predicateForEventsWithStartDate_endDate_calendars_(
    EventKit.NSDate.dateWithTimeIntervalSinceNow_(-365*24*60*60), 
    EventKit.NSDate.dateWithTimeIntervalSinceNow_(365*24*60*60), 
    None
)
events = event_store.eventsMatchingPredicate_(predicate)
event_data = []
for event in events:
    event_info = {
        'title': event.title(),
        'start_date': event.startDate(),
        'end_date': event.endDate(),
        'location': event.location() or ''
    }
    event_data.append(event_info)

df_events = pd.DataFrame(event_data)
# print(df_events)

# -

df_events

# +
import EventKit
from Foundation import NSError
import ctypes
import pandas as pd
from datetime import datetime

# Event Storeのインスタンスを作成
event_store = EventKit.EKEventStore.alloc().init()

def add_event(title, start_date, end_date, location=''):
    new_event = EventKit.EKEvent.eventWithEventStore_(event_store)
    new_event.setTitle_(title)
    new_event.setStartDate_(start_date)
    new_event.setEndDate_(end_date)
    new_event.setLocation_(location)
    
    error_ptr = ctypes.pointer(ctypes.py_object(NSError.new()))
    success = event_store.saveEvent_span_error_(new_event, None, error_ptr)
    
    if not success:
        error = error_ptr.contents.value
        print(f"Error saving event: {error.localizedDescription()}")
    else:
        print("Event saved successfully")

# 使用例:
add_event('Meeting', EventKit.NSDate.date(), EventKit.NSDate.dateWithTimeIntervalSinceNow_(3600), 'Office')

# -





# +
import EventKit
import pandas as pd

# Event Storeのインスタンスを作成
event_store = EventKit.EKEventStore.alloc().init()

# +
# # リマインダーのアクセス権限を確認/リクエスト
# access_granted = event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, None)
# if not access_granted:
#     print("Access to the Reminders is not granted.")
#     exit()

# +
import EventKit
import pandas as pd

# Event Storeのインスタンスを作成
event_store = EventKit.EKEventStore.alloc().init()

# リマインダーのアクセス権限を確認/リクエスト
# access_granted = event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, None)
# if not access_granted:
#     print("Access to the Reminders is not granted.")
#     exit()
# -
# すべてのリマインダーを取得するためのpredicateを作成
predicate = event_store.predicateForRemindersInCalendars_(None)
predicate

# リマインダーを取得
reminders = event_store.fetchRemindersMatchingPredicate_completion_(predicate, None)
reminders

# +
# reminders?
# -

# リマインダー情報を抽出してDataFrameに変換
reminder_data = []
for reminder in reminders:
    reminder_info = {
        'title': reminder.title(),
        'due_date': reminder.dueDateComponents().date() if reminder.dueDateComponents() else None,
        'completed': reminder.isCompleted(),
        'completion_date': reminder.completionDate(),
        'notes': reminder.notes() or ''
    }
    reminder_data.append(reminder_info)
# +
df_reminders = pd.DataFrame(reminder_data)

# DataFrameの表示
print(df_reminders)
# +
import EventKit

# Event Storeのインスタンスを作成
event_store = EventKit.EKEventStore.alloc().init()

# リマインダーのアクセス権限を確認/リクエスト
# access_granted = event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, None)
# if not access_granted:
#     print("Access to the Reminders is not granted.")
#     exit()

# リマインダーリストを取得
reminder_lists = event_store.calendars()

# リマインダーリストの名前を出力
for reminder_list in reminder_lists:
    # リマインダーリストのタイプを確認 (リマインダーのリストのみ出力)
    if reminder_list.type() == EventKit.EKCalendarTypeReminder:
        print(reminder_list.title())


# +
import EventKit

# Event Storeのインスタンスを作成
event_store = EventKit.EKEventStore.alloc().init()

# # リマインダーのアクセス権限を確認/リクエスト
# access_granted = event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, None)
# if not access_granted:
#     print("Access to the Reminders is not granted.")
#     exit()

# カレンダーとリマインダーリストを取得
all_calendars = event_store.calendars()

# カレンダーとリマインダーリストの名前を出力
for calendar in all_calendars:
    print(calendar.title())

# -

EventKit.EKCalendarTypeCalDAV

a = reminder_lists[5]

a.type()

# +
import subprocess

def get_reminder_lists():
    script = '''
    tell application "Reminders"
        set listNames to name of every list
        return listNames as text
    end tell
    '''
    process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode == 0:
        # AppleScript returns the list names as a single text string, each name separated by a comma and a space
        reminder_lists = stdout.decode('utf-8').strip().split(", ")
        return reminder_lists
    else:
        print(f"Script failed with error: {stderr.decode('utf-8')}")
        return None

# Get the list of reminder lists
reminder_lists = get_reminder_lists()
if reminder_lists is not None:
    for i, list_name in enumerate(reminder_lists, 1):
        print(f"{i}. {list_name}")

# -

reminder_lists

# +
import subprocess
import json

def get_all_tasks():
    script = '''
    tell application "Reminders"
        set allTasks to {}
        repeat with aList in every list
            repeat with aTask in every reminder of aList
                set end of allTasks to {listName:name of aList, taskName:name of aTask, notes:note of aTask}
            end repeat
        end repeat
        return allTasks
    end tell
    '''
    process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    
    if process.returncode == 0:
        # Convert the AppleScript record string to a valid JSON string, then parse it to a Python dictionary
        json_str = stdout.replace("{", "{\"").replace("}", "\"}").replace(":", "\":\"").replace(", ", "\",\"").replace(";", "\",\"")
        tasks = json.loads(json_str)
        return tasks
    else:
        print(f"Script failed with error: {stderr}")
        return None

# Get all tasks
all_tasks = get_all_tasks()
if all_tasks is not None:
    for task in all_tasks:
        print(f"List: {task['listName']}, Task: {task['taskName']}, Notes: {task['notes']}")

# -


