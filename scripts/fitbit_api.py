import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime
import os

# Authenticate to fitbit api
CLIENT_ID = os.environ['FITBIT_CLIENT_ID']
CLIENT_SECRET = os.environ['FITBIT_CLIENT_SECRET']

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

#Get resting heart rate by day
startTime = pd.datetime(year = 2020, month = 3, day = 25)
endTime = pd.datetime.today().date() - datetime.timedelta(days=1)

time_list = []
rhr_list = []
df_list = []
allDates = pd.date_range(start=startTime, end = endTime)

for oneDate in allDates:
    oneDate = oneDate.date().strftime("%Y-%m-%d")
    oneDayData = auth2_client.intraday_time_series('activities/heart', base_date=oneDate, detail_level='1sec')
    #print(oneDayData)
    rhr_list.append(oneDayData['activities-heart'][0]['value']['restingHeartRate'])
    time_list.append(oneDayData['activities-heart'][0]['dateTime'])
    df = pd.DataFrame({'Time':time_list, 'Heart Rate':rhr_list})    

    
df.to_csv('../processed_data/heart'+ \
               str(startTime)+'.csv', \
               columns=['Time','Heart Rate'], header=True, \
               index = False)

"""Sleep data on the night of ...."""
fit_statsSl = auth2_client.sleep(date='today')
stime_list = []
sval_list = []
for i in fit_statsSl['sleep'][0]['minuteData']:
    stime_list.append(i['dateTime'])
    sval_list.append(i['value'])
sleepdf = pd.DataFrame({'State':sval_list,
                     'Time':stime_list})
sleepdf['Interpreted'] = sleepdf['State'].map({'2':'Awake','3':'Very Awake','1':'Asleep'})
sleepdf.to_csv('../processed_data/sleep' + \
               today+'.csv', \
               columns = ['Time','State','Interpreted'],header=True,
               index = False)


"""Sleep Summary on the night of ...."""
fit_statsSum = auth2_client.sleep(date='today')['sleep'][0]
ssummarydf = pd.DataFrame({'Date':fit_statsSum['dateOfSleep'],
                'MainSleep':fit_statsSum['isMainSleep'],
               'Efficiency':fit_statsSum['efficiency'],
               'Duration':fit_statsSum['duration'],
               'Minutes Asleep':fit_statsSum['minutesAsleep'],
               'Minutes Awake':fit_statsSum['minutesAwake'],
               'Awakenings':fit_statsSum['awakeCount'],
               'Restless Count':fit_statsSum['restlessCount'],
               'Restless Duration':fit_statsSum['restlessDuration'],
               'Time in Bed':fit_statsSum['timeInBed']
                        } ,index=[0])
