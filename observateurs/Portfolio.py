from observateurs.observateur import Observateur

class Portfolio(Observateur):
    def __init__(self, label_valeur, label_variation):
        # Tkinter labels pour totale et variation 
        self.label_valeur = label_valeur
        self.label_variation = label_variation

    def actualiser(self, sujet):
        # obtenir toutes les données du sujet (Portefeuille)
        data = sujet.get_donnees()
        prix_actuels = data["prix_actuels"]
        titres = data["titres"]

        valeur_totale = 0
        valeur_ouverture = 0

        # calculer la valeur totale et la valeur d'ouverture.
        for ticker, info in prix_actuels.items():
            prix = info["prix"]
            ouverture = info["ouverture"]
            quantite = titres[ticker]["quantite"]

            valeur_totale += prix * quantite
            valeur_ouverture += ouverture * quantite

        # Variation depuis l'ouverture du marché.
        variation = valeur_totale - valeur_ouverture

        # Mise en forme de l'interface utilisateur

        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"

        # mettre à jour les étiquettes
        self.label_valeur.config(text=f"Valeur totale : {valeur_totale:.2f} $")
        self.label_variation.config(
            text=f"{symbole} {abs(variation):.2f} $ depuis l'ouverture",
            fg=couleur
        )


