import grovepi

class Detecteur_Mouvement:
    def __init__(self, port, lock):
        self.port = port
        self.lock = lock
    
    def lecture(self):
        with self.lock:
            return grovepi.digitalRead(self.port)
