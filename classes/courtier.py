from posixpath import split
import paho.mqtt.client as mqtt

class Courtier:
    def __init__(self, topic_publish, topic_subscribe, user, ip):
        self.topic_publish = topic_publish
        self.topic_subscribe = topic_subscribe
        self.user = user
        self.ip = ip
        self.temp = None
        self.humid = None
        self.est_fini = False
        
        # client
        client = mqtt.Client(self.user)
        client.on_connect = self.on_connection
        client.on_message = self.on_message
        client.connect(self.ip) #"test.mosquitto.org"

    def on_connection(self, client, userdata, flags, rc):
        global result_subscribe , mid_subscribe
        result_subscribe , mid_subscribe = client.subscribe(self.topic_subscribe , 0)
        print("Connected")

    def on_message(self, client,userdata, msg):
        (temp, humid) = str(msg.payload).split(",")
        self.temp = temp
        self.humid = humid
        self.est_fini = True

    def publish(self,temp, humid):
        self.client.loop_start()
        self.client.publish(self.topic_publish,f"{temp},{humid}" , 0, True)
        self.client.loop_stop(self.est_fini)

    ## le deadlock 

