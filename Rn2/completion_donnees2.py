import json
import sys
from matplotlib import pyplot as plt

with open(sys.argv[1]) as jsonfile :
	donnee = json.load(jsonfile)

date = [0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875]
donnee_propre = [dict(),dict()]
for annee in donnee[0].keys() : 
	donnee_propre[0][annee] = []
	donnee_propre[1][annee] = []
	for j in range(int(max(donnee[0][annee]))+1) :
		for position in date :
			donnee_propre[0][annee].append(j+position)
			if j+position in donnee[0][annee] :
				donnee_propre[1][annee].append(donnee[1][annee][donnee[0][annee].index(j+position)])
			else : 
				pred = donnee_propre[1][annee][-1]
				ind = -2
				cherche = donnee_propre[0][annee][ind]
				while cherche not in donnee[0][annee] :
					ind -= 1
					cherche = donnee_propre[0][annee][ind]
				index = donnee[0][annee].index(donnee_propre[0][annee][ind])
				if index+1 < len(donnee[1][annee]) :
					succ = donnee[1][annee][index+1]
					val = (succ - pred)/(donnee[0][annee][index+1] - donnee[0][annee][index])*(j+position-donnee[0][annee][index]) + pred
				else :
					succ = donnee[1][str(int(annee) + 1)][0]
					val = (succ - pred)/(donnee[0][str(int(annee) + 1)][0] - donnee[0][annee][index])*(j+position-donnee[0][annee][index]) + pred
				donnee_propre[1][annee].append(val)

with open(sys.argv[2],'w') as jsonfile :
	json.dump(donnee_propre,jsonfile,indent = 4)


#for annee in donnee_propre[0] :
#	plt.plot(donnee_propre[0][annee], donnee_propre[1][annee], label=annee)
#	plt.legend()
#	plt.show()
#	plt.clf()