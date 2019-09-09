#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 19:21:23 2019

@author: geoffrey.kip
"""
import pandas as pd
import statsmodels.api as sm
import numpy as np

df = pd.read_csv("../processed_data/final_dataset_09082019.csv")
df.columns
df.dtypes
df.describe()

#Create new columns
df["Date"] = pd.to_datetime(df["Date"],format="%Y/%m/%d %H:%M:%S")
df['Year']= df['Date'].dt.year
df['Month']=df['Date'].dt.month
df['Day']= df['Date'].dt.day
df['Hour']=df['Date'].dt.hour
df['Minute']=df['Date'].dt.minute
df['day_of_week'] = df['Date'].dt.day_name()

#Sleep time 
df["sleep_start_time"] = pd.to_datetime(df["sleep_start_time"],format="%Y/%m/%d %H:%M:%S")
df['SleepDay']= df['sleep_start_time'].dt.day
df['SleepHour']=df['sleep_start_time'].dt.hour
df['SleepMinute']=df['sleep_start_time'].dt.minute

#Calculate exercise column. Walks dont count
df['exercise'] = np.where(df['ExerciseDate'].notnull() & ~df['ExerciseActivityName'].isin(['Walk']),1,0)
df['sleep_before_12'] = np.where(df['SleepHour'].isin([21,22,23]),1,0)

# Calculate time columns as hours
df['ExerciseDuration'] = df['ExerciseDuration']/3600000
df['time_in_bed'] = df['time_in_bed']/60

#Exploratory analysis 
df['BPM'].hist()
df['BPM'].mean()

df['RestingBPM'].hist()
df['RestingBPM'].mean()

df['Calories'].hist()
df['Calories'].mean()

df['Steps'].hist()
df['Steps'].mean()

df['sleep_duration'].hist()
df['sleep_duration'].mean()

df['rem_sleep'].hist()
df['rem_sleep'].mean()

df['deep_sleep'].hist()
df['deep_sleep'].mean()

df['time_in_bed'].hist()
df['time_in_bed'].mean()

df['ExerciseDuration'].hist()
df['ExerciseDuration'].mean()

df['ExerciseCalories'].hist()
df['ExerciseCalories'].mean()

df['ExerciseAverageHeartRate'].hist()
df['ExerciseAverageHeartRate'].mean()

df['ExerciseVeryActiveMinutes'].hist()
df['ExerciseVeryActiveMinutes'].mean()

df.boxplot(column=['runVO2Max','demographicVO2Max'])

active_months= df.groupby(['Month']).ExerciseVeryActiveMinutes.mean().reset_index().sort_values(by="ExerciseVeryActiveMinutes",ascending=False)
active_days = df.groupby(['day_of_week']).ExerciseVeryActiveMinutes.mean().reset_index().sort_values(by="ExerciseVeryActiveMinutes",ascending=False)

rhr_months= df.groupby(['Month']).RestingBPM.mean().reset_index().sort_values(by="RestingBPM",ascending=False)
rhr_days= df.groupby(['day_of_week']).RestingBPM.mean().reset_index().sort_values(by="RestingBPM",ascending=False)
rhr_days.plot(x="day_of_week",y="RestingBPM",kind="bar")


sleep_months= df.groupby(['Month']).sleep_duration.mean().reset_index().sort_values(by="sleep_duration",ascending=False)
sleep_days= df.groupby(['day_of_week']).sleep_duration.mean().reset_index().sort_values(by="sleep_duration",ascending=False)

sleep_days.plot(x="day_of_week",y="sleep_duration",kind="bar")

calorie_months= df.groupby(['Month']).Calories.mean().reset_index().sort_values(by="Calories",ascending=False)
calorie_days= df.groupby(['day_of_week']).Calories.mean().reset_index().sort_values(by="Calories",ascending=False)

calorie_days.plot(x="day_of_week",y="Calories",kind="bar")

step_months= df.groupby(['Month']).Steps.mean().reset_index().sort_values(by="Steps",ascending=False)
step_days= df.groupby(['day_of_week']).Steps.mean().reset_index().sort_values(by="Steps",ascending=False)

step_days.plot(x="day_of_week",y="Steps",kind="bar")


# Recode outcome variables to binary for model
# Look at next day outcomes to try to infer if there is a causal effect
df['next_day_calories'] = df['Calories'].shift(-1)
df['next_day_active_minutes'] = df['VeryActiveMinutes'].shift(-1)
df['next_day_steps'] = df['Steps'].shift(-1)
df['next_day_exercise'] = df['exercise'].shift(-1)
df['next_day_rhr'] = df['RestingBPM'].shift(-1)



df["calories_goal_met"]= np.where(df["next_day_calories"] >= 3000,1,0)
df["active_minutes_goal_met"] = np.where(df["next_day_active_minutes"] >= 60,1,0)
df["step_goal_met"] = np.where(df["next_day_steps"] >= 7500,1,0)
df["sleep_ge_seven_hours"] = np.where(df["sleep_duration"] >= 7,1,0)

df.to_csv("../processed_data/statistical_dataset.csv",index=False)