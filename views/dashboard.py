import tkinter as tk

from observers.PrixTitres import PrixTitres
from observers.Portfolio import Portfolio
from observers.Alertes import Alertes
from observers.Logger import Logger

#Fenêtre principale qui construit l'interface et connecte les observateurs au portefeuille
class Dashboard(tk.Tk):

    # Rafraîchissement des prix toutes les 30 secondes
    INTERVALLE_MS = 30000

    def __init__(self, portefeuille):
        super().__init__()

        # Le portefeuille contient les données de l'application
        self.portefeuille = portefeuille

        self.title("Portfolio Tracker")
        self.resizable(False, False)

        # Garde les labels et les frames associés à chaque titre
        self.labels_prix = {}
        self.frames_prix = {}

        # Prépare l'interface et les observateurs
        self._construire_interface()
        self._creer_observateurs()
        self._abonner_observateurs()

        # Premier rafraîchissement
        self.after(100, self._rafraichir)

    def _construire_interface(self):

        # Titre de l'application
        tk.Label(
            self,
            text="Portfolio Tracker",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        # Zone des prix
        self.frame_prix = tk.LabelFrame(
            self,
            text="Prix en temps réel",
            padx=10,
            pady=10
        )

        self.frame_prix.pack(
            fill=tk.X,
            padx=10,
            pady=5
        )

        # Crée une ligne pour chaque titre
        for ticker in self.portefeuille.get_donnees()["titres"]:
            self._creer_ligne_prix(ticker)

        # Zone du portefeuille
        frame_portfolio = tk.LabelFrame(
            self,
            text="Mon portfolio",
            padx=10,
            pady=10
        )

        frame_portfolio.pack(
            fill=tk.X,
            padx=10,
            pady=5
        )

        self.label_valeur = tk.Label(
            frame_portfolio,
            text="Valeur totale : calcul en cours..."
        )

        self.label_valeur.pack()

        self.label_variation = tk.Label(
            frame_portfolio,
            text=""
        )

        self.label_variation.pack()

        # Zone des alertes
        frame_alertes = tk.LabelFrame(
            self,
            text="Alertes",
            padx=10,
            pady=10
        )

        frame_alertes.pack(
            fill=tk.X,
            padx=10,
            pady=5
        )

        self.label_alertes = tk.Label(
            frame_alertes,
            text="Aucune alerte",
            fg="gray"
        )

        self.label_alertes.pack()

        # Zone pour gérer les titres
        frame_gestion = tk.LabelFrame(
            self,
            text="Gérer les titres",
            padx=10,
            pady=10
        )

        frame_gestion.pack(
            fill=tk.X,
            padx=10,
            pady=5
        )

        # Liste des titres
        self.listbox_titres = tk.Listbox(
            frame_gestion,
            height=5
        )

        self.listbox_titres.pack(
            fill=tk.X,
            pady=5
        )

        self._rafraichir_liste()

        # Zone d'ajout
        frame_ajout = tk.Frame(frame_gestion)
        frame_ajout.pack(fill=tk.X)

        tk.Label(
            frame_ajout,
            text="Ticker:"
        ).pack(side=tk.LEFT)

        self.entry_ticker = tk.Entry(
            frame_ajout,
            width=8
        )

        self.entry_ticker.pack(
            side=tk.LEFT,
            padx=5
        )

        tk.Label(
            frame_ajout,
            text="Quantité:"
        ).pack(side=tk.LEFT)

        self.entry_quantite = tk.Entry(
            frame_ajout,
            width=6
        )

        self.entry_quantite.pack(
            side=tk.LEFT,
            padx=5
        )

        tk.Button(
            frame_ajout,
            text="Ajouter",
            command=self.ajouter_titre
        ).pack(side=tk.LEFT)

        # Zone de modification
        frame_modification = tk.Frame(frame_gestion)

        frame_modification.pack(
            fill=tk.X,
            pady=5
        )

        tk.Label(
            frame_modification,
            text="Nouvelle quantité:"
        ).pack(side=tk.LEFT)

        self.entry_nouvelle_quantite = tk.Entry(
            frame_modification,
            width=6
        )

        self.entry_nouvelle_quantite.pack(
            side=tk.LEFT,
            padx=5
        )

        # Seuils d'alerte (facultatifs si on modifie seulement la quantité)
        tk.Label(frame_modification, text="Seuil bas:").pack(side=tk.LEFT)
        self.entry_nouveau_seuil_bas = tk.Entry(frame_modification, width=7)
        self.entry_nouveau_seuil_bas.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_modification, text="Seuil haut:").pack(side=tk.LEFT)
        self.entry_nouveau_seuil_haut = tk.Entry(frame_modification, width=7)
        self.entry_nouveau_seuil_haut.pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_modification,
            text="Modifier",
            command=self.modifier_quantite
        ).pack(side=tk.LEFT)

        tk.Button(
            frame_modification,
            text="Retirer",
            command=self.retirer_titre
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        # Message de statut
        self.label_statut = tk.Label(
            self,
            text="",
            fg="gray"
        )

        self.label_statut.pack(pady=5)

    def _creer_observateurs(self):

        # Observateur qui affiche les prix
        self.prix_titres = PrixTitres(
            self.labels_prix
        )

        # Observateur qui affiche la valeur du portefeuille
        self.portfolio = Portfolio(
            self.label_valeur,
            self.label_variation
        )

        # Observateur qui affiche les alertes
        self.alertes = Alertes(
            self.label_alertes
        )

        # Observateur qui écrit dans le fichier CSV
        self.logger = Logger()

    def _abonner_observateurs(self):

        # On abonne tous les observateurs au portefeuille
        self.portefeuille.abonner(self.prix_titres)
        self.portefeuille.abonner(self.portfolio)
        self.portefeuille.abonner(self.alertes)
        self.portefeuille.abonner(self.logger)

    def _creer_ligne_prix(self, ticker):

        # Crée une ligne pour afficher le prix d'un titre
        frame = tk.Frame(self.frame_prix)

        frame.pack(
            fill=tk.X,
            pady=2
        )

        tk.Label(
            frame,
            text=f"{ticker}:",
            width=8,
            anchor="w"
        ).pack(side=tk.LEFT)

        label = tk.Label(
            frame,
            text="Chargement..."
        )

        label.pack(side=tk.LEFT)

        # Sauvegarde les widgets pour pouvoir les modifier plus tard
        self.labels_prix[ticker] = label
        self.frames_prix[ticker] = frame

    def _rafraichir_liste(self):

        # Vide puis reconstruit la liste des titres
        self.listbox_titres.delete(
            0,
            tk.END
        )

        titres = self.portefeuille.get_donnees()["titres"]

        for ticker, infos in titres.items():

            quantite = infos["quantite"]

            self.listbox_titres.insert(
                tk.END,
                f"{ticker} — {quantite} action(s)"
            )

    def _ticker_selectionne(self):

        # Récupère le titre sélectionné dans la liste
        selection = self.listbox_titres.curselection()

        if not selection:
            return None

        texte = self.listbox_titres.get(
            selection[0]
        )

        return texte.split(" — ")[0]

    def ajouter_titre(self):

        # Récupère les valeurs entrées par l'utilisateur
        ticker = self.entry_ticker.get().strip().upper()
        if not ticker:
            self.label_statut.config(
                text="Veuillez entrer un ticker.",
                fg="red"
            )
            return
        try:
            quantite = int(
                self.entry_quantite.get()
            )

            # Le label doit exister avant la notification
            if ticker not in self.labels_prix:
                self._creer_ligne_prix(ticker)

            # Ajoute le titre dans le portefeuille
            self.portefeuille.ajouter_titre(
                ticker,
                quantite
            )

            self._rafraichir_liste()

            # Vide les champs après l'ajout
            self.entry_ticker.delete(
                0,
                tk.END
            )

            self.entry_quantite.delete(
                0,
                tk.END
            )

            self.label_statut.config(
                text=f"{ticker} ajouté.",
                fg="green"
            )

        except Exception as erreur:

            # Enlève la ligne si l'ajout a échoué
            if (
                ticker in self.frames_prix
                and ticker not in self.portefeuille.get_donnees()["titres"]
            ):
                self.frames_prix[ticker].destroy()

                del self.frames_prix[ticker]
                del self.labels_prix[ticker]

            self.label_statut.config(
                text=f"Erreur : {erreur}",
                fg="red"
            )

    def modifier_quantite(self):
        # Modifie la quantité et/ou les deux seuils du titre sélectionné
        ticker = self._ticker_selectionne()
        if ticker is None:
            self.label_statut.config(text="Sélectionnez un titre.", fg="orange")
            return

        try:
            texte_quantite = self.entry_nouvelle_quantite.get().strip()
            texte_bas = self.entry_nouveau_seuil_bas.get().strip()
            texte_haut = self.entry_nouveau_seuil_haut.get().strip()

            if not texte_quantite and not texte_bas and not texte_haut:
                raise ValueError("Entrez une quantité ou les deux seuils.")

            # Valider tous les champs avant de modifier le portefeuille
            quantite = None
            if texte_quantite:
                quantite = int(texte_quantite)
                if quantite <= 0:
                    raise ValueError("La quantité doit être supérieure à 0.")

            seuil_bas = None
            seuil_haut = None
            if texte_bas or texte_haut:
                if not texte_bas or not texte_haut:
                    raise ValueError("Vous devez entrer les deux seuils.")
                seuil_bas = float(texte_bas)
                seuil_haut = float(texte_haut)
                if not (0 < seuil_bas < seuil_haut < float('inf')):
                    raise ValueError("Les seuils doivent être positifs et le seuil bas inférieur au seuil haut.")

            # Ces méthodes appellent notifier() dans Portefeuille
            if quantite is not None:
                self.portefeuille.modifier_quantite(ticker, quantite)
            if seuil_bas is not None:
                self.portefeuille.modifier_seuils(ticker, seuil_bas, seuil_haut)

            self._rafraichir_liste()
            self.entry_nouvelle_quantite.delete(0, tk.END)
            self.entry_nouveau_seuil_bas.delete(0, tk.END)
            self.entry_nouveau_seuil_haut.delete(0, tk.END)
            self.label_statut.config(text=f"{ticker} modifié.", fg="green")

        except (ValueError, OverflowError) as erreur:
            self.label_statut.config(text=f"Erreur : {erreur}", fg="red")
        except Exception as erreur:
            self.label_statut.config(text=f"Erreur : {erreur}", fg="red")

    def retirer_titre(self):

        # Récupère le titre sélectionné
        ticker = self._ticker_selectionne()

        if ticker is None:
            self.label_statut.config(
                text="Sélectionnez un titre.",
                fg="orange"
            )
            return

        try:
            # Retire le titre du portefeuille
            self.portefeuille.retirer_titre(
                ticker
            )

            # Retire aussi les widgets du titre
            if ticker in self.frames_prix:
                self.frames_prix[ticker].destroy()

                del self.frames_prix[ticker]
                del self.labels_prix[ticker]

            self._rafraichir_liste()

            self.label_statut.config(
                text=f"{ticker} retiré.",
                fg="green"
            )

        except Exception as erreur:
            self.label_statut.config(
                text=f"Erreur : {erreur}",
                fg="red"
            )

    def _rafraichir(self):

        try:
            # Met à jour les prix et prévient les observateurs
            self.portefeuille.rafraichir()

            self.label_statut.config(
                text="Données mises à jour.",
                fg="gray"
            )

        except Exception as erreur:
            self.label_statut.config(
                text=f"Erreur : {erreur}",
                fg="red"
            )

        # Relance la mise à jour après 30 secondes
        self.after(
            self.INTERVALLE_MS,
            self._rafraichir
        )