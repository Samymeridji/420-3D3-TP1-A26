import yfinance as yf
from modeles.sujet import Sujet


class Portefeuille(Sujet):

    def __init__(self):
        #initialise la liste des observateurs
        super().__init__()

        #titres du portefeuille
        self.titres = {
            "AAPL": {
                "quantite": 10,
                "seuil_haut": 200.0,
                "seuil_bas": 150.0
            },
            "GOOGL": {
                "quantite": 5,
                "seuil_haut": 160.0,
                "seuil_bas": 120.0
            },
            "MSFT": {
                "quantite": 8,
                "seuil_haut": 430.0,
                "seuil_bas": 380.0
            }
        }

        #prix actuels des titres
        self.prix_actuels = {}

    def rafraichir(self):
        #recupere les nouveaux prix
        self.prix_actuels = {}

        for ticker in self.titres:
            info = yf.Ticker(ticker).fast_info

            prix = info["last_price"]
            ouverture = info["open"]

            self.prix_actuels[ticker] = (prix, ouverture)

        #avertir les observateurs
        self.notifier()

    def get_donnees(self) -> dict:
        #retourne les donnees aux observateurs
        return {
            "titres": self.titres,
            "prix_actuels": self.prix_actuels
        }