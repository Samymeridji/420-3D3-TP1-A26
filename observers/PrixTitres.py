from observers.observateur import Observateur

#Observateur qui affiche le prix et la variation de chaque titre
class PrixTitres(Observateur):

    def __init__(self, labels_prix):
        #labels utilises pour afficher le prix de chaque titre
        self.labels_prix = labels_prix

    def actualiser(self, sujet) -> None:
        #recupere les nouvelles donnees du sujet
        donnees = sujet.get_donnees()
        prix_actuels = donnees["prix_actuels"]

        for ticker, (prix, ouverture) in prix_actuels.items():
            #calcule la variation depuis l'ouverture
            variation = (prix - ouverture) / ouverture * 100

            symbole = "▲" if variation >= 0 else "▼"
            couleur = "green" if variation >= 0 else "red"

            texte = f"{prix:.2f} $  {symbole} {abs(variation):.2f}%"

            #met à jour le label du titre
            if ticker in self.labels_prix:
                self.labels_prix[ticker].config(
                    text=texte,
                    fg=couleur
                )