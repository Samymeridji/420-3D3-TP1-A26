from datetime import datetime
from observers.observateur import Observateur

#Observateur non visuel qui enregistre les données dans le fichier CSV (journalisation)
class Logger(Observateur):

    def actualiser(self, sujet) -> None:
        #recupere les donnees du portefeuille
        donnees = sujet.get_donnees()
        prix_actuels = donnees["prix_actuels"]

        #date et heure de la maj
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #ajoute les prix dans le fichier csv
        with open("portfolio.csv", "a") as fichier:
            for ticker, (prix, ouverture) in prix_actuels.items():
                fichier.write(
                    f"{horodatage},{ticker},{prix:.2f},{ouverture:.2f}\n"
                )