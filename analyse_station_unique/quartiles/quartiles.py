import json
import numpy as np

with open('../json/temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('../json/humidite.json') as jsonfile :
	humidite = json.load(jsonfile)

temp = []

for annee in temperature[1].keys () :
	for t in temperature [1][annee] :
		temp. append (t)

temp.sort()

Q1t = temp [int (0.25 * len (temp)) ] - 273.15
met = temp [int (0.5 * len (temp)) ] - 273.15
Q3t = temp [int (0.75 * len (temp)) ] - 273.15

tempe = np.array (temp)

mot = tempe.mean() - 273.15
et = np.nanstd(tempe)


print ( "Q1t = " + str (Q1t)+ "  met = " + str (met) +  "  Q3t = " + str (Q3t) + "  mot =" + str (mot) + "  et =" +str(et) )

hum = []

for annee in humidite[1].keys () :
	for t in humidite [1][annee] :
		hum. append (t)

hum.sort()

Q1h = hum [int (0.25 * len (hum)) ]
meh = hum [int (0.5 * len (hum)) ]
Q3h = hum [int (0.75 * len (hum)) ]

humi = np.array(hum)

moh = humi.mean()
eh = np.nanstd (humi)

print ( "Q1h = " + str (Q1h)+ "  meh = " + str (meh) +  "  Q3h = " + str (Q3h) + "  moh =" + str (moh) + "  eh =" +str(eh) )


