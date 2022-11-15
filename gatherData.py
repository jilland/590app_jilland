import requests
import datetime

authKey = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSTUIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk2MDE4LCJpYXQiOjE2NjA3NjAwMTh9.Ud4qSIXGglbXaYeK-JDzL9GolEskKk9aCGrl79NMDY4"
authKey2 = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRWVkiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjg2NTkwLCJpYXQiOjE2NjA3NTA1OTB9.X-idXVjUcvSECA5jZTWoLf5yWdxr2wSAa7Z3KaKbg68"
header = {'Accept' : 'application/json', 'Authorization' : 'Bearer {}'.format(authKey)}

currentDate = format(datetime.date.today())

def get_name():
    profileURL = "https://api.fitbit.com/1/user/-/profile.json"
    nameResp = requests.get(profileURL, headers=header).json()
    userName = nameResp['user']['fullName']
    return userName

def get_time():
    return datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
    
def mins_to_hours(val):
    hrsSlept = format(val // 60)
    remMins = format(val % 60)
    durationStr = val + " hours and " + remMins + " minutes"
    return durationStr

def mins_to_hours(val):
    hrsSlept = format(val // 60)
    remMins = format(val % 60)
    durationStr = hrsSlept + " hours and " + remMins + " minutes"
    return durationStr

def get_heartrate():
    heartRateURL = "https://api.fitbit.com/1/user/-/activities/heart/date/" + currentDate + "/1d/1min.json"
    heartRateResp = requests.get(heartRateURL, headers=header).json()
    hr = format(heartRateResp['activities-heart-intraday']['dataset'][-1]['value'])
    hrTime = datetime.datetime.strptime(heartRateResp['activities-heart-intraday']['dataset'][-1]['time'],'%H:%M:%S') 
    
    now = get_time()
    offset = now - hrTime
    offsetStr:str = str(offset - datetime.timedelta(0,14400,0))
    
    heartStr = {'heart-rate': hr, 'time offset': offsetStr}
    return heartStr

def get_steps():
    stepsURL = "https://api.fitbit.com/1/user/-/activities/date/" + currentDate + ".json"
    stepsTimeURL = "https://api.fitbit.com/1/user/-/activities/steps/date/today/1d/1min.json"
    #distURL = "https://api.fitbit.com/1/user/-/activities/distance/date/" + currentDate + "/1d/1min.json"
    distURL = "https://api.fitbit.com/1/user/-/activities/list.json"
    stepsResp = requests.get(stepsURL, headers=header).json()
    stepsTimeResp = requests.get(stepsTimeURL, headers=header).json()
    distResp = requests.get(stepsURL, headers=header).json()


    steps = format(stepsResp['summary']['steps'])
    dist = format(distResp['summary']['distances'][0]['distance'])
    stepsTime = datetime.datetime.strptime(stepsTimeResp["activities-steps-intraday"]["dataset"][-1]["time"], '%H:%M:%S')
    
    now = get_time()
    offset = now - stepsTime
    offsetStr:str = str(offset - datetime.timedelta(0,14400,0))
    
    stepsStr = {'step-count': steps, 'distance': dist, 'time offset': offsetStr}
    return stepsStr

def get_sleep(date):
    sleepURL = "https://api.fitbit.com/1.2/user/-/sleep/date/" + date + ".json"
    sleepResp = requests.get(sleepURL, headers=header).json()
    #sleepDur = mins_to_hours(sleepMins)
    noDataStr = "Nothing recorded on given day."

    try:
        awake = sleepResp["summary"]["stages"]["wake"]
        lightSleep = sleepResp["summary"]["stages"]["light"]
        deepSleep = sleepResp["summary"]["stages"]["deep"]
        remSleep = sleepResp["summary"]["stages"]["rem"]
    except:
        return noDataStr

    sleepStr = {'deep': deepSleep, 'light': lightSleep, 'rem': remSleep, 'wake': awake}
    return sleepStr

def get_activeness(date):
    activeURL = "https://api.fitbit.com/1/user/-/activities/date/" + date + ".json"
    activeResp = requests.get(activeURL, headers=header).json()
    act = activeResp['summary']
    sedMins = act['sedentaryMinutes']
    lightMins = act['lightlyActiveMinutes']
    veryMins = act['veryActiveMinutes']

    #sedDur = mins_to_hours(sedMins)
    #lightDur = mins_to_hours(lightMins)
    #veryDur = mins_to_hours(veryMins)

    activeStr = {'very-active': veryMins, 'lightly-active': lightMins, 'sedentary': sedMins}
    return activeStr
