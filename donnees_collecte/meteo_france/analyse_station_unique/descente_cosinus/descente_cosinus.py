import json
from matplotlib import pyplot as plt
import numpy as np

delta = 10**(-3)
alpha = [1, 1, 1, 1, 0.1, 0.1, 0.1]

with open('../ancienne_bdd/totale/temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('../ancienne_bdd/totale/humidite.json') as jsonfile :
	humidite = json.load(jsonfile)

dates = set()
for annee in temperature[0].keys() :
	for date in temperature[0][annee] :
		dates.add(date)
dates = list(dates)
dates.sort()


def fct_test(X, x) :
	return X[0]*np.cos(2*np.pi*x + X[4]) + X[1]*np.cos(2*np.pi*x/365 + X[5]) + X[2]*np.cos(4*np.pi*x + X[6]) + X[3]

def ecart_temperature(temperature_test) :
	ecarts_temperature = 0
	compt = 0
	for i_date in range(len(temperature_test[0])) :
		for annee in temperature[0].keys() :
			if temperature_test[0][i_date] in temperature[0][annee] :
				ecarts_temperature = ecarts_temperature + (temperature_test[1][i_date] - temperature[1][annee][temperature[0][annee].index(temperature_test[0][i_date])])**2
				compt += 1	
	return (ecarts_temperature/compt)**(1/2)


X = np.array([2.0,10.0,0.0,285.0,0.0,0.0,0.0])
# A,B,C,D,phi1,phi2,phi3
# Acos(w1t + phi1) + Bcos(w2t+phi2) + Ccos(w3t+phi3) + D
#w1 jour w2 annee w3 demi-journee

for i in range(100) :
	val_actuel = []
	for date in dates :
		val_actuel.append(fct_test(X,date))
	val_actuel_ecart = ecart_temperature([dates,val_actuel])
	if i == 0 :
		plt.plot(dates, val_actuel, label='init')
	dX = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0])
	for j in range(len(X)) :
		X_modif = X.copy()
		X_modif[j] = X_modif[j] + delta
		val_modif = []
		for date in dates :
			val_modif.append(fct_test(X_modif,date))
		val_modif_ecart = ecart_temperature([dates,val_modif])
		df = (val_modif_ecart - val_actuel_ecart)/delta
		dX[j] = - df * alpha[j]
	X = X + dX
	X[4] = X[4]%(2*np.pi)
	X[5] = X[5]%(2*np.pi)
	X[6] = X[6]%(2*np.pi)
	#print(X)
	if i%10 == 0 :
		print("{} sur 100".format(i))
		print(val_modif_ecart)
		print(" ")

plt.plot(dates, val_actuel, label='final')
plt.legend()
plt.savefig("result.png")
print(X)



