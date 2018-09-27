const express = require('express');
const http = require('http');
const admin = require('firebase-admin');
const { spawn } = require('child_process');

const serviceAccount = require('./mdec-5edc2-firebase-adminsdk-vg9vm-9c5355fe8e.json'); // Firebase service account key (your private key)
const port = 4001;                                          // localhost port
const app = express();                                      // invoking app instance
const server = http.createServer(app);                      // server instance

// Server listens to given port
server.listen(port, () => {
    console.log(`http server listening on port ${port}`);
});

// initializing Firebase app
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://mdec-5edc2.firebaseio.com/"
});

const firebaseDB = admin.database();
const carEventsRef = firebaseDB.ref("car/carEvents");

carEventsRef.limitToLast(1).on("child_added", snapshot => {
        const jsonData = snapshot.val();
        const flag = jsonData.Event == "Entry" || jsonData.Event == "Motion";
        const child = spawn("python", ["uart_test.py", Number(flag)]);

        child.stdout.on('data', data => {
            console.log(`Child stdout: ${data}`);
        });
        child.stderr.on('data', data => {
            console.log(`Child stderr: ${data}`);
        });
    },
    error => {
        console.log("Car events ref error: " + error.code);
});

