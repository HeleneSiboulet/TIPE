import json
from matplotlib import pyplot as plt
import numpy as np
import random as rd

delta = 10**(-3)
alpha = [0.01, 0.01, 0.01, 0.01]

with open('../json/temperatureTest.json') as jsonfile :
	temperature = json.load(jsonfile)


def fct_test(X, x, deb) :
	return X[0]*(x - deb) + X[1] + X[2]*np.cos(2*np.pi*x + X[3])

def ecart_temperature(temperature_test, temperature_reference) :
	ecarts_temperature = 0
	compt = 0
	for i_date in range(len(temperature_test[0])) :
		if temperature_test[0][i_date] in temperature_reference[0] :
			ecarts_temperature += ((temperature_test[1][i_date] - temperature_reference[1][temperature_reference[0].index(temperature_test[0][i_date])])*(i_date + 7)/7)**2
			compt += 1	
	return (ecarts_temperature/compt)**(1/2)

compt = 0
longueur = 7
ecart = np.zeros(13)


for tour in range (100) :
	debut = rd.randint (0,351) + rd.randint(0,8) * 1/8
	if debut in temperature[0]["2019"] and (debut + longueur) in temperature[0]["2019"] and (debut + 2*longueur) in temperature[0]["2019"] :
		ideb = temperature[0]["2019"].index(debut)
		imili = temperature[0]["2019"].index(debut + longueur) + 1
		ifin = temperature[0]["2019"].index(debut + 2*longueur) + 1
		temperature_reference = [temperature[0]["2019"][ideb:imili], temperature[1]["2019"][ideb:imili]]

		X = np.array([0.0,285.13810537,3.75735475,2.47218])
		# At + B + C cos (wt + phi)

		drapeau = False
		ecart_precedant = 0
		while drapeau == False :
			val_actuel = []
			for date in temperature_reference [0] :
				val_actuel.append(fct_test(X,date,debut))
			val_actuel_ecart = ecart_temperature([temperature_reference [0],val_actuel], temperature_reference)
			dX = np.array([0.0,0.0,0.0,0.0])
			for j in range(len(X)) :
				X_modif = X.copy()
				X_modif[j] = X_modif[j] + delta
				val_modif = []
				for date in temperature_reference [0] :
					val_modif.append(fct_test(X_modif,date,debut))
				val_modif_ecart = ecart_temperature([temperature_reference [0],val_modif], temperature_reference)
				df = (val_modif_ecart - val_actuel_ecart)/delta
				dX[j] = - df * alpha[j]
			X = X + dX
			X[3] = X[3]%(2*np.pi)
			if abs (val_actuel_ecart - ecart_precedant) < 0.0000001 :
				drapeau = True
			#print (val_actuel_ecart)
			ecart_precedant = val_actuel_ecart


		temperature_obs = [temperature[0]["2019"][imili:ifin], temperature[1]["2019"][imili:ifin]]
		for i in range (13) :
			decalage = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 2, 3, 4, 5, 6]
			if (debut + longueur + decalage[i]) in temperature_obs[0] :
				ecart[i] = ecart[i] + (temperature_obs[1][temperature_obs[0].index (debut + longueur + decalage[i])] - fct_test (X, (debut + longueur + decalage[i]), debut)) ** 2
		#	print (ecart)
		compt += 1
		# print (compt)

ET = np.zeros(13)
for i in range (13) :
	ET [i] = (ecart[i] / compt) ** (1/2)
print (ET)





