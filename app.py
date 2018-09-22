import os

from flask import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as database

import cv2
from PIL import Image
import pytesseract


app = Flask(__name__);

global firebaseApp;
global firebaseDB;
global lightEventsRef;
global carEventsRef;

def main():
    # All things global should be defined here
    global firebaseApp;
    global firebaseDB;
    global lightEventsRef;
    global carEventsRef;
    cred = credentials.Certificate("mdec-5edc2-firebase-adminsdk-vg9vm-9c5355fe8e.json");
    firebaseApp = firebase_admin.initialize_app(cred);
    firebaseDB = database;
    databaseURL = "https://mdec-5edc2.firebaseio.com/";
    lightEventsRef = database.reference("light/lightEvents", firebaseApp, databaseURL);
    carEventsRef = database.reference("car/carEvents", firebaseApp, databaseURL);


def isCapitalized(c):
    return ord(c) >= 65 and ord(c) <= 90;


def isDigit(c):
    return ord(c) >= 48 and ord(c) <= 57;


@app.route("/")
def hello_world():
    # FIXME: Hardcoded Image path
    currentDir = os.path.dirname(os.path.realpath(__file__));
    imgPath = os.path.join(currentDir, "IP/carNumberPlate.jpg");
    config = ("-l eng --oem 1 --psm 6");
    result = pytesseract.image_to_string(Image.open(imgPath), config=config);
    carPlateNum = "";
    for c in result:
        if isCapitalized(c) or isDigit(c):
            carPlateNum += c;

    data = { "date": "22-09-2018", "time": "08:22:08", "Log": 319, "Carplate": "WPR9070", "Event": "Entry"};
    data["Carplate"] = carPlateNum;
    carEventsRef.push(data);

    return "Hello";


@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404;


@app.errorhandler(405)
def method_not_allowed(error):
    return "405 METHOD NOT ALLOWED", 405


if __name__ == "__main__":
    main();
    app.run();

