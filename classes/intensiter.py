# Francis Di-Folco
# 2022-03-17

class Intensiter:
    MIN_INTENSITER = 0
    MAX_INTENSITER = 255

    def __init__(self):
        self.valeur = None

    def set_intensiter(self, valeur):
        if (valeur >= Intensiter.MIN_INTENSITER and valeur <= Intensiter.MAX_INTENSITER):
            self.valeur = valeur
        else:
            print("intensiter invalide => valeur [0-255]")

    def get_intensiter(self):
        return self.valeur

