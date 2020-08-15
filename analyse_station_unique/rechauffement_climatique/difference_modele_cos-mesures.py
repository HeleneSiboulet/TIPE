import json
from matplotlib import pyplot as plt
import numpy as np

with open('../temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

	X = []
	Y = []

	for annee in temperature[0].keys() :
		for date in temperature[0][annee] :
			X.append(date + 365 * (int (annee) - 1996))
			#prevision = -3.79735387 * cos ( (2* np.pi) + 5.61085748 ) + 8.43455708 * cos ( (2* np.pi)/365 + 2.81469217 ) + 285.13820904
			#prevision ave 2 cosinus
			prevision = -3.79715097 * np.cos ( (2* np.pi) * date + 5.61080193 ) + 8.43465995 * np.cos ( ((2* np.pi)/365) * date + 2.81468304 ) + 0.69543303 * np.cos ( 4 * np.pi * date + 6.09790539 ) + 285.13823784 
			mesure = temperature[1][annee][temperature[0][annee].index(date)]
			Y.append (mesure - prevision)	

plt.plot (X,Y)
plt.savefig ("resultat2.png")
