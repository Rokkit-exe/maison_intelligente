import grovepi
import paho.mqtt.client as mqtt
import time, threading

from classes.button import Button
from classes.capteur_lumiere import Capteur_Lumiere
from classes.dht11 import DHT11
from classes.lcd import LCD
from classes.lumiere import Lumiere
from classes.potentiometre import Potentiometre
from classes.detecteur_mouvement import Detecteur_Mouvement
from classes.controleur import Controleur
from classes.courtier import Courtier


LOCK = threading.Lock()
stop = False

# analog
PORT_POT = 2
PORT_CAPTEUR_LUMIERE = 0

# digital
PORT_DHT11 = 2
PORT_BOUTON = 5
PORT_LED_ROUGE = 8
PORT_LED_BLEU = 4
PORT_LED_VERT = 3
PORT_DM = 7

bouton = Button(PORT_BOUTON, LOCK)
cl = Capteur_Lumiere(PORT_CAPTEUR_LUMIERE, LOCK)
dht11 = DHT11(PORT_DHT11, LOCK)
lcd = LCD(LOCK)
led_rouge = Lumiere(PORT_LED_ROUGE, LOCK)
led_bleu = Lumiere(PORT_LED_BLEU, LOCK)
led_vert = Lumiere(PORT_LED_VERT, LOCK)
pot = Potentiometre(PORT_POT, LOCK)
dm = Detecteur_Mouvement(PORT_DM, LOCK)

topic_publish = "CLG/IOT/LP"
topic_subscribe = "blblka"
user = "LP"
ip = "test.mosquitto.org"

courtier = Courtier(topic_publish,topic_subscribe, user, ip)
controleur = Controleur(bouton, cl, dm, dht11, lcd, pot, led_rouge, led_bleu, led_vert, courtier, stop)

def initialiser_capteur():
    led_rouge.eteindre()
    led_vert.eteindre()
    led_bleu.eteindre()

# surveille si bouton est clicker et affiche la bonne page du lcd
thread_interface = threading.Thread(target=controleur.control_interface, args=())

# lit capteurs (dht11, potentiometre, affiche les donners du lcd)
thread_capteur = threading.Thread(target=controleur.lecture_capteur, args=())

# allume et eteint les LED en fonction des capteurs
thread_action = threading.Thread(target=controleur.controleur_action, args=())
initialiser_capteur()
thread_interface.start()
thread_capteur.start()
thread_action.start()

thread_interface.join()
thread_capteur.join()
thread_action.join()


