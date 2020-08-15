import json
from matplotlib import pyplot as plt
import numpy as np

with open('../temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

	annees = []
	moyennes = []

	for annee in temperature[0].keys() :
		annees.append (annee)
		somme = 0
		for date in temperature[0][annee] :
			somme += temperature[1][annee][temperature[0][annee].index(date)]
		moyennes.append (somme / len(temperature[0][annee]) )

plt.plot (annees, moyennes)
plt.savefig ("result.png")