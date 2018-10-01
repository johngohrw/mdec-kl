import os
import argparse as ap

from flask import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as database

import cv2
from PIL import Image
import pytesseract

from mqtt_client import MQTTClient
from camera import VideoCamera

import sys
sys.path.append("IP/SecurityCamera");
import ccCameraSplit as ccS

app = Flask(__name__);

global firebaseApp;
global firebaseDB;
global dbPush;
global lightEventsRef;
global carEventsRef;
global mqttClient;
global LED_HIGH;
global LED_LOW;

def main():
    # All things global should be defined here
    global firebaseApp;
    global firebaseDB;
    global lightEventsRef;
    global carEventsRef;
    global mqttClient;
    global LED_HIGH;
    global LED_LOW;
    cred = credentials.Certificate("mdec-5edc2-firebase-adminsdk-vg9vm-9c5355fe8e.json");
    firebaseApp = firebase_admin.initialize_app(cred);
    firebaseDB = database;
    databaseURL = "https://mdec-5edc2.firebaseio.com/";
    lightEventsRef = database.reference("light/lightEvents", firebaseApp, databaseURL);
    carEventsRef = database.reference("car/carEvents", firebaseApp, databaseURL);

    mqttClient = MQTTClient();
    LED_HIGH = "D1";
    LED_LOW = "D2";


def isCapitalized(c):
    return ord(c) >= 65 and ord(c) <= 90;


def isDigit(c):
    return ord(c) >= 48 and ord(c) <= 57;


def signalCallback(signal, datetimeStr):
    time, date = datetimeStr.split(" ");

    intensity = "100%" if signal == 1 else "50%";
    causeOfMotion = "Vehicle" if signal == 1 else "null";
    lightData = { "Date": date, "Time": time, "Log": 444, "Light_ID": "L15", "Light_intensity": intensity, "Caused_by_motion": "null", "Energy_type": "Brown"};

    if dbPush:
        lightEventsRef.push(lightData);

    if signal == 0:
        mqttClient.publishData(LED_LOW);
    else:
        mqttClient.publishData(LED_HIGH);

    data = { "Date": date, "Time": time, "Log": 400, "Event": "Motion"};
    print("Callback detected: ");
    print(signal);

    if dbPush:
        carEventsRef.push(data);


def genFrame(camera):
    mdEnt = ccS.MDEntity(signalCallback);
    while True:
        frame = camera.get_frame();
        message = mdEnt.processImage(frame);
        cv2.putText(frame, "Obs: {}".format(message), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        _, jpeg = cv2.imencode('.jpg', frame);

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n');


@app.route("/")
def entranceExitDetection():
    # FIXME: Hardcoded Image path
    currentDir = os.path.dirname(os.path.realpath(__file__));
    imgPath = os.path.join(currentDir, "IP/carNumberPlate.jpg");
    img = cv2.imread(imgPath);
    cv2.imshow("Image", img);
    cv2.waitKey(1);

    config = ("-l eng --oem 1 --psm 6");
    result = pytesseract.image_to_string(Image.open(imgPath), config=config);
    carPlateNum = "";
    for c in result:
        if isCapitalized(c) or isDigit(c):
            carPlateNum += c;

    mqttClient.publishData(LED_HIGH);

    data = { "Date": "22-09-2018", "Time": "08:22:08", "Log": 319, "Carplate": "WPR9070", "Event": "Entry"};
    data["Carplate"] = carPlateNum;
    carEventsRef.push(data);

    return "";


@app.route("/live_test")
def livestream_page():
    return render_template('index.html');


@app.route("/car_test")
def carvideo_page():
    return render_template('car.html');


@app.route("/motion")
def analyse_footage():
    return Response(genFrame(VideoCamera()),
            mimetype='multipart/x-mixed-replace; boundary=frame');


@app.route("/car_video")
def analyse_car_video():
    currentDir = os.path.dirname(os.path.realpath(__file__));
    videoPath = os.path.join(currentDir, "IP/SecurityCamera/basementFootage.mp4");
    return Response(genFrame(VideoCamera(videoPath)),
            mimetype='multipart/x-mixed-replace; boundary=frame');


@app.route("/test")
def test():
    currentDir = os.path.dirname(os.path.realpath(__file__));
    filePath = os.path.join(currentDir, "lippy/json_data.txt");
    with open(filePath, "r") as lipFile:
        for Json in lipFile:
            current = Json.rstrip();
            dic = json.loads(current);
            try:
                dic["Event"];
                carEventsRef.push(dic);
            except KeyError:
                lightEventsRef.push(dic);

    return "";


@app.route("/firebase_db", methods=["DELETE"])
def clear_db():
    carEventsRef.delete();
    lightEventsRef.delete();
    return "", 204;


@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404;


@app.errorhandler(405)
def method_not_allowed(error):
    return "405 METHOD NOT ALLOWED", 405


if __name__ == "__main__":
    global dbPush;
    parser = ap.ArgumentParser();
    parser.add_argument("-m", type=int, default=1, help="To push(1) or not to push(0) to Firebase DB");
    args = parser.parse_args();
    dbPush = args.m;

    main();
    app.run();

