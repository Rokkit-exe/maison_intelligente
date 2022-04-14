import paho.mqtt.client as mqtt
import time

class Controleur:
    EQUART = 2
    DELAI_ACTIVATION = 10
    SEUIL_LUMIERE = 200
    TEMP_MIN = 0
    TEMP_MAX = 30
    BIT_SHIFT_POT = 5
    VALEUR_MAX_POT = 1023
    DELAIS_QUITTER = 5.0
    DERNIERE_PAGE = 4

    def __init__(self, bouton, capteur_lumiere, detecteur_mouvement, dht11, lcd, potentiometre, led_rouge, led_bleu, led_vert, courtier, stop):
        # Capteurs
        self.bouton = bouton
        self.capteur_lumiere = capteur_lumiere
        self.detecteur_mouvement = detecteur_mouvement
        self.dht11 = dht11
        self.lcd = lcd
        self.potentimetre = potentiometre
        self.led_rouge = led_rouge
        self.led_bleu = led_bleu
        self.led_vert = led_vert
        self.courtier = courtier

        # propriété
        self.stop = stop
        self.temp_actuel = 0
        self.temp_cible = 0
        self.humid_actuel = 0
        self.humid_cible = 0
        self.temp_dis = 0
        self.humid_dis = 0
        self.mouvement = 0
        self.luminositer = 0
        self.page = 0
        self.click_enregistrer = False
        self.r = 0
        self.g = 255
        self.b = 0
        self.compteur_quitter = None


    def control_interface(self):
        while(not self.stop):
            time.sleep(0.05)
            lecture = self.bouton.lecture()
            if (lecture and self.page == Controleur.DERNIERE_PAGE):
                self.page = 0
                lecture = None
            if (lecture and self.page < Controleur.DERNIERE_PAGE):
                self.page += 1
            


    def lecture_capteur(self):


        while(not self.stop):
            time.sleep(0.5)
            self.courtier.publish(self.temp_actuel, self.humid_actuel)

            # Donnees locaux
            if (self.page == 0):
                (temp, humid) = self.dht11.lecture()
                if (temp > 0):
                    self.temp_actuel = temp
                if (humid > 0):
                    self.humid_actuel = humid
                self.lcd.afficher_index(self.temp_actuel, self.humid_actuel, "LOC", self.r, self.g, self.b)
                
            # Courtier
            if (self.page == 1):
                time.sleep(0.2)
                self.lcd.afficher_index(self.courtier.temp, self.courtier.humid, "DIS", self.r, self.g, self.b)

            # Temp config
            if (self.page == 2):
                time.sleep(0.2) 
                valeur = self.potentimetre.lecture(Controleur.BIT_SHIFT_POT)
                valeur = Controleur.TEMP_MAX if valeur > Controleur.TEMP_MAX else valeur
                self.temp_cible = valeur
                self.lcd.afficher_edit(1, self.temp_cible, self.humid_cible, self.r, self.g, self.b)

            # Humidite config
            if (self.page == 3):
                time.sleep(0.2)
                valeur = self.potentimetre.lecture()
                valeur = (valeur * 100) / 1023 
                self.humid_cible = valeur
                self.lcd.afficher_edit(0, self.temp_cible, self.humid_cible, self.r, self.g, self.b)

            # Quitter
            if(self.page == 4 and not self.stop):
                time.sleep(0.2)
                self.lcd.afficher("Quitter?", 0, 255, 0, 0)
                if(self.bouton.lecture(False) and self.compteur_quitter == None):
                    self.compteur_quitter = time.perf_counter()



            self.mouvement = self.detecteur_mouvement.lecture()
            self.luminositer = self.capteur_lumiere.lecture()


    def controleur_action(self):
        
        compteur_temp = None
        compteur_humid = None
        compteur_lum = None

        while not self.stop:
            time.sleep(0.5)

            # Chauffage
            if (self.temp_cible - self.temp_actuel >= Controleur.EQUART and compteur_temp == None):
                compteur_temp = time.perf_counter()
            if (compteur_temp != None):
                if (self.temp_cible - self.temp_actuel >= Controleur.EQUART and time.perf_counter() - compteur_temp > Controleur.DELAI_ACTIVATION):
                    self.led_rouge.allumer()
            if (self.temp_actuel >= self.temp_cible):
                compteur_temp = None
                self.led_rouge.eteindre()

            # Déshumidificateur
            if (self.humid_actuel - self.humid_cible >= Controleur.EQUART and compteur_humid == None):
                compteur_humid = time.perf_counter()
            if (compteur_humid != None):
                if (time.perf_counter() - compteur_humid > Controleur.DELAI_ACTIVATION and self.humid_actuel - self.humid_cible >= Controleur.EQUART):
                    self.led_bleu.allumer()
            if (self.humid_actuel <= self.humid_cible):
                compteur_humid = None
                self.led_bleu.eteindre()

            # Mouvement
            if (self.mouvement and self.luminositer < Controleur.SEUIL_LUMIERE and compteur_lum == None):
                self.led_vert.allumer()
                self.g = 255
                compteur_lum = time.perf_counter()
            if (compteur_lum != None):
                if (time.perf_counter() - compteur_lum  > Controleur.DELAI_ACTIVATION):
                    compteur_lum = None
                    self.led_vert.eteindre()
                    self.g = 0
            
            # Quitter
            if(self.compteur_quitter != None and time.perf_counter() - self.compteur_quitter >= Controleur.DELAIS_QUITTER):
                self.stop = True
                self.lcd.afficher("Au revoir!", 4.0, 128, 0, 128)
