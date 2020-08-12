import numpy as np
import json
from matplotlib import pyplot as plt

with open('temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('humidite.json') as jsonfile :
	humidite = json.load(jsonfile)

temp = []
humi = []
for annee in temperature[1].keys() :
	temp = temp + temperature[1][annee]
	humi = humi + humidite[1][annee]


Y = np.fft.fft(temp - np.mean(temp))
freq = np.fft.fftfreq(len(temp), d = temperature[0]["1996"][1] - temperature[0]["1996"][0])

lY = np.log(Y)
maxY = max(lY)
f = list(lY).index(maxY)
print(1/freq[f])
print(Y[f])

plt.plot(freq,lY)


plt.show()