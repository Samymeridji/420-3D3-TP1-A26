from datetime import datetime
import os
from observers.observateur import Observateur

#Observateur non visuel qui enregistre les données dans le fichier CSV (journalisation)
class Logger(Observateur):

    def actualiser(self, sujet) -> None:
        #recupere les donnees du portefeuille
        donnees = sujet.get_donnees()
        prix_actuels = donnees["prix_actuels"]

        #date et heure de la maj
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fichier_vide = not os.path.exists("portfolio.csv") or os.path.getsize("portfolio.csv") == 0
        with open("portfolio.csv", "a") as fichier:

            # Ajoute les noms des colonnes une seule fois
            if fichier_vide:
                fichier.write("horodatage,ticker,prix,ouverture\n")
            for ticker, (prix, ouverture) in prix_actuels.items():
                fichier.write(
                    f"{horodatage},{ticker},{prix:.2f},{ouverture:.2f}\n"
                )