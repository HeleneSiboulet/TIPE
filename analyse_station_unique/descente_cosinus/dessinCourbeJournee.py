import numpy as np
import json
from matplotlib import pyplot as plt



with open('../json/temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('../json/humidite.json') as jsonfile :
	humidite = json.load(jsonfile)

s = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
compt = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
r = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

for annee in temperature[0].keys() :
	for date in temperature[0][annee] :
		i1 = (date - int(date) )* 8
		#print (i1)
		i = int (i1)
		compt[i] += 1
		s [i] += temperature[1][annee][temperature[0][annee].index(date)]

for j in range (len (s)) :
	r[j] = (s[j] / compt[j]) - 273.15

mesure = [1,2,3,4,5,6,7,8]


courbe = []
for m in mesure :
	c = -3.79759261*np.cos(2*np.pi*(m-1)/8 + 5.6) + 285.13820915 - 273.15
	courbe .append (c) 

print (str (r))
plt.plot (mesure, r)
plt.plot (mesure, courbe)
plt.savefig("moyenne_sur_la_journee.png")
