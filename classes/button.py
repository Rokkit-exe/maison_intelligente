# Francis Di-Folco
# 2021-03-17

import grovepi
import threading
import time

from numpy import NaN

class Button:
    def __init__(self, port, lock):
        self.port = port
        self.lock = lock
        self.etat = 0
        self.press = None

    def lecture(self, onclick=True):
        with self.lock:
            if (onclick):
                return self.__on_click__(grovepi.digitalRead(self.port))
            else:
                return grovepi.digitalRead(self.port)

    def __on_click__(self, lecture):
        allumer = None
        if (lecture):
            self.press = True
        if (self.press and not lecture):
            self.press = False
            allumer = 1
        return allumer






