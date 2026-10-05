from observers.observateur import Observateur

#Observateur qui calcule et affiche la valeur totale du portefeuille
class Portfolio(Observateur):

    def __init__(self, label_valeur, label_variation):
        self.label_valeur = label_valeur
        self.label_variation = label_variation

    def actualiser(self, sujet) -> None:
        # Obtenir les données du sujet
        donnees = sujet.get_donnees()

        prix_actuels = donnees["prix_actuels"]
        titres = donnees["titres"]

        valeur_totale = 0
        valeur_ouverture = 0

        # Calcul de la valeur du portefeuille
        for ticker, (prix, ouverture) in prix_actuels.items():
            quantite = titres[ticker]["quantite"]

            valeur_totale += prix * quantite
            valeur_ouverture += ouverture * quantite

        # Variation totale depuis l'ouverture
        variation = valeur_totale - valeur_ouverture

        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"

        self.label_valeur.config(
            text=f"Valeur totale : {valeur_totale:.2f} $"
        )

        self.label_variation.config(
            text=f"{symbole} {abs(variation):.2f} $ depuis l'ouverture",
            fg=couleur
        )