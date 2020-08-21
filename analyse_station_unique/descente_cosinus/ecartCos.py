import json
import numpy as np

with open('../json/temperatureTest.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('../json/humiditeTest.json') as jsonfile :
	humidite = json.load(jsonfile)



ecart = 0
compt = 0
for annee in temperature[0].keys() :
	for date in temperature[0][annee] :
		mesure = temperature[1][annee][temperature[0][annee].index(date)]
		prevision =	-3.79759261*np.cos(2*np.pi*date + 5.61085591) + 8.43465377*np.cos(2*np.pi*date/365 + 2.81469216) + 285.13820915
		ecart += (mesure - prevision)**2
		compt += 1

res = (ecart/compt)** (1/2)
print("ecart de temperature : " + str(res) + "°C")

ecart = 0
compt = 0
for annee in humidite[0].keys() :
	for date in humidite[0][annee] :
		mesure = humidite[1][annee][humidite[0][annee].index(date)]
		prevision =	12.96579285 * np.cos(2*np.pi*date + 5.62656321) + 6.90328207 *np.cos(2*np.pi*date/365 + 0.31947095) + 71.15684141
		ecart += (mesure - prevision)**2
		compt += 1

res = (ecart/compt)** (1/2)
print("ecart d'humidite ' : " + str(res) + "%")