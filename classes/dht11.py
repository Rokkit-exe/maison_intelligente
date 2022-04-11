# Francis Di-Folco
# 2022-03-17

import grovepi
import time
import threading

# capteur d'humiditer/temperature
class DHT11:

    DHT11 = 0
    DHT22 = 1

    def __init__(self, port, lock):
        self.port = port
        self.lock = lock
        self.temp = None
        self.humid = None

    def lecture(self):
        with self.lock:
            (temp, humid) = grovepi.dht(self.port,self.DHT11)
            self.temp = temp
            self.humid = humid
            return (temp, humid)
       
            
