import os
li = os.listdir()
liste_tableau = []
station = {}
for nom in li :
	print(str(li.index(nom)) + " " + str(len(li)))
	if nom[-3:] == "csv" :
		with open(nom,'r') as csvfile :
			lignes = csvfile.readlines()
			for ligne in lignes[1:] :
				carac = ligne.split(';')
				if carac[0] in station.keys() :
					station[carac[0]] = station[carac[0]] + ligne
				else :
					station[carac[0]] = lignes[0] + ligne

for clef in station.keys() :
	with open(f'sortie/{clef}.csv','w') as csvfile :
		csvfile.write(station[clef])