from observateurs.observateur import Observateur

class Alertes(Observateur):
    def __init__(self, label_alertes):
        # alerts 
        self.label_alertes = label_alertes

    def actualiser(self, sujet):
        # Obtenir toutes les données du sujet (Portefeuille)

        data = sujet.get_donnees()
        prix_actuels = data["prix_actuels"]

        alertes = []

        # Vérifier chaque titre pour les conditions d'alerte

        for ticker, info in prix_actuels.items():
            prix = info["prix"]
            seuil_haut = info["seuil_haut"]
            seuil_bas = info["seuil_bas"]

            if prix >= seuil_haut:
                alertes.append(f"⚠️ {ticker} dépasse le seuil haut ({prix:.2f} ≥ {seuil_haut:.2f})")
            elif prix <= seuil_bas:
                alertes.append(f"⚠️ {ticker} sous le seuil bas ({prix:.2f} ≤ {seuil_bas:.2f})")

        # mettre à jour les étiquettes. 
        if alertes:
            self.label_alertes.config(text="\n".join(alertes), fg="red")
        else:
            self.label_alertes.config(text="Aucune alerte", fg="gray")
