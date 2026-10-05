from modeles.portefeuille import Portefeuille
from views.dashboard import Dashboard


portefeuille = Portefeuille()

app = Dashboard(portefeuille)

app.mainloop()