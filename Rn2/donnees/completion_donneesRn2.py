import json
import sys
from matplotlib import pyplot as plt

with open(sys.argv[1]) as jsonfile :
	donnee = json.load(jsonfile)

def CEstBon (jpp, annee, k):
	if not (jpp in donnee[0][annee]) :
		return False
	if donnee[k][annee][donnee[0][annee].index(jpp)] == 'mq':
		return False
	return True

date = [0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875]
donnee_propre = [dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict()]
for annee in donnee[0].keys() :

	donnee_propre[0][annee] = []
	for k in range(1,12):
		donnee_propre[k][annee] = []
	for j in range(int(max(donnee[0][annee]))+1) :
		for position in date :
			donnee_propre[0][annee].append(j+position)
			for k in range(1,12):
				if CEstBon ( j + position, annee, k):
					val = donnee[k][annee][donnee[0][annee].index(j+position)]
				else :
					if donnee_propre[k][annee] == []:
						prec = donnee_propre[k][str(int(annee)-1)][-1]
					else:
						prec = donnee_propre[k][annee][-1]
					ecart = 0
					while not CEstBon (j + position + 0.25 * ecart, annee, k) and (j + position + 0.25 * ecart) < 366 :
						ecart +=1
					if (j + position + 0.25 * ecart) >= 366 :
						suiv = donnee[k][str(int(annee)+1)][0]
					else:
						suiv = donnee[k][annee][donnee[0][annee].index(j + position + 0.25 * ecart)]
					val = float(prec) + (float(suiv) - float(prec))/ (ecart+1)	
				
				donnee_propre[k][annee].append(val)

with open(sys.argv[2],'w') as jsonfile :
	json.dump(donnee_propre,jsonfile,indent = 4)



#for annee in donnee_propre[0] :
#	plt.plot(donnee_propre[0][annee], donnee_propre[1][annee], label=annee)
#	plt.legend()
#	plt.show()
#	plt.clf()