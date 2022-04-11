# Francis Di-Folco
# 2022-03-17

import time

class Detecteur_Jour_Nuit:
    def __init__(self, func_jour=None, func_nuit=None, seuil_jour=600, seuil_nuit=100, interval=600): #interval 10 min
        self.jour = None
        self.compteur_demarer = False
        self.compteur = None
        self.func_jour = func_jour
        self.func_nuit = func_nuit
        self.seuil_jour = seuil_jour
        self.seuil_nuit = seuil_nuit
        self.interval = interval

    def est_jour(self, valeur):
        # logique jour
        if (valeur >= self.seuil_jour and not self.compteur_demarer): 
            self.jour = True
            self.compteur_demarer = True
            self.compteur = time.perf_counter()
        if (valeur >= self.seuil_jour and self.compteur_demarer):
            now = time.perf_counter()
            if (now - self.compteur >= self.interval):
                self.jour = None
                self.compteur_demarer = False
                self.compteur = None
                if (self.func_jour != None):
                    self.func_jour()
                return True
        # logique nuit
        if (valeur <= self.seuil_nuit and not self.compteur_demarer): 
            self.jour = False
            self.compteur_demarer = True
            self.compteur = time.perf_counter()
        if (valeur <= self.seuil_nuit and self.compteur_demarer):
            now = time.perf_counter()
            if (now - self.compteur >= self.interval):
                self.jour = None
                self.compteur_demarer = False
                self.compteur = None
                if (self.func_nuit != None):
                    self.func_nuit()
                return False
        else:
            return None
