import yfinance as yf
from modeles.sujet import Sujet

#Sujet concret qui contient les données du portefeuille et récupère les prix
class Portefeuille(Sujet):

    def __init__(self):
        # Initialise la liste des observateurs
        super().__init__()

        # Titres du portefeuille
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

        # Prix actuels des titres
        self.prix_actuels = {}

    def recuperer_prix(self, ticker):
        """
        Récupère le prix actuel et le prix d'ouverture d'un titre.
        """
        info = yf.Ticker(ticker).fast_info

        prix = info["last_price"]
        ouverture = info["open"]

        if prix is None or ouverture is None:
            raise ValueError(f"Impossible de récupérer le prix de {ticker}")

        return float(prix), float(ouverture)

    def rafraichir(self):
        """
        Récupère les nouveaux prix et avertit tous les observateurs.
        """
        self.prix_actuels = {}

        for ticker in self.titres:
            try:
                prix, ouverture = self.recuperer_prix(ticker)

                self.prix_actuels[ticker] = (
                    prix,
                    ouverture
                )

            except Exception as e:
                print(
                    f"Erreur lors de la récupération de {ticker}: {e}"
                )

        # Avertir les observateurs avec les données récupérées
        self.notifier()

    def ajouter_titre(
        self,
        ticker,
        quantite,
        seuil_bas=None,
        seuil_haut=None
    ):
        """
        Ajoute un nouveau titre au portefeuille.
        """

        ticker = ticker.strip().upper()

        if ticker in self.titres:
            raise ValueError(
                f"{ticker} est déjà dans le portefeuille."
            )

        if quantite <= 0:
            raise ValueError(
                "La quantité doit être supérieure à 0."
            )

        # Vérifier que le ticker existe et récupérer son prix
        prix, ouverture = self.recuperer_prix(ticker)

        # Si aucun seuil n'est donné :
        # -20 % pour le seuil bas
        # +20 % pour le seuil haut
        if seuil_bas is None:
            seuil_bas = prix * 0.80

        if seuil_haut is None:
            seuil_haut = prix * 1.20

        if seuil_bas >= seuil_haut:
            raise ValueError(
                "Le seuil bas doit être inférieur au seuil haut."
            )

        self.titres[ticker] = {
            "quantite": quantite,
            "seuil_bas": round(seuil_bas, 2),
            "seuil_haut": round(seuil_haut, 2)
        }

        # Enregistrer immédiatement le prix
        self.prix_actuels[ticker] = (
            prix,
            ouverture
        )

        # Important pour le TP :
        # une modification doit notifier les observateurs
        self.notifier()

    def modifier_quantite(self, ticker, nouvelle_quantite):
        """
        Modifie la quantité d'actions d'un titre.
        """

        ticker = ticker.upper()

        if ticker not in self.titres:
            raise ValueError(
                f"{ticker} n'existe pas dans le portefeuille."
            )

        if nouvelle_quantite <= 0:
            raise ValueError(
                "La quantité doit être supérieure à 0."
            )

        self.titres[ticker]["quantite"] = nouvelle_quantite

        # Avertir les observateurs
        self.notifier()

    def modifier_seuils(self, ticker, seuil_bas, seuil_haut):
        """
        Modifie les seuils d'alerte d'un titre.
        """

        ticker = ticker.upper()

        if ticker not in self.titres:
            raise ValueError(
                f"{ticker} n'existe pas dans le portefeuille."
            )

        if seuil_bas <= 0 or seuil_haut <= 0:
            raise ValueError(
                "Les seuils doivent être positifs."
            )

        if seuil_bas >= seuil_haut:
            raise ValueError(
                "Le seuil bas doit être inférieur au seuil haut."
            )

        self.titres[ticker]["seuil_bas"] = seuil_bas
        self.titres[ticker]["seuil_haut"] = seuil_haut

        self.notifier()

    def retirer_titre(self, ticker):
        """
        Retire un titre du portefeuille.
        """

        ticker = ticker.upper()

        if ticker not in self.titres:
            raise ValueError(
                f"{ticker} n'existe pas dans le portefeuille."
            )

        del self.titres[ticker]

        if ticker in self.prix_actuels:
            del self.prix_actuels[ticker]

        self.notifier()

    def get_donnees(self) -> dict:
        """
        Retourne les données aux observateurs.
        """

        return {
            "titres": self.titres,
            "prix_actuels": self.prix_actuels
        }