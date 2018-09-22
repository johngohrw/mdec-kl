from flask import *
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__);

global firebaseDB;

def main():
    # All things global should be defined here
    global firebaseDB;
    cred = credentials.Certificate("mdec-5edc2-firebase-adminsdk-vg9vm-9c5355fe8e.json");
    firebaseDB = firebase_admin.initialize_app(cred);


@app.route("/")
def hello_world():
    return "HELLO";


@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404;


@app.errorhandler(405)
def method_not_allowed(error):
    return "405 METHOD NOT ALLOWED", 405


if __name__ == "__main__":
    main();
    app.run();

