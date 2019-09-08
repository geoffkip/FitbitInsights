#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 21:22:54 2019

@author: geoffrey.kip
"""

import pandas as pd
import os
import json
import re

def find_word(text, search):

   result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
   if len(result)>0:
      return True
   else:
      return False

files = os.listdir("../data")


### READ HEART RATE DATA IN  ####
heart_rate_files = []
for file in files:
    if find_word(file,"heart_rate"):
        print(file)
        heart_rate_files.append(file)
        
results = []
with open("result.json", "w") as outfile:
    for file in heart_rate_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)
    

dates= []
bpms = []

for d in results:
    date = d["dateTime"]
    bpm = d["value"]["bpm"]
    dates.append(date)
    bpms.append(bpm)
        
heart_rates = dict(zip(dates, bpms))

df = pd.DataFrame(list(heart_rates.items()), columns=['DateTime', 'BPM'])
df.head()
df.dtypes

df["DateTime"] = pd.to_datetime(df["DateTime"],format="%m/%d/%y %H:%M:%S")
df.sort_values(by="DateTime",inplace=True)
df["DateTime"].min()
df["DateTime"].max()
df.to_csv("processed_data/all_heart_rate_data.csv",index=False)


df['Year']= df['DateTime'].dt.year
df['Month']=df['DateTime'].dt.month
df['Day']= df['DateTime'].dt.day
df['Hour']=df['DateTime'].dt.hour
df['Minute']=df['DateTime'].dt.minute
df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day','Hour']])

heart_rate_by_hour = df.groupby(['Date']).BPM.mean()
heart_df = pd.DataFrame(heart_rate_by_hour)
heart_df.reset_index(inplace=True)
heart_df['Year']= heart_df['Date'].dt.year
heart_df['Month']=heart_df['Date'].dt.month
heart_df['Day']= heart_df['Date'].dt.day
heart_df['Date2'] = pd.to_datetime(heart_df[['Year', 'Month', 'Day']])
heart_df.drop(['Year','Month','Day'],axis=1,inplace=True)

### READ SLEEP DATA IN ###
sleep_files = []
for file in files:
    if find_word(file,"sleep"):
        print(file)
        sleep_files.append(file)
        
results = []
with open("..processed_data/result.json", "w") as outfile:
    for file in sleep_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)
    

sleep_dict={}
sleep_dict['Date'] = []
sleep_dict['sleep_duration'] = []
sleep_dict['sleep_efficiency'] = []
sleep_dict['sleep_start_time'] = []
sleep_dict['minutes_after_wakeup'] = []
sleep_dict['minutes_asleep'] = []
sleep_dict['minutes_awake'] = []
sleep_dict['minutes_to_fall_asleep'] = []
sleep_dict['time_in_bed'] = []
sleep_dict['deep_sleep'] = []
sleep_dict['rem_sleep'] = []
sleep_dict['wake_sleep'] = []
sleep_dict['light_sleep'] = []

for d in results:
    Date = d["dateOfSleep"]
    sleep_duration = d["duration"]
    sleep_efficiency = d["efficiency"]
    sleep_start_time = d["startTime"]
    sleep_endtime = d["endTime"]
    minutes_after_wakeup = d["minutesAfterWakeup"]
    minutes_asleep = d["minutesAsleep"]
    minutes_awake = d["minutesAwake"]
    minutes_to_fall_asleep= d["minutesToFallAsleep"]
    time_in_bed = d["timeInBed"]
    try:
        deep_sleep = d["levels"]["summary"]["deep"]["minutes"]
    except:
        print("No deep sleep value")
    try:
        rem_sleep = d["levels"]["summary"]["rem"]["minutes"]
    except:
        print("No Rem sleep value")
    try:
        wake_sleep = d["levels"]["summary"]["wake"]["minutes"]
    except:
        print("No wake sleep")
    try:
        light_sleep = d["levels"]["summary"]["light"]["minutes"]
    except:
        print("No light sleep")
    sleep_dict['Date'].append(Date)
    sleep_dict['sleep_duration'].append(sleep_duration)
    sleep_dict['sleep_efficiency'].append(sleep_efficiency)
    sleep_dict['sleep_start_time'].append(sleep_start_time)
    sleep_dict['minutes_after_wakeup'].append(minutes_after_wakeup)
    sleep_dict['minutes_asleep'].append(minutes_asleep)
    sleep_dict['minutes_awake'].append(minutes_awake)
    sleep_dict['minutes_to_fall_asleep'].append(minutes_to_fall_asleep)
    sleep_dict['time_in_bed'].append(time_in_bed)
    sleep_dict['deep_sleep'].append(deep_sleep)
    sleep_dict['rem_sleep'].append(rem_sleep)
    sleep_dict['wake_sleep'].append(wake_sleep)
    sleep_dict['light_sleep'].append(light_sleep)
   
df=pd.DataFrame(sleep_dict)
df.head()
df.dtypes

df["Date"] = pd.to_datetime(df["Date"],format="%Y/%m/%d %H:%M:%S")
df["sleep_duration"] = df["sleep_duration"]/3600000
df.sort_values(by="Date",inplace=True)

heart_sleep_df= pd.merge(heart_df, df, left_on='Date2', right_on='Date', how='left')
heart_sleep_df.drop(["Date_y"],axis=1,inplace=True)
heart_sleep_df.rename({"Date_x": "DateTime", "Date2": "MonthYearDay"},inplace=True,axis=1)