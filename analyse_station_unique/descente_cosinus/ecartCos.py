import json
import numpy as np

with open('../json/temperatureTest.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('../json/humiditeTest.json') as jsonfile :
	humidite = json.load(jsonfile)



ecartf = 0
ecartg = 0
ecarth = 0
compt = 0
for annee in temperature[0].keys() :
	for date in temperature[0][annee] :
		mesure = temperature[1][annee][temperature[0][annee].index(date)]
		f =	-3.75735475*np.cos(2*np.pi*date + 5.61376937) + 285.13810537 -8.37900126*np.cos(2*np.pi*date/365 + 5.95629115)
		g = 2.85138181e+02 + -3.77024667e+00*np.cos(2*np.pi*date + 5.61243708e+00) + 6.64813028e-01 *np.cos(4*np.pi*date + 6.19368036e+00) -8.39742026e+00*np.cos(2*np.pi*date/365 + 5.95627061e+00) -3.56389400e-02 *np.cos(4*np.pi*date/365 + 6.61334074e-03)
		h = 2.85138253e+02 + -3.77025815e+00*np.cos(2*np.pi*date + 5.61243713e+00 ) + 6.64829296e-01 *np.cos(4*np.pi*date + 6.19366499e+00) + 8.58689428e-02 *np.cos(4*np.pi*date + 6.27803532e+00) -8.39738900e+00*np.cos(2*np.pi*date/365 + 5.95626734e+00 ) -3.55282083e-02 *np.cos(4*np.pi*date/365 + 6.59654426e-03) -7.80736324e-02*np.cos(4*np.pi*date/365 + 6.27876991e+00)
		ecartf += (f - mesure)**2
		ecartg += (g - mesure)**2
		ecarth += (h - mesure)**2
		compt += 1

ef = (ecartf/compt)** (1/2)
eg = (ecartg/compt)** (1/2)
eh = (ecarth/compt)** (1/2)
print ("T")
print("ecart f : " + str(ef) + "°C")
print("ecart g : " + str(eg) + "°C")
print("ecart h : " + str(eh) + "°C")
