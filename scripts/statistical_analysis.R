setwd("~/Projects/fitbit")

df = read.csv("processed_data/statistical_dataset.csv")
str(df)

df$day_of_week <- relevel(df$day_of_week, ref = "Monday")

## Fit General linear models to see the influence of sleep on meeting step, active minutes and calorie goals
step_model <- glm(step_goal_met ~ sleep_ge_seven_hours + day_of_week, data = df, family = "binomial")
summary(step_model)
exp(cbind(OR = coef(step_model), confint(step_model)))

active_minutes_model <- glm(active_minutes_goal_met ~ sleep_ge_seven_hours + day_of_week, data = df, family = "binomial")
summary(active_minutes_model)
exp(cbind(OR = coef(active_minutes_model), confint(active_minutes_model)))

calories_model <- glm(calories_goal_met ~ sleep_ge_seven_hours + day_of_week, data = df, family = "binomial")
summary(calories_model)
exp(cbind(OR = coef(calories_model), confint(calories_model)))

exercise_model <- glm(next_day_exercise ~ sleep_ge_seven_hours + day_of_week, data = df, family = "binomial")
summary(exercise_model)
exp(cbind(OR = coef(exercise_model), confint(exercise_model)))

