from datetime import datetime
import pandas as pd
import sys
from matplotlib import pyplot as plt
import json
import numpy as np

origine_temps = datetime(1996,1,1)

with open(sys.argv[1],'r') as csvfile :
	donnees = pd.read_csv(csvfile, sep=";", low_memory = False)

Temps = {}

TypeDonnees = ["pmer", "tend", "cod_tend", "dd", "ff", "t", "td", "u", "vv", "pres", "rr3"]
ValeurDonnees = [""] * 11
ListeDonnees = [{},{},{},{},{},{},{},{},{},{},{}]

donnees = donnees.sort_values(by=['date'])
donnees = donnees.reset_index(drop=True)

for i in range(0,len(donnees["numer_sta"])) :
	date = datetime.strptime(str(donnees["date"][i]),'%Y%m%d%H%M%S')
	for j in range (11):
		val = donnees[TypeDonnees[j]][i]
		if val == 'mq':
			ValeurDonnees[j] = 'mq'
		else :
			ValeurDonnees[j] = str(donnees[TypeDonnees[j]][i])

	annee = date.strftime("%Y")
	if annee != "2008" and annee != "2020" and annee != "2019" :
		dt = date - datetime(int(annee), 1, 1)

		
		dt = int(dt.days) + int(dt.seconds)/3600/24

		if annee in Temps.keys() :
			Temps[annee].append(dt)
			for j in range (11) :
				if ValeurDonnees[j] == 'mq' :
					ListeDonnees[j][annee].append('mq')
				else :
					ListeDonnees[j][annee].append(float(ValeurDonnees[j]))
		else :
			Temps[annee] = [dt]
			for j in range (11) :
				if ValeurDonnees[j] == 'mq' :
					ListeDonnees[j][annee] = ['mq'] 
				else :
					ListeDonnees[j][annee] = [float(ValeurDonnees[j])]


with open('donnees.json','w') as jsonfile :
	jsonfile.write(json.dumps([Temps, ListeDonnees], indent=4))




