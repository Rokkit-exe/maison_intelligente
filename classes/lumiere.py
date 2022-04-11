# Francis Di-Folco
# 2022-03-17

import grovepi
from classes.intensiter import Intensiter

class Lumiere:
    def __init__(self, port, lock, intensiter=None ):
        self.port = port
        self.lock = lock

    def allumer(self):
        with self.lock:
            grovepi.digitalWrite(self.port, 1)

    def eteindre(self):
        with self.lock:
            grovepi.digitalWrite(self.port, 0)


