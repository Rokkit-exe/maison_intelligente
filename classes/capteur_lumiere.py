# Francis Di-Folco
# 2022-03-17

from datetime import datetime
import grovepi
import time

class Capteur_Lumiere:
    def __init__(self, port, lock):
        self.port = port
        self.lock = lock
        

    def lecture(self):
        with self.lock:
            return grovepi.analogRead(self.port)
                


