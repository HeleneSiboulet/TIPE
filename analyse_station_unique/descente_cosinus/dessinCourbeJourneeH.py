import numpy as np
import json
from matplotlib import pyplot as plt



with open('../json/humidite.json') as jsonfile :
	temperature = json.load(jsonfile)


s = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
compt = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
r = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

for annee in temperature[0].keys() :
	for date in temperature[0][annee] :
		i1 = (date - int(date) )* 8
		#print (i1)
		i = int (i1)
		compt[i] += 1
		s [i] += temperature[1][annee][temperature[0][annee].index(date)]

for j in range (len (s)) :
	r[j] = (s[j] / compt[j])

mesure = [1,2,3,4,5,6,7,8]


f = []
g = []
h = []
for m in mesure :
	pf = 12.73536399*np.cos(2*np.pi*(m-1)/8 + 5.61376937) +71.15758689
	f .append (pf)
	pg = 71.15503638 + 12.90397869*np.cos(2*np.pi*(m-1)/8 + 5.62646828) -2.70175487 *np.cos(4*np.pi*(m-1)/8 + 5.69268334)
	g .append (pg) 
	ph = 71.1553131 + 12.95354558*np.cos(2*np.pi*(m-1)/8 + 5.62648561 ) - 2.72510888 *np.cos(4*np.pi*(m-1)/8 + 5.66712864) + -0.16110029 *np.cos(4*np.pi*(m-1)/8 + 6.21532372)
	h.append (ph)
#print (str (r))
plt.plot (mesure, r, label = "moyenne")
plt.plot (mesure, f, label = "f")
plt.plot (mesure, g, label = "g")
plt.plot (mesure, h, label = "h")

plt.legend()
plt.savefig("moyenne_sur_la_journeeH.png")
