import numpy as np
import json
from matplotlib import pyplot as plt



import json
from matplotlib import pyplot as plt

with open('../temperature.json') as jsonfile :
	temperature = json.load(jsonfile)


Moyenne_temperature = []
dates = set()

for annee in temperature[0].keys() :
	for date in temperature[0][annee] :
		dates.add(int (date))
dates = list(dates)
dates.sort()

for date in dates :
	i = 0
	somme_temperature = 0
	for annee in temperature[0].keys() :
		for heure in range (8):
			if date + (1/8) * heure in temperature[0][annee]:
				index = temperature[0][annee].index(date)
				i += 1
				somme_temperature += temperature[1][annee][index]
	Moyenne_temperature.append(somme_temperature/i)
plt.plot(dates, Moyenne_temperature)
plt.savefig("Moyenne_temperature.png")
plt.clf()

f = []
g = []
h = []
for m in mesure :
	pf = 12.73536399*np.cos(2*np.pi*(m-1)/8 + 5.61376937) +71.15758689
	f .append (pf)
	pg = 71.15503638 + 12.90397869*np.cos(2*np.pi*(m-1)/8 + 5.62646828) -2.70175487 *np.cos(4*np.pi*(m-1)/8 + 5.69268334)
	g .append (pg) 
	ph = 71.1553131 + 12.95354558*np.cos(2*np.pi*(m-1)/8 + 5.62648561 ) - 2.72510888 *np.cos(4*np.pi*(m-1)/8 + 5.66712864) + -0.16110029 *np.cos(4*np.pi*(m-1)/8 + 6.21532372)
	h.append (ph)
#print (str (r))
plt.plot (mesure, r, label = "moyenne")
plt.plot (mesure, f, label = "f")
plt.plot (mesure, g, label = "g")
plt.plot (mesure, h, label = "h")

plt.legend()
plt.savefig("moyenne_sur_la_journeeH.png")
