from datetime import datetime
import pandas as pd
import sys
from matplotlib import pyplot as plt
import json

origine_temps = datetime(1996,1,1)

with open(sys.argv[1],'r') as csvfile :
	donnees = pd.read_csv(csvfile, sep=";", low_memory = False)

Temps_temperature = {}
Temperature = {}

Temps_humidite = {}
Humidite = {}

donnees = donnees.sort_values(by=['date'])
donnees = donnees.reset_index(drop=True)

for i in range(0,len(donnees["numer_sta"])) :
	date = datetime.strptime(str(donnees["date"][i]),'%Y%m%d%H%M%S')
	temperature = str(donnees["t"][i])
	humidite = str(donnees["u"][i])

	annee = date.strftime("%Y")
	if annee == "2008"  or annee == "2019" :
		dt = date - datetime(int(annee), 1, 1)

		
		dt = int(dt.days) + int(dt.seconds)/3600/24

		if temperature != 'mq' :
			if annee in Temps_temperature.keys() :
				Temps_temperature[annee].append(dt)
				Temperature[annee].append(float(temperature))
			else :
				Temps_temperature[annee] = [dt]
				Temperature[annee] = [float(temperature)]

		if humidite != 'mq' :
			if annee in Temps_humidite.keys() :
				Temps_humidite[annee].append(dt)
				Humidite[annee].append(float(humidite))
			else :
				Temps_humidite[annee] = [dt]
				Humidite[annee] = [float(humidite)]



for clef in Temps_temperature.keys() :
	plt.plot(Temps_temperature[clef], Temperature[clef], label=clef)
plt.legend()
plt.savefig("temperatureTest.png")
plt.clf()

with open('temperatureTest.json','w') as jsonfile :
	jsonfile.write(json.dumps([Temps_temperature, Temperature], indent=4))

for clef in Temps_humidite.keys() :
	plt.plot(Temps_humidite[clef], Humidite[clef], label=clef)
plt.legend()
plt.savefig("humiditeTest.png")
plt.clf()

with open('humiditeTest.json','w') as jsonfile :
	jsonfile.write(json.dumps([Temps_humidite, Humidite], indent=4))



