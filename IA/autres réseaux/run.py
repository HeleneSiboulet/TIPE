import json
import torch
import numpy as np

with open("./donnees/temperature.json") as jsonfile :
	temperature = json.load(jsonfile)

with open("./donnees/temperatureTest.json") as jsonfile :
	temperature_test = json.load(jsonfile)

with open("./donnees/humidite.json") as jsonfile :
	humidite = json.load(jsonfile)

with open("./donnees/humiditeTest.json") as jsonfile :
	humidite_test = json.load(jsonfile)

def convertiseur_date(dt) :
	angle = dt/366*2*np.pi
	return np.cos(angle), np.sin(angle)

temperature_continu = []
annee = []
temp = []
for i in temperature[0].keys() :
	for j in range(len(temperature[0][i])) :
		annee.append(float(i))
		temp.append(temperature[1][i][j])  #enlever les clés
	
annee = torch.tensor(annee)
temp = torch.tensor(temp)
ma = float(torch.mean(annee))
sta = float(torch.std(annee)) #ecart type
mt = float(torch.mean(temp))
stt = float(torch.std(temp))
for i in temperature[0].keys() :
	for j in range(len(temperature[0][i])) :
		cdt,sdt = convertiseur_date(temperature[0][i][j])
		temperature_continu.append([(float(i) - ma)/sta,cdt,sdt,(temperature[1][i][j]- mt)/stt])

#print(temperature_continu)

longueur = 8*7


import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import time
from matplotlib import pyplot as plt
import random


class Net(nn.Module) :

    def __init__(self) :
        super(Net, self).__init__()            #appel init de nn module
        self.fc1 = nn.Linear(224, 56).double() #ajout de fcc1 à la ft.   224 valeurs (annee, sin, cos, temp) en une semaine, 56 mesure
        self.fc2 = nn.Linear(56, 56).double()
        self.fc3 = nn.Linear(56, 8).double()  #sortie : temp d'une journee
        self.prelu1 = nn.PReLU().double()
        self.prelu2 = nn.PReLU().double()

    def forward(self, x) :
        x = self.prelu1(self.fc1(x))
        x = self.prelu2(self.fc2(x))
        x = self.fc3(x)
        return x


#print('\n\n\n')

net = Net()
criterion = nn.MSELoss()	#critère de distance
optimizer = optim.Adam(net.parameters(), lr=10**(-3))
print(net)
index_test = []	#liste d'indice d'ordre aléatoire
for i in range(longueur, len(temperature_continu) - 8) :
	index_test.append(i)

for tour in range(1000) :
	optimizer.zero_grad()	#initialise pts de départ du gradient pour ce tour
	batch_source = []
	batch_target = []
	for j in range(20) :
		i = random.choice(index_test)
		batch_source.append(torch.tensor(temperature_continu[i-longueur:i]).double().view(1,-1))	#view : mettre ds une matrie de "1" colonne
		target = []
		for k in range(i, i+8) :
			target.append(temperature_continu[k][3])
		batch_target.append(torch.tensor(target).double().unsqueeze(0)) #unsqueeze rajoute une dimension
	source = torch.cat(batch_source,0)	#cat : concaténation de tenseurs colonne -> grille
	target = torch.cat(batch_target,0)

	out = net(source)
	#print(out)
	#print(target)
	loss = criterion(out,target)	#criterion renvoie les pertes et le gradient
	#print(loss)
	loss.backward()		#rétropropagation
	optimizer.step()
	if tour % 100 == 0 :
		print(tour/100000)
		print(loss)
	#print('\n\n')


taille = len(temperature_test[0]["2019"])
X = []
Y_reel = []
Y = []
dX = []
dY = []
for i in range(0,taille,8) :
	entre = []
	sortie = []
	for j in range(56) :
		an = (2019.0 - ma)/sta
		cdt,sdt = convertiseur_date(temperature_test[0]["2019"][(j+i)%taille])	#à coller avec début 2020
		tp = (temperature_test[1]["2019"][(j+i)%taille] - mt)/stt
		entre.append([an,cdt,sdt,tp])
	for j in range(8) :
		sortie.append((temperature_test[1]["2019"][(j+i+56)%taille]- mt)/stt)
		X.append(temperature_test[0]["2019"][(j+i+56)%taille])
	entre = torch.tensor(entre).double().view(1,-1)
	sortie = torch.tensor(sortie).double()
	rep = net(entre)
	Y = Y + list(rep[0])
	Y_reel = Y_reel + list(sortie)
	dY.append(criterion(rep,sortie))
	dX.append(temperature_test[0]["2019"][(i+56)%taille])


torch.save(net.state_dict(), "./net.nn")

plt.plot(X,Y,label='simu')
plt.plot(X,Y_reel,label='reel')
plt.legend()
plt.savefig("prediction.png")
plt.show()
plt.clf()
plt.plot(dX, dY)
plt.savefig("differencejour.png")

with open("rep.csv",'w') as csvfile : 
	csvfile.write('"date";"Reel";"Simule"\n')
	for i in range(len(X)) :
		csvfile.write(f'{X[i]};{Y_reel[i]*stt+mt};{Y[i]*stt+mt}\n'.replace(".",","))