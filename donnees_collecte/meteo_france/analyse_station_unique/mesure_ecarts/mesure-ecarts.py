import json
import sys

with open('temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('humidite.json') as jsonfile :
	humidite = json.load(jsonfile)

with open(sys.argv[1]) as jsonfile :
	temperature_test = json.load(jsonfile)

with open(sys.argv[2]) as jsonfile :
	humidite_test = json.load(jsonfile)

ecarts_temperature = 0
compt = 0
for i_date in range(len(temperature_test[0])) :
	for annee in temperature[0].keys() :
		if temperature_test[0][i_date] in temperature[0][annee] :
			#print(abs(temperature_test[1][i_date] - temperature[1][annee][temperature[0][annee].index(temperature_test[0][i_date])]))
			ecarts_temperature = ecarts_temperature + (temperature_test[1][i_date] - temperature[1][annee][temperature[0][annee].index(temperature_test[0][i_date])])**2
			compt += 1
print("ecart de temperature : " + str((ecarts_temperature/compt)**(1/2)) + "°C")


ecarts_humidite = 0
compt = 0
for i_date in range(len(humidite_test[0])) :
	for annee in humidite[0].keys() :
		if humidite_test[0][i_date] in humidite[0][annee] :
			#print(abs(humidite_test[1][i_date] - humidite[1][annee][humidite[0][annee].index(humidite_test[0][i_date])]))
			ecarts_humidite = ecarts_humidite + (humidite_test[1][i_date] - humidite[1][annee][humidite[0][annee].index(humidite_test[0][i_date])])**2
			compt += 1
print("ecart de humidite : " + str((ecarts_humidite/compt)**(1/2)) +"%")

