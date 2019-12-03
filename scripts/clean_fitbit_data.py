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
df.to_csv("../processed_data/all_heart_rate_data.csv",index=False)

##Read in data from csv file ###
df = pd.read_csv("../processed_data/all_heart_rate_data.csv")
df["DateTime"] = pd.to_datetime(df["Date"],format="%Y/%m/%d %H:%M:%S")

df['Year']= df['DateTime'].dt.year
df['Month']=df['DateTime'].dt.month
df['Day']= df['DateTime'].dt.day
df['Hour']=df['DateTime'].dt.hour
df['Minute']=df['DateTime'].dt.minute
df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
df.drop(['Year','Month','Day','Hour','Minute'],axis=1,inplace=True)

heart_rate_by_day = df.groupby(['Date']).BPM.mean()
heart_df = pd.DataFrame(heart_rate_by_day)
heart_df.reset_index(inplace=True)
heart_df.to_csv("../processed_data/all_heart_rate_data.csv",index=False)

### READ SLEEP DATA IN ###
sleep_files = []
for file in files:
    if find_word(file,"sleep"):
        print(file)
        sleep_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
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
sleep_dict['sleep_end_time'] = []
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
    sleep_dict['sleep_end_time'].append(sleep_endtime)
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
df.to_csv("../processed_data/all_sleep_data.csv",index=False)

heart_sleep_df= pd.merge(heart_df, df, on="Date", how='left')


### READ RESTING HEART RATE ###
rhr_files = []
for file in files:
    if find_word(file,"resting_heart_rate"):
        print(file)
        rhr_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in rhr_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

rhr_dict = {}
rhr_dict["Date"] = []
rhr_dict["RestingBPM"] = []

for d in results:
    Date = d["dateTime"]
    RestingBPM = d["value"]["value"]
    rhr_dict['Date'].append(Date)
    rhr_dict['RestingBPM'].append(RestingBPM)
    
rh_df = pd.DataFrame(rhr_dict)
rh_df = rh_df[rh_df["RestingBPM"] != 0]
rh_df.dtypes
rh_df["Date"] = pd.to_datetime(rh_df["Date"],format="%m/%d/%y %H:%M:%S")
rh_df.sort_values(by='Date',inplace=True)
rh_df.to_csv("../processed_data/rhr_data.csv",index=False)

all_df= pd.merge(heart_sleep_df, rh_df, on="Date", how='left')

### READ CALORIES DATA ###
calories_files = []
for file in files:
    if find_word(file,"calories"):
        print(file)
        calories_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in calories_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

calories_dict = {}
calories_dict["Date"] = []
calories_dict["Calories"] = []

for d in results:
    Date = d["dateTime"]
    Calories = d["value"]
    calories_dict['Date'].append(Date)
    calories_dict['Calories'].append(Calories)
    
calories_df = pd.DataFrame(calories_dict)
calories_df.head()
calories_df["Date"] = pd.to_datetime(calories_df["Date"],format="%m/%d/%y %H:%M:%S")
calories_df.sort_values(by='Date',inplace=True)

calories_df['Year']= calories_df['Date'].dt.year
calories_df['Month']=calories_df['Date'].dt.month
calories_df['Day']= calories_df['Date'].dt.day
calories_df['YearMonthDay'] = pd.to_datetime(calories_df[['Year', 'Month', 'Day']])
calories_df['Calories'] = pd.to_numeric(calories_df['Calories'])

calories_by_day = calories_df.groupby(['YearMonthDay']).Calories.sum()
calories_df = pd.DataFrame(calories_by_day)
calories_df.reset_index(inplace=True)
calories_df.columns = ['Date','Calories']
calories_df = calories_df[(calories_df['Date'] >= '2018-09-12') 
                                  & (calories_df['Date'] <= '2019-09-05')]
calories_df.to_csv("../processed_data/calories_data.csv",index=False)

all_df2= pd.merge(all_df, calories_df, on="Date", how='left')


### READ DISTANCE DATA ###
distance_files = []
for file in files:
    if find_word(file,"distance"):
        print(file)
        distance_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in distance_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

distance_dict = {}
distance_dict["Date"] = []
distance_dict["Distance"] = []

for d in results:
    Date = d["dateTime"]
    Distance = d["value"]
    distance_dict['Date'].append(Date)
    distance_dict['Distance'].append(Distance)
    
distance_df = pd.DataFrame(distance_dict)
distance_df.head()
distance_df["Date"] = pd.to_datetime(distance_df["Date"],format="%m/%d/%y %H:%M:%S")
distance_df.sort_values(by='Date',inplace=True)

distance_df['Year']= distance_df['Date'].dt.year
distance_df['Month']=distance_df['Date'].dt.month
distance_df['Day']= distance_df['Date'].dt.day
distance_df['YearMonthDay'] = pd.to_datetime(distance_df[['Year', 'Month', 'Day']])
distance_df['Distance'] = pd.to_numeric(distance_df['Distance'])

distance_df = distance_df.groupby(['YearMonthDay']).Distance.sum()
distance_df = pd.DataFrame(distance_df)
distance_df.reset_index(inplace=True)
distance_df.columns = ['Date','Distance']
distance_df.to_csv("../processed_data/distance_data.csv",index=False)

all_df3= pd.merge(all_df2, distance_df, on="Date", how='left')

### READ STEPS DATA ###
step_files = []
for file in files:
    if find_word(file,"steps"):
        print(file)
        step_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in step_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

steps_dict = {}
steps_dict["Date"] = []
steps_dict["Steps"] = []

for d in results:
    Date = d["dateTime"]
    Steps = d["value"]
    steps_dict['Date'].append(Date)
    steps_dict['Steps'].append(Steps)
    
steps_df = pd.DataFrame(steps_dict)
steps_df.head()
steps_df["Date"] = pd.to_datetime(steps_df["Date"],format="%m/%d/%y %H:%M:%S")
steps_df.sort_values(by='Date',inplace=True)

steps_df['Year']= steps_df['Date'].dt.year
steps_df['Month']=steps_df['Date'].dt.month
steps_df['Day']= steps_df['Date'].dt.day
steps_df['YearMonthDay'] = pd.to_datetime(steps_df[['Year', 'Month', 'Day']])
steps_df['Steps'] = pd.to_numeric(steps_df['Steps'])

steps_df = steps_df.groupby(['YearMonthDay']).Steps.sum()
steps_df = pd.DataFrame(steps_df)
steps_df.reset_index(inplace=True)
steps_df.columns = ['Date','Steps']
steps_df.to_csv("../processed_data/steps_data.csv",index=False)

all_df4= pd.merge(all_df3, steps_df, on="Date", how='left')

### READ LIGHTLY ACTIVE ###
light_active_files = []
for file in files:
    if find_word(file,"lightly_active_minutes"):
        print(file)
        light_active_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in light_active_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

light_active_dict = {}
light_active_dict["Date"] = []
light_active_dict["LightActiveMinutes"] = []

for d in results:
    Date = d["dateTime"]
    Minutes = d["value"]
    light_active_dict['Date'].append(Date)
    light_active_dict['LightActiveMinutes'].append(Minutes)
    
light_active_df = pd.DataFrame(light_active_dict)
light_active_df.dtypes
light_active_df["Date"] = pd.to_datetime(rh_df["Date"],format="%m/%d/%y %H:%M:%S")
light_active_df.sort_values(by='Date',inplace=True)
light_active_df['LightActiveMinutes'] = pd.to_numeric(light_active_df['LightActiveMinutes'])
light_active_df.to_csv("../processed_data/light_active_minutes.csv",index=False)

all_df5= pd.merge(all_df4, light_active_df, on="Date", how='left')


### READ Moderately ACTIVE ###
moderate_active_files = []
for file in files:
    if find_word(file,"moderately_active_minutes"):
        print(file)
        moderate_active_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in moderate_active_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

moderate_active_dict = {}
moderate_active_dict["Date"] = []
moderate_active_dict["ModerateActiveMinutes"] = []

for d in results:
    Date = d["dateTime"]
    Minutes = d["value"]
    moderate_active_dict['Date'].append(Date)
    moderate_active_dict['ModerateActiveMinutes'].append(Minutes)
    
moderate_active_df = pd.DataFrame(moderate_active_dict)
moderate_active_df.dtypes
moderate_active_df["Date"] = pd.to_datetime(rh_df["Date"],format="%m/%d/%y %H:%M:%S")
moderate_active_df.sort_values(by='Date',inplace=True)
moderate_active_df['ModerateActiveMinutes'] = pd.to_numeric(moderate_active_df['ModerateActiveMinutes'])
moderate_active_df.to_csv("../processed_data/moderate_active_minutes.csv",index=False)

all_df6= pd.merge(all_df5, moderate_active_df, on="Date", how='left')

### READ VERY ACTIVE ###
very_active_files = []
for file in files:
    if find_word(file,"very_active_minutes"):
        print(file)
        very_active_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in very_active_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

very_active_dict = {}
very_active_dict["Date"] = []
very_active_dict["VeryActiveMinutes"] = []

for d in results:
    Date = d["dateTime"]
    Minutes = d["value"]
    very_active_dict['Date'].append(Date)
    very_active_dict['VeryActiveMinutes'].append(Minutes)
    
very_active_df = pd.DataFrame(very_active_dict)
very_active_df.dtypes
very_active_df["Date"] = pd.to_datetime(rh_df["Date"],format="%m/%d/%y %H:%M:%S")
very_active_df.sort_values(by='Date',inplace=True)
very_active_df['VeryActiveMinutes'] = pd.to_numeric(very_active_df['VeryActiveMinutes'])
very_active_df.to_csv("../processed_data/very_active_minutes.csv",index=False)

all_df7= pd.merge(all_df6, very_active_df, on="Date", how='left')

### READ SEDENTARY MINUTES###
sedentary_files = []
for file in files:
    if find_word(file,"sedentary_minutes"):
        print(file)
        sedentary_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in sedentary_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

sedentary_dict = {}
sedentary_dict["Date"] = []
sedentary_dict["SedentaryMinutes"] = []

for d in results:
    Date = d["dateTime"]
    Minutes = d["value"]
    sedentary_dict['Date'].append(Date)
    sedentary_dict['SedentaryMinutes'].append(Minutes)
    
sedentary_df = pd.DataFrame(sedentary_dict)
sedentary_df.dtypes
sedentary_df["Date"] = pd.to_datetime(rh_df["Date"],format="%m/%d/%y %H:%M:%S")
sedentary_df.sort_values(by='Date',inplace=True)
sedentary_df['SedentaryMinutes'] = pd.to_numeric(sedentary_df['SedentaryMinutes'])
sedentary_df.to_csv("../processed_data/sedentary_minutes.csv",index=False)

all_df8= pd.merge(all_df7, sedentary_df, on="Date", how='left')


### READ ALTITUDE FILES ###
altitude_files = []
for file in files:
    if find_word(file,"altitude"):
        print(file)
        altitude_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in altitude_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

altitude_dict = {}
altitude_dict["Date"] = []
altitude_dict["Altitude"] = []

for d in results:
    Date = d["dateTime"]
    Altitude = d["value"]
    altitude_dict['Date'].append(Date)
    altitude_dict['Altitude'].append(Altitude)
    
altitude_df = pd.DataFrame(altitude_dict)
altitude_df.head()
altitude_df["Date"] = pd.to_datetime(steps_df["Date"],format="%m/%d/%y %H:%M:%S")
altitude_df.sort_values(by='Date',inplace=True)

altitude_df['Year']= altitude_df['Date'].dt.year
altitude_df['Month']=altitude_df['Date'].dt.month
altitude_df['Day']= altitude_df['Date'].dt.day
altitude_df['YearMonthDay'] = pd.to_datetime(altitude_df[['Year', 'Month', 'Day']])
altitude_df['Altitude'] = pd.to_numeric(altitude_df['Altitude'])

altitude_df = altitude_df.groupby(['YearMonthDay']).Altitude.max()
altitude_df = pd.DataFrame(altitude_df)
altitude_df.reset_index(inplace=True)
altitude_df.columns = ['Date','MaxAltitude']
altitude_df.to_csv("../processed_data/altitude_data.csv",index=False)

all_df9= pd.merge(all_df8, altitude_df, on="Date", how='left')


### READ DEMOGRAPHIC Vo2 max data ###
demographic_vo2_files = []
for file in files:
    if find_word(file,"demographic_vo2_max"):
        print(file)
        demographic_vo2_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in demographic_vo2_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

demographic_vo2_dict = {}
demographic_vo2_dict["Date"] = []
demographic_vo2_dict["demographicVO2Max"] = []

for d in results:
    Date = d["dateTime"]
    DemographicV02 = d["value"]["demographicVO2Max"]
    demographic_vo2_dict['Date'].append(Date)
    demographic_vo2_dict['demographicVO2Max'].append(DemographicV02)
    
demographic_vo2_df = pd.DataFrame(demographic_vo2_dict)
demographic_vo2_df.dtypes
demographic_vo2_df["Date"] = pd.to_datetime(demographic_vo2_df["Date"],format="%m/%d/%y %H:%M:%S")
demographic_vo2_df.sort_values(by='Date',inplace=True)
demographic_vo2_df.to_csv("../processed_data/demographic_vo2.csv",index=False)

all_df10= pd.merge(all_df9, demographic_vo2_df, on="Date", how='left')

### READ HEART RATE ZONES ### 
hrz_files = []
for file in files:
    if find_word(file,"time_in_heart_rate_zones"):
        print(file)
        hrz_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in hrz_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

hrz_dict = {}
hrz_dict["Date"] = []
hrz_dict["BELOW_DEFAULT_ZONE_1"] = []
hrz_dict["IN_DEFAULT_ZONE_1"] = []
hrz_dict["IN_DEFAULT_ZONE_2"] = []
hrz_dict["IN_DEFAULT_ZONE_3"] = []

for d in results:
    Date = d["dateTime"]
    BELOW_DEFAULT_ZONE_1 = d['value']['valuesInZones']['BELOW_DEFAULT_ZONE_1']
    IN_DEFAULT_ZONE_1 = d['value']['valuesInZones']['IN_DEFAULT_ZONE_1']
    IN_DEFAULT_ZONE_2 = d['value']['valuesInZones']['IN_DEFAULT_ZONE_2']
    IN_DEFAULT_ZONE_3 = d['value']['valuesInZones']['IN_DEFAULT_ZONE_3']
    hrz_dict['Date'].append(Date)
    hrz_dict['BELOW_DEFAULT_ZONE_1'].append(BELOW_DEFAULT_ZONE_1)
    hrz_dict['IN_DEFAULT_ZONE_1'].append(IN_DEFAULT_ZONE_1)
    hrz_dict['IN_DEFAULT_ZONE_2'].append(IN_DEFAULT_ZONE_2)
    hrz_dict['IN_DEFAULT_ZONE_3'].append(IN_DEFAULT_ZONE_3)

hrz_df = pd.DataFrame(hrz_dict)
hrz_df.dtypes
hrz_df["Date"] = pd.to_datetime(hrz_df["Date"],format="%m/%d/%y %H:%M:%S")
hrz_df.sort_values(by='Date',inplace=True)
hrz_df.to_csv("../processed_data/heart_rate_zone_minutes.csv",index=False)

all_df11= pd.merge(all_df10, hrz_df, on="Date", how='left')


### READ DEMOGRAPHIC Vo2 max data ###
demographic_vo2_files = []
for file in files:
    if find_word(file,"demographic_vo2_max"):
        print(file)
        demographic_vo2_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in demographic_vo2_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

demographic_vo2_dict = {}
demographic_vo2_dict["Date"] = []
demographic_vo2_dict["demographicVO2Max"] = []

for d in results:
    Date = d["dateTime"]
    DemographicV02 = d["value"]["demographicVO2Max"]
    demographic_vo2_dict['Date'].append(Date)
    demographic_vo2_dict['demographicVO2Max'].append(DemographicV02)
    
demographic_vo2_df = pd.DataFrame(demographic_vo2_dict)
demographic_vo2_df.dtypes
demographic_vo2_df["Date"] = pd.to_datetime(demographic_vo2_df["Date"],format="%m/%d/%y %H:%M:%S")
demographic_vo2_df.sort_values(by='Date',inplace=True)
demographic_vo2_df.to_csv("../processed_data/demographic_vo2.csv",index=False)

all_df10= pd.merge(all_df9, demographic_vo2_df, on="Date", how='left')

### READ EXERISES ### 
exercise_files = []
for file in files:
    if find_word(file,"exercise"):
        print(file)
        exercise_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in exercise_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

exercise_dict = {}
exercise_dict["ExerciseDate"] = []
exercise_dict["ExerciseActivityName"] = []
exercise_dict["ExerciseActiveDuration"] = []
exercise_dict["ExerciseAverageHeartRate"] = []
exercise_dict["ExerciseCalories"] = []
exercise_dict["ExerciseDuration"] = []
exercise_dict["ExerciseElevationGain"] = []
exercise_dict["ExerciseDuration"] = []
exercise_dict["ExerciseSteps"] = []
exercise_dict["ExerciseSedentaryMinutes"] = []
exercise_dict["ExerciseLightMinutes"] = []
exercise_dict["ExerciseFairlyActiveMinutes"] = []
exercise_dict["ExerciseVeryActiveMinutes"] = []
exercise_dict["ExerciseOutOfRangeMaxHR"] = []
exercise_dict["ExerciseOutOfRangeMinHR"] = []
exercise_dict["ExerciseOutOfRangeMinutes"] = []
exercise_dict["ExerciseFatBurnMaxHR"] = []
exercise_dict["ExerciseFatBurnMinHR"] = []
exercise_dict["ExerciseFatBurnMinutes"] = []
exercise_dict["ExerciseCardioMaxHR"] = []
exercise_dict["ExerciseCardioMinHR"] = []
exercise_dict["ExerciseCardioMinutes"] = []
exercise_dict["ExercisePeakMaxHR"] = []
exercise_dict["ExercisePeakMinHR"] = []
exercise_dict["ExercisePeakMinutes"] = []
exercise_dict["Speed"] = []
exercise_dict["Pace"] = []
exercise_dict["ExerciseDistance"] = []

for d in results:
       ExerciseDate = d["startTime"]
       ExerciseActivityName = d["activityName"]
       ExerciseActiveDuration= d["activeDuration"]
       try:
           ExerciseAverageHeartRate= d["averageHeartRate"]
       except:
           ExerciseAverageHeartRate = 0
       ExerciseCalories = d["calories"]
       ExerciseDuration = d["duration"]
       try:
           ExerciseElevationGain= d["elevationGain"]
       except:
          ExerciseElevationGain = 0
       try:
           ExerciseSteps = d["steps"]
       except:
           ExerciseSteps = 0
       try:
           Speed = d["speed"] 
       except:
           Speed = 0
       try:
           Pace = d["pace"]
       except:
           Pace = 0
       try:
           ExerciseDistance = d["distance"]
       except:
           ExerciseDistance = 0
       ExerciseSedentaryMinutes = d["activityLevel"][0]["minutes"]
       ExerciseLightMinutes = d["activityLevel"][1]["minutes"]
       ExerciseFairlyActiveMinutes = d["activityLevel"][2]["minutes"]
       ExerciseVeryActiveMinutes = d["activityLevel"][3]["minutes"]
       try:
           ExerciseOutOfRangeMaxHR = d["heartRateZones"][0]["max"]
       except:
           ExerciseOutOfRangeMaxHR = 0
       try:
           ExerciseOutOfRangeMinHR = d["heartRateZones"][0]["min"]
       except:
           ExerciseOutOfRangeMinHR = 0
       try:
           ExerciseOutOfRangeMinutes = d["heartRateZones"][0]["minutes"]
       except:
           ExerciseOutOfRangeMinutes = 0
       try: 
           ExerciseFatBurnMaxHR = d["heartRateZones"][1]["max"]
       except: 
           ExerciseFatBurnMaxHR = 0
       try:
           ExerciseFatBurnMinHR = d["heartRateZones"][1]["min"]
       except:
           ExerciseFatBurnMinHR = 0
       try:
           ExerciseFatBurnMinutes = d["heartRateZones"][1]["minutes"]
       except:
           ExerciseFatBurnMinutes = 0
       try: 
           ExerciseCardioMaxHR = d["heartRateZones"][2]["max"]
       except:    
           ExerciseCardioMaxHR = 0
       try: 
           ExerciseCardioMinHR = d["heartRateZones"][2]["min"]
       except:
           ExerciseCardioMinHR = 0
       try: 
           ExerciseCardioMinutes = d["heartRateZones"][2]["minutes"]
       except:
           ExerciseCardioMinutes = 0
       try: 
           ExercisePeakMaxHR = d["heartRateZones"][3]["max"]
       except:
           ExercisePeakMaxHR = 0
       try: 
           ExercisePeakMinHR = d["heartRateZones"][3]["min"]
       except:
           ExercisePeakMinHR = 0
       try:
           ExercisePeakMinutes = d["heartRateZones"][3]["minutes"]
       except:
           ExercisePeakMinutes = 0
       ##Add to dictionary
       exercise_dict["ExerciseDate"].append(ExerciseDate)
       exercise_dict["ExerciseActivityName"].append(ExerciseActivityName)
       exercise_dict["ExerciseActiveDuration"].append(ExerciseActiveDuration)
       exercise_dict["ExerciseAverageHeartRate"].append(ExerciseAverageHeartRate)
       exercise_dict["ExerciseCalories"].append(ExerciseCalories)
       exercise_dict["ExerciseElevationGain"].append(ExerciseElevationGain)
       exercise_dict["ExerciseDuration"].append(ExerciseDuration)
       exercise_dict["ExerciseSteps"].append(ExerciseSteps)
       exercise_dict["ExerciseSedentaryMinutes"].append(ExerciseSedentaryMinutes)
       exercise_dict["ExerciseLightMinutes"].append(ExerciseLightMinutes)
       exercise_dict["ExerciseFairlyActiveMinutes"].append(ExerciseFairlyActiveMinutes)
       exercise_dict["ExerciseVeryActiveMinutes"].append(ExerciseVeryActiveMinutes)
       exercise_dict["ExerciseOutOfRangeMaxHR"].append(ExerciseOutOfRangeMaxHR)
       exercise_dict["ExerciseOutOfRangeMinHR"].append(ExerciseOutOfRangeMinHR)
       exercise_dict["ExerciseOutOfRangeMinutes"].append(ExerciseOutOfRangeMinutes)
       exercise_dict["ExerciseFatBurnMaxHR"].append(ExerciseFatBurnMaxHR)
       exercise_dict["ExerciseFatBurnMinHR"].append(ExerciseFatBurnMinHR)
       exercise_dict["ExerciseFatBurnMinutes"].append(ExerciseFatBurnMinutes)
       exercise_dict["ExerciseCardioMaxHR"].append(ExerciseCardioMaxHR)
       exercise_dict["ExerciseCardioMinHR"].append(ExerciseCardioMinHR)
       exercise_dict["ExerciseCardioMinutes"].append(ExerciseCardioMinutes)
       exercise_dict["ExercisePeakMaxHR"].append(ExercisePeakMaxHR)
       exercise_dict["ExercisePeakMinHR"].append(ExercisePeakMinHR)
       exercise_dict["ExercisePeakMinutes"].append(ExercisePeakMinutes)
       exercise_dict["Speed"].append(Speed)
       exercise_dict["Pace"].append(Pace)
       exercise_dict["ExerciseDistance"].append(ExerciseDistance)
       
exercise_df = pd.DataFrame(exercise_dict)
exercise_df.dtypes
exercise_df["ExerciseDate"] = pd.to_datetime(exercise_df["ExerciseDate"],format="%m/%d/%y %H:%M:%S")
exercise_df.sort_values(by='ExerciseDate',inplace=True)

exercise_df['Year']= exercise_df['ExerciseDate'].dt.year
exercise_df['Month']=exercise_df['ExerciseDate'].dt.month
exercise_df['Day']= exercise_df['ExerciseDate'].dt.day
exercise_df['YearMonthDay'] = pd.to_datetime(exercise_df[['Year', 'Month', 'Day']])
exercise_df.to_csv("../processed_data/exercise_data.csv",index=False)

all_df12= pd.merge(all_df11, exercise_df, left_on="Date", right_on="YearMonthDay", how='left')
all_df12.drop(["Year","Month","Day","YearMonthDay"],inplace=True,axis = 1)

### READ Run Vo2 max data ###
run_vo2_files = []
for file in files:
    if find_word(file,"run_vo2_max"):
        print(file)
        run_vo2_files.append(file)
        
results = []
with open("../processed_data/result.json", "w") as outfile:
    for file in run_vo2_files:
        name = "../data" + "/" + file
        with open(name, 'rb') as infile:
            file_data = json.load(infile)
            results += file_data
    json.dump(results, outfile)

run_vo2_dict = {}
run_vo2_dict["Date"] = []
run_vo2_dict["runVO2Max"] = []

for d in results:
    Date = d["dateTime"]
    RunV02max = d["value"]["runVO2Max"]
    run_vo2_dict['Date'].append(Date)
    run_vo2_dict['runVO2Max'].append(RunV02max)
    
run_vo2_df = pd.DataFrame(run_vo2_dict)
run_vo2_df.dtypes
run_vo2_df["Date"] = pd.to_datetime(run_vo2_df["Date"],format="%m/%d/%y %H:%M:%S")
run_vo2_df.sort_values(by='Date',inplace=True)

run_vo2_df.to_csv("../processed_data/run_vo2.csv",index=False)

# Read sleep score data in
sleep_score_df = pd.read_csv("../data/sleep_score.csv")
sleep_score_df["timestamp"] = pd.to_datetime(sleep_score_df["timestamp"])

sleep_score_df['Year']= sleep_score_df['timestamp'].dt.year
sleep_score_df['Month']=sleep_score_df['timestamp'].dt.month
sleep_score_df['Day']= sleep_score_df['timestamp'].dt.day

sleep_score_df['YearMonthDay'] = pd.to_datetime(sleep_score_df[['Year', 'Month', 'Day']])
sleep_score_df = sleep_score_df[['YearMonthDay', 'overall_score', 'composition_score',
       'revitalization_score', 'duration_score', 'deep_sleep_in_minutes',
       'resting_heart_rate', 'restlessness']]

# Create final dataframe
all_df13= pd.merge(all_df12, run_vo2_df, left_on="ExerciseDate", right_on="Date", how='left')
all_df13.drop(["Date_y"],axis=1,inplace=True)
all_df13.rename(columns= {"Date_x":"Date"},inplace=True)

final_df = pd.merge(all_df13,sleep_score_df,left_on="Date",right_on="YearMonthDay",how="left")
final_df.dtypes
final_df.columns

final_df = final_df[['Date', 'BPM', 'RestingBPM','sleep_duration', 'sleep_efficiency', 'sleep_start_time',
       'sleep_end_time', 'minutes_after_wakeup', 'minutes_asleep',
       'minutes_awake', 'minutes_to_fall_asleep', 'time_in_bed', 'deep_sleep',
       'rem_sleep', 'wake_sleep', 'light_sleep', 'Calories',
       'Distance', 'Steps', 'LightActiveMinutes', 'ModerateActiveMinutes',
       'VeryActiveMinutes', 'SedentaryMinutes', 'MaxAltitude',
       'demographicVO2Max', 'BELOW_DEFAULT_ZONE_1', 'IN_DEFAULT_ZONE_1',
       'IN_DEFAULT_ZONE_2', 'IN_DEFAULT_ZONE_3', 'ExerciseDate',
       'ExerciseActivityName', 'ExerciseActiveDuration',
       'ExerciseAverageHeartRate', 'ExerciseCalories', 'ExerciseDuration',
       'ExerciseElevationGain', 'ExerciseSteps', 'ExerciseSedentaryMinutes',
       'ExerciseLightMinutes', 'ExerciseFairlyActiveMinutes',
       'ExerciseVeryActiveMinutes', 'ExerciseOutOfRangeMaxHR',
       'ExerciseOutOfRangeMinHR', 'ExerciseOutOfRangeMinutes',
       'ExerciseFatBurnMaxHR', 'ExerciseFatBurnMinHR',
       'ExerciseFatBurnMinutes', 'ExerciseCardioMaxHR', 'ExerciseCardioMinHR',
       'ExerciseCardioMinutes', 'ExercisePeakMaxHR', 'ExercisePeakMinHR',
       'ExercisePeakMinutes', 'Speed', 'Pace', 'ExerciseDistance',
       'runVO2Max','overall_score', 'composition_score',
       'revitalization_score', 'duration_score', 'deep_sleep_in_minutes',
       'resting_heart_rate', 'restlessness']]

final_df.to_csv("../processed_data/final_dataset_12012019.csv",index=False)
