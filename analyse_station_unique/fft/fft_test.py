import numpy as np
import json
from matplotlib import pyplot as plt

with open('../../json/temperature.json') as jsonfile :
	temperature = json.load(jsonfile)

with open('../../json/humidite.json') as jsonfile :
	humidite = json.load(jsonfile)

temp = []
humi = []
for annee in temperature[1].keys() :
	temp = temp + temperature[1][annee]
	humi = humi + humidite[1][annee]


Y = np.fft.fft(temp - np.mean(temp) + 0.001)
freq = np.fft.fftfreq(len(temp), d = temperature[0]["1996"][1] - temperature[0]["1996"][0])

print (freq [0])
print (Y[0])

lY = np.log(Y)
maxY = max(lY)
f = list(lY).index(maxY)
print(1/freq[f])
print(Y[f])

plt.plot(freq,lY)


plt.savefig("fftT.png")
plt.show()
plt.clf()

#plt.plot(1/freq[10:50]/365, lY[10:50])
#plt.show()
#with open("fftT.csv",'w') as csvfile :
#	texte = ""
#	texte = texte + '"frequence";"amplitude";"logAmplitude";"amplitudePhase";"logAmplitudePhase"\n'
#	for k in range(len(freq)) :
#		texte = texte + f"{freq[k]};{np.real(Y[k])};{np.real(lY[k])};{np.imag(Y[k])};{np.imag(lY[k])}\n"
#	texte = texte.replace(".",",")
#	csvfile.write(texte)

plt.clf ()

Y2 = np.fft.fft(humi - np.mean(humi) + 0.001 )
freq2 = np.fft.fftfreq(len(humi), d = humidite[0]["1996"][1] - humidite[0]["1996"][0])

lY2 = np.log(Y2)
maxY2 = max(lY2)
f2 = list(lY2).index(maxY2)
#print(1/freq2[f])
#print(Y2[f])

#print (temp)
#print (freq2)
#print (humi)

plt.plot(freq2,lY2)

plt.savefig("fftH.png")
plt.plot(freq2,lY2)
#plt.show()

with open("fftH.csv",'w') as csvfile :
	texte = ""
	texte = texte + '"frequence";"amplitude";"logAmplitude";"amplitudePhase";"logAmplitudePhase"\n'
	for k in range(len(freq2)) :
		texte = texte + f"{freq2[k]};{np.real(Y2[k])};{np.real(lY2[k])};{np.imag(Y2[k])};{np.imag(lY2[k])}\n"
	texte = texte.replace(".",",")
	csvfile.write(texte)

