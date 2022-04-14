# Francis Di-Folco
# 2022-03-17

import time,random
from grove_rgb_lcd import *

class LCD:
    RANGER = 2
    COLONNE = 16

    def __init__(self, lock):
        self.lock = lock
        self.initialiser()

        # afficher un charactère fait maison avec la couleur en param
    # affiche ce charactere sur l'index 1
    def afficher_char(self, schema, r,g,b, interval):
        with self.lock:
            setRGB(r,g,b)
            for i in range(0,len(schema)):
                create_char(0,schema[i])
                setText(f"{chr(0)}")
                time.sleep(interval)
            self.initialiser()

    def afficher_index(self, temp, humid, mode, r, g, b):
        with self.lock:
            setRGB(r,g,b)
            text1 = self.formater_ligne(f"temp {temp}C " + mode)
            text2 = self.formater_ligne(f"humiditer {humid}% ")
            setText(text1 + text2)
    
    def afficher_edit(self, est_temp, temp, humid, r, g, b):
        with self.lock:
            fleche  = [
                0b00000,
                0b00100,
                0b00110,
                0b11111,
                0b00110,
                0b00100,
                0b00000,
                0b00000
            ]
            setRGB(r,g,b)
            create_char(0,fleche)
            if (est_temp):
                text1 = self.formater_ligne(f"{chr(0)} temp {temp}C ")
                text2 = self.formater_ligne(f"  humiditer {humid}% ")
            else:
                text1 = self.formater_ligne(f"  temp {temp}C ")
                text2 = self.formater_ligne(f"{chr(0)} humiditer {humid}% ")
            setText(text1 + text2)
    
    # ajoute des espaces pour créer une chaine de texte de 16 charactere (1 ligne)
    def formater_ligne(self, text):
        espace = self.COLONNE - len(text)
        for i in range(espace):
            text = text + " "
        return text

    # initialise l'écran (aucun text, aucune couleur)
    def initialiser(self):
        with self.lock:
            setText("")
            setRGB(0,0,0)

    # affiche le text et la couleur pour une durer passer en paramètre
    def afficher(self, text, durer, r,g,b):
        with self.lock:
            setText(text)
            setRGB(r,g,b)
            time.sleep(durer)
            #self.initialiser()

    # flash en affichant le text et
    # les couleur passer en paramètre
    def flash(self, text, r,g,b, repetition=10 , interval=0.5):
        with self.lock:
            for i in range(repetition):
                setRGB(r,g,b)
                setText(text)
                time.sleep(interval)
                self.initialiser()



        