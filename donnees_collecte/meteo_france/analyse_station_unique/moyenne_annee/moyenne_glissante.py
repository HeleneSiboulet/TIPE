import json
from matplotlib import pyplot as plt

with open('Moyenne_temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('Moyenne_humidite.json') as jsonfile :
	humidite = json.load(jsonfile)

for nb_glissant in range(1,5) :
	nb_glissant = nb_glissant * 3

	Glissante_temperature = []

	for i in range(len(temperature[0])) :
		somme = 0
		div = 0
		for j in range(nb_glissant) :
			if i+j >= len(temperature[0]) :
				maxi = i+j-len(temperature[0])
			else:
				maxi = i+j

			somme  = somme + 1/(j+2)*temperature[1][i-j] + 1/(j+2)*temperature[1][maxi]
			div = div + 2/(j+2)
		Glissante_temperature.append(somme/div)

	plt.plot(temperature[0], Glissante_temperature, label=f'nb_glissant = {nb_glissant}')
	with open(f'Moyenne_temperature_glissate_{nb_glissant}.json','w') as jsonfile :
		jsonfile.write(json.dumps([temperature[0], Glissante_temperature], indent=4))
plt.legend()
plt.savefig("moyenne_glissante_temperature.png")
plt.clf()

for nb_glissant in range(1,5) :
	nb_glissant = nb_glissant * 3

	Glissante_humidite = []

	for i in range(len(humidite[0])) :
		somme = 0
		div = 0
		for j in range(nb_glissant) :
			if i+j >= len(humidite[0]) :
				maxi = i+j-len(humidite[0])
			else:
				maxi = i+j

			somme  = somme + 1/(j+2)*humidite[1][i-j] + 1/(j+2)*humidite[1][maxi]
			div = div + 2/(j+2)
		Glissante_humidite.append(somme/div)

	plt.plot(humidite[0], Glissante_humidite, label=f'nb_glissant = {nb_glissant}')
	with open(f'Moyenne_humidite_glissate_{nb_glissant}.json','w') as jsonfile :
		jsonfile.write(json.dumps([humidite[0], Glissante_humidite], indent=4))
plt.legend()
plt.savefig("moyenne_glissante_humidite.png")
plt.clf()