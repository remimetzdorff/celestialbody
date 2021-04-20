import numpy as np
import matplotlib.pyplot as plt

###########################################################################
# LECTURE DES FICHIERS DE DONNÉES POUR RÉCUPÉRER LES POSITIONS DES PLANÈTES
###########################################################################
# Terre
data_terre = np.loadtxt("earth.txt", skiprows=8)
x_terre, y_terre = data_terre[:,0], data_terre[:,1]
# Tchouri
data_tchouri = np.loadtxt("tchouri.txt", skiprows=8)
x_tchouri, y_tchouri = data_tchouri[:,0], data_tchouri[:,1]
# Jupiter
data_jupiter = np.loadtxt("jupiter.txt", skiprows=8)
x_jupiter, y_jupiter = data_jupiter[:,0], data_jupiter[:,1]

##############################################################
# REPRESENTATION GRAPHIQUE DES POSITIONS DES DIFFÉRENTS OBJETS
##############################################################
fig = plt.figure()

# Le Soleil
plt.plot([0],[0], "*", color="gold", markersize=20, label="Soleil")

# TERRE
#plt.plot(x_terre, y_terre, "o", color="blue", label="Terre")

# TCHOURI
# À compléter

# JUPITER
# À compléter

# Changement d'échelle pour les axes (modification des limites du graphe)
plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)

# Titre, nom des axes et légende
plt.title("Évolution de la position de quelques objets du système solaire")
plt.xlabel("Abscisse par rapport au soleil\nen unités astronomiques (au)")
plt.ylabel("Ordonnée par rapport au soleil\nen unités astronomiques (au)")
plt.legend(loc = "upper left")
fig.axes[0].set_aspect("equal")
plt.show()