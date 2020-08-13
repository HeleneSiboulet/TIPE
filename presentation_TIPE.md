*** TIPE : Faire des prévisions météorologiques

** État de l'art 

Méthode la plus courante de prévision météo selon Jean Pailleux de Météo-France
Modélisation de l'athmosphère par :
• Équation du mouvement(Newton)
• Équation de continuité
• Thermodynamique
• Équation des gaz parfaits
• Équations de bilans de constituants: vapeur d’eau, eau liquide, ozone, etc...


** Recherche de données

Base de donnée trouvée sur  : https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=90&id_rubrique=32
Contient les relevés de 62 stations en France Métropolitaine et en France d’Outre mer
De 1996 à 2020  (avec certaines mesures manquantes)
Un relevé toutes les trois heures
Paramètres atmosphériques: température, humidité, direction et force du vent, pression atmosphérique, hauteur de précipitations, temps sensible, description des nuages, visibilité
Chaque fichier couvre un moi et toutes les stations

Collecte des données avec Webbot
Décompression des fichiers au format csv
Tri des données par station

** Analyse sur une station unique

Extracion des données de température et d'humidité de Clermont-Ferrandau au format json
Les annees 2008, 2019 et 2020 sont retirées de la base d'entrainement et serviront de base de test
! donnes_collecte/meteo_france/analyse_station_unique/humidite.png
! donnes_collecte/meteo_france/analyse_station_unique/temperature.png

Calcul des Quartiles de l'humidité et de la tempéraure
Température : Q1 = 6.39  Q3 = 17.4  soit un intervalle de 11°C  
Humidité : 	  Q1 = 59.0  Q3 = 85.0  soit un intervalle de 26%

* Calcul de la moyenne de la température et de l'humidité par jour et heure
Approximation de la température à un phoénomène cyclique de période un an

ecart quadratique moyen de temperature : 4.28°C
ecart quadratique moyen d'humidite : 14.8%

* Approximation de la courbe des températures par un fonction
À priori est un phoénomène cyclique sur l'année et sur le jour
Transformée de Fourier

Hypothèse vérifiée :
Approximation par une fonction de la forme f(t) = A cos (w1 t + \varphi<sup>1<\sup>) + B cos (w2 t + \varphi<sup>2<\sup>) + C
avec w1 = 2 \pi  et w2 = 2 \pi /365
Et par une fonction de la forme g(t) = A cos (w1 t + \varphi<sup>1<\sup>) + B cos (w2 t + \varphi<sup>2<\sup>) + C + D cos (w3 t + \varphi<sup>3<\sup>)
avec w3 = 4 \pi

On utilise la méthode du gradient pour trouver les coefficient :
- on crée une fonction écart(u(t)) qui calcule l'écart entre les prévisions de u(t) et les valeurs de la base d'entrainement
- on cherche à trouver le minimum de écart en fonction des paramètres donc
- on initialise aléatoirement les paramètres
- on dérive écart par rapport à chaque paramètre
- on modifie chaque paramètre X en faisant X = X - dX
- on répète les deux points précédants un grand nombre de fois

