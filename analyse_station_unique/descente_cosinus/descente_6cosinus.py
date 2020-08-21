import json
from matplotlib import pyplot as plt
import numpy as np

delta = 10**(-3)
alpha = [1, 1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1]

with open('../json/temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('../json/humidite.json') as jsonfile :
	humidite = json.load(jsonfile)

dates = set()
for annee in temperature[0].keys() :
	for date in temperature[0][annee] :
		dates.add(date)
dates = list(dates)
dates.sort()


def fct_test(X, x) :
	return X[0] + X[1]*np.cos (2*np.pi*x + X[2]) + X[3]*np.cos(2*np.pi*x/365 + X[4]) + X[5]*np.cos (4*np.pi*x + X[6]) + X[7]*np.cos(4*np.pi*x/365 + X[8]) + X[9]*np.cos (6*np.pi*x + X[10]) + X[11]*np.cos(6*np.pi*x/365 + X[12])
	#X[0]*np.cos(2*np.pi*x + X[3]) + X[1]*np.cos(2*np.pi*x/365 + X[4]) + X[2] + X[5]*np.cos(4*np.pi*x + X[6])

def ecart_temperature(temperature_test) :
	ecarts_temperature = 0
	compt = 0
	for i_date in range(len(temperature_test[0])) :
		for annee in temperature[0].keys() :
			if temperature_test[0][i_date] in temperature[0][annee] :
				ecarts_temperature = ecarts_temperature + (temperature_test[1][i_date] - temperature[1][annee][temperature[0][annee].index(temperature_test[0][i_date])])**2
				compt += 1	
	return (ecarts_temperature/compt)**(1/2)


X = np.array([280 ,0.0 ,0.0,0.0,0.0,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
# C A phi1 B phi2 D phi3 E phi4
# Acos(w1t + phi1) + Bcos(w2t+phi2) + C + Dcos (w3t+phi3)
#w1 jour w2 annee W3 demi jour

drapeau = False
ecart_precedant = 0
while drapeau == False :
	val_actuel = []
	for date in dates :
		val_actuel.append(fct_test(X,date))
	val_actuel_ecart = ecart_temperature([dates,val_actuel])
	#if i == 0 :
	#	plt.plot(dates, val_actuel, label='init')
	dX = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
	for j in range(len(X)) :
		X_modif = X.copy()
		X_modif[j] = X_modif[j] + delta
		val_modif = []
		for date in dates :
			val_modif.append(fct_test(X_modif,date))
		val_modif_ecart = ecart_temperature([dates,val_modif])
		df = (val_modif_ecart - val_actuel_ecart)/delta
		dX[j] = - df * alpha[j]
	if abs (val_actuel_ecart - ecart_precedant) < 0.0001 :
		drapeau = True
	ecart_precedant = val_actuel_ecart
	X = X + dX
	X[2] = X[2]%(2*np.pi)
	X[4] = X[4]%(2*np.pi)
	X[6] = X[6]%(2*np.pi)
	X[8] = X[8]%(2*np.pi)
	X[10] = X[10]%(2*np.pi)
	X[12] = X[12]%(2*np.pi)
	#print(X)
	#if i%10 == 0 :
	#	print("{} sur 100".format(i))
	#	print(val_modif_ecart)
	#	print(" ")
print ("ecart")
print (val_actuel_ecart)
print ("dX")
print (dX)

for annee in temperature[0].keys() :
	temp = []
	jour = []
	for date2 in temperature[0][annee] :
		jour.append (date2)
		temp.append (temperature[1][annee][temperature[0][annee].index(date2)])
	plt.plot (jour, temp, label = annee) 


plt.plot(dates, val_actuel, label='final')
plt.legend()
plt.savefig("T6cos.png")
print ("X = [C, A, phi1, B, phi2, D, phi3, E, phi4], F, phi5, G, phi6")
print(X)


def ecart_humidite(humidite_test) :
	ecarts_humidite = 0
	compt = 0
	for i_date in range(len(humidite_test[0])) :
		for annee in humidite[0].keys() :
			if humidite_test[0][i_date] in humidite[0][annee] :
				ecarts_humidite = ecarts_humidite + (humidite_test[1][i_date] - humidite[1][annee][humidite[0][annee].index(humidite_test[0][i_date])])**2
				compt += 1	
	return (ecarts_humidite/compt)**(1/2)


X = np.array([70.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
# C A phi1 B phi2 D phi3 E phi4
# Acos(w1t + phi1) + Bcos(w2t+phi2) + C + Dcos (w3t+phi3)
#w1 jour w2 annee W3 demi jour

ecart_precedant = 0
drapeau = False
while drapeau == False :
	val_actuel = []
	for date in dates :
		val_actuel.append(fct_test(X,date))
	val_actuel_ecart = ecart_humidite([dates,val_actuel])
	#if i == 0 :
	#	plt.plot(dates, val_actuel, label='init')
	dX = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
	for j in range(len(X)) :
		X_modif = X.copy()
		X_modif[j] = X_modif[j] + delta
		val_modif = []
		for date in dates :
			val_modif.append(fct_test(X_modif,date))
		val_modif_ecart = ecart_humidite([dates,val_modif])
		df = (val_modif_ecart - val_actuel_ecart)/delta
		dX[j] = - df * alpha[j]

	if abs (val_actuel_ecart - ecart_precedant) < 0.0001 :
		drapeau = True
	ecart_precedant = val_actuel_ecart
	X = X + dX
	X[2] = X[2]%(2*np.pi)
	X[4] = X[4]%(2*np.pi)
	X[6] = X[6]%(2*np.pi)
	X[8] = X[8]%(2*np.pi)
	X[10] = X[10]%(2*np.pi)
	X[12] = X[12]%(2*np.pi)

	#print(X)
	#if i%10 == 0 :
	#	print("{} sur 100".format(i))
	#	print(val_modif_ecart)
	#	print(" ")
plt.clf()

print ("H")

print("ecart")
print (val_modif_ecart)
print ("dX")
print (dX)

for annee in humidite[0].keys() :
	humi = []
	jour = []
	for date2 in humidite[0][annee] :
		jour.append (date2)
		humi.append (humidite[1][annee][humidite[0][annee].index(date2)])
	plt.plot (jour, humi) 

plt.plot(dates, val_actuel, label='final')
plt.legend()
plt.savefig("H6cos.png")
print ("X = [C, A, phi1, B, phi2, D, phi3, E, phi4], F, phi5, G, phi6")
print(X)



