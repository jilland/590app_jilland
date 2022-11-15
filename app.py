from flask import Flask, render_template, url_for, jsonify, request
from pymongo import MongoClient
from gatherData import *
import json
import datetime
import requests
import random
import certifi


#Jillian Anderson PID 730368080
#September 7 2022 - COMP 590

client = MongoClient("mongodb+srv://compuser:user@cluster0.6lmeybw.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client["mydb"]

currentDate = format(datetime.date.today())

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    userName = get_name()
    return jsonify(userName)

@app.route("/heartrate/last", methods=["GET"])
def heartrate_report():
    heartrate = get_heartrate()
    return jsonify(heartrate)

@app.route("/steps/last", methods=["GET"])
def steps_report():
    steps = get_steps()
    return jsonify(steps)

@app.route("/sleep/<date>", methods=["GET"])
def sleep_report(date):
    sleep = get_sleep(date)
    return jsonify(sleep)

@app.route("/activity/<date>", methods=["GET"])
def activity_report(date):
    activity = get_activeness(date)
    return jsonify(activity)


@app.route("/sensors/env", methods=["GET"])
def get_env():
    rows = db.env.find({})
    envDict = {}
    envDict.update({})
    for row in rows:
        envDict:dict
        envDict.update(row)
    del envDict['_id']
    return jsonify(envDict)

@app.route("/sensors/pose", methods=["GET"])
def get_pose():
    rows = db.pose.find({})
    poseDict = {}
    poseDict.update({})

    for row in rows:
        poseDict:dict
        poseDict.update(row)

    del poseDict['_id']
    return jsonify(poseDict)


@app.route("/post/env", methods=["POST"])
def post_env():
    input = request.get_json()
    tempVal = input['temp']
    humidityVal = input['humidity']
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)
    postEnvStr = {'temp':tempVal, 'humidity':humidityVal, 'timestamp':timestamp}
    db.env.insert_one(postEnvStr)
    today = {
        'data' : jsonify(str(postEnvStr))
    }
    return jsonify(str(postEnvStr))

@app.route("/post/pose", methods=["POST"])
def post_pose():
    input = request.get_json()
    presenceVal = input['prescence']
    poseVal = input['pose']
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)
    postPoseStr = {'presence':presenceVal, 'pose':poseVal, 'timestamp':timestamp}
    db.pose.insert_one(postPoseStr)
    today = {
        'data' : jsonify(str(postPoseStr))
    }
    return jsonify(str(postPoseStr))

if __name__ == '__main__':
    app.run(debug=True)
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
