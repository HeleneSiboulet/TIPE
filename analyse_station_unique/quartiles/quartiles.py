import json
import numpy as np

with open('../temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('../humidite.json') as jsonfile :
	humidite = json.load(jsonfile)

temp = []

for annee in temperature[1].keys () :
	for t in temperature [1][annee] :
		temp. append (t)

temp.sort()

Q1t = temp [int (0.25 * len (temp)) ] - 273.15
Q3t = temp [int (0.75 * len (temp)) ] - 273.15

print ( "Q1t = " + str (Q1t)+ "  Q2t = " + str (Q3t))

hum = []

for annee in humidite[1].keys () :
	for t in humidite [1][annee] :
		hum. append (t)

hum.sort()

Q1h = hum [int (0.25 * len (hum)) ]
Q3h = hum [int (0.75 * len (hum)) ]

print ( "Q1h = " + str (Q1h)+ "  Q2h = " + str (Q3h))