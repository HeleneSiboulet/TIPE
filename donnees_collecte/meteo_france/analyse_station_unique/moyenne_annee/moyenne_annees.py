import json
from matplotlib import pyplot as plt

with open('temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('humidite.json') as jsonfile :
	humidite = json.load(jsonfile)


Moyenne_temperature = []


dates = set()

for annee in temperature[0].keys() :
	for date in temperature[0][annee] :
		dates.add(date)
dates = list(dates)
dates.sort()

for date in dates :
	i = 0
	somme_temperature = 0
	for annee in temperature[0].keys() :
		if date in temperature[0][annee]:
			index = temperature[0][annee].index(date)
			i += 1
			somme_temperature += temperature[1][annee][index]
	Moyenne_temperature.append(somme_temperature/i)
plt.plot(dates, Moyenne_temperature)
plt.savefig("Moyenne_temperature.png")
plt.clf()

with open("Moyenne_temperature.json",'w') as jsonfile :
	jsonfile.write(json.dumps([dates, Moyenne_temperature], indent=4))


Moyenne_humidite =[]
dates = set()

for annee in humidite[0].keys() :
	for date in humidite[0][annee] :
		dates.add(date)
dates = list(dates)
dates.sort()

for date in dates :
	i = 0
	somme_humidite = 0
	for annee in humidite[0].keys() :
		if date in humidite[0][annee]:
			index = humidite[0][annee].index(date)
			i += 1
			somme_humidite += humidite[1][annee][index]
	Moyenne_humidite.append(somme_humidite/i)
plt.plot(dates, Moyenne_humidite)
plt.savefig("Moyenne_humidite.png")
plt.clf()

with open("Moyenne_humidite.json",'w') as jsonfile :
	jsonfile.write(json.dumps([dates, Moyenne_humidite],indent=4))



