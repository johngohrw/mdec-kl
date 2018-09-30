import paho.mqtt.client as mqtt

class MQTTClient:

    def __init__(self, mqtt_server = "localhost", mqtt_server_port = 1883):
        # MQTT client setup
        self.client = mqtt.Client();
        self.client.on_connect = self.__on_connect;
        self.client.on_message = self.__on_message;
        self.client.connect(mqtt_server, mqtt_server_port);
        self.client.loop_start();

        # Topics
        self.pubTopic = "/nodemcu/led";
        self.subTopic = "/nodemcu/general";
        print("MQTT Client up and ready!");


    def __on_connect(self, client, userdata, flags, returnCode):
        print("Connected to MQTT server (%d)" % returnCode);
        # Any subscription topics should be put here
        self.client.subscribe(self.subTopic);


    def __on_message(self, client, userdata, msg):
        print(msg.topic + ": " + str(msg.payload));


    def publishData(self, data):
        self.client.publish(self.pubTopic, data);

