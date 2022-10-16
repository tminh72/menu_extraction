from tkinter.tix import Tree
from paho.mqtt import client as mqtt
import random
from time import sleep

client_id = 'check_in_#45'
broker = 'localhost'
port = 1883
username = 'user'
password = 'user'
topic = 'test'
class MQTTServer():
    def __init__(self):
        self.create_client()
    
    def create_client(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        self.client = mqtt.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(broker, port)

    def publish(self):
        num = random.randint(1,100)
        msg = f"messages {num}"
        result = self.client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


if __name__ == '__main__':
    mqtt_server = MQTTServer()
    while True:
        sleep(2)
        mqtt_server.publish()