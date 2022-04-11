# Francis Di-Folco
# 2022-03-17

import grovepi
import threading
import time

class Potentiometre:
    def __init__(self, port, lock):
        self.port = port
        self.lock = lock
        self.valeur = None
        self.stop = False

    def lecture(self, bit_shift=0):
        with self.lock:
            self.valeur = grovepi.analogRead(self.port)
            return self.valeur >> bit_shift

