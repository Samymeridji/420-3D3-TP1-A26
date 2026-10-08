from observers.observateur import Observateur

#Observateur qui vérifie les seuils et affiche les alertes
class Alertes(Observateur):

    def __init__(self, label_alertes):
        self.label_alertes = label_alertes

    def actualiser(self, sujet) -> None:
        # Obtenir les données du sujet
        donnees = sujet.get_donnees()

        prix_actuels = donnees["prix_actuels"]
        titres = donnees["titres"]

        alertes = []

        # Vérifier les seuils de chaque titre
        for ticker, (prix, ouverture) in prix_actuels.items():

            seuil_haut = titres[ticker]["seuil_haut"]
            seuil_bas = titres[ticker]["seuil_bas"]

            if prix >= seuil_haut:
                alertes.append(
                    f"⚠️ {ticker} dépasse le seuil haut "
                    f"({prix:.2f} $ ≥ {seuil_haut:.2f} $)"
                )

            elif prix <= seuil_bas:
                alertes.append(
                    f"⚠️ {ticker} sous le seuil bas "
                    f"({prix:.2f} $ ≤ {seuil_bas:.2f} $)"
                )

        if alertes:
            self.label_alertes.config(
                text="\n".join(alertes),
                fg="red"
            )
        else:
            self.label_alertes.config(
                text="Aucune alerte",
                fg="gray"
            )