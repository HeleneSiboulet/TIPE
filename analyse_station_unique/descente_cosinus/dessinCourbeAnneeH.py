import numpy as np
import json
from matplotlib import pyplot as plt



import json
from matplotlib import pyplot as plt

with open('../json/humidite.json') as jsonfile :
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
			if (date + (1/8) * heure) in temperature[0][annee]:
				index = temperature[0][annee].index(date + (1/8) * heure)
				i += 1
				somme_temperature += temperature[1][annee][index]
	Moyenne_temperature.append(somme_temperature/i)



jour = range (366)
f = []
g = []
h = []
for j in jour :
	pf = 6.78906587*np.cos(2*np.pi*j/365 + 0.31944989) + 71.15758689
	f .append (pf)
	pg = 71.15503638 + 6.87475093*np.cos(2*np.pi*j/365 + 0.31901173) + 2.40357027*np.cos(4*np.pi*j/365 + 0.89433251)
	g .append (pg) 
	ph = 71.1553131 +6.90021219*np.cos(2*np.pi*j/365 + 0.3193087 ) + 2.50198275*np.cos(4*np.pi*j/365 + 1.00739916) + 1.38720613*np.cos(4*np.pi*j/365 + 5.39421813)
	h.append (ph)

plt.plot(dates, Moyenne_temperature, label = "moyenne")
plt.plot (jour, f, label = "f")
plt.plot (jour, g, label = "g")
plt.plot (jour, h, label = "h")
plt.legend()
plt.savefig("CourbeAnneeH.png")

