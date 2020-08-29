import json
import torch
import numpy as np
import random as rd

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

humidite_continu = []
annee = []
humi = []
for i in humidite[0].keys() :
	for j in range(len(humidite[0][i])) :
		annee.append(float(i))
		humi.append(humidite[1][i][j])
	
annee = torch.tensor(annee)
temp = torch.tensor(temp)
humi = torch.tensor (humi)
ma = float(torch.mean(annee))
sta = float(torch.std(annee)) #ecart type
mt = float(torch.mean(temp))
stt = float(torch.std(temp))
mh = float(torch.mean(humi))
sth = float(torch.std(humi))
for i in temperature[0].keys() :
	for j in range(len(temperature[0][i])) :
		cdt,sdt = convertiseur_date(temperature[0][i][j])
		temperature_continu.append([(float(i) - ma)/sta,cdt,sdt,(temperature[1][i][j]- mt)/stt, (humidite[1][i][j]- mh)/sth])


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
        self.fc1 = nn.Linear(280, 112).double() #ajout de fcc1 à la ft   224 valeurs (annee, sin, cos, temp) en une semaine, 56 mesure
        self.fc2 = nn.Linear(112, 112).double()
        self.fc3 = nn.Linear(112, 16).double()  #sortie : temp d'une journee
        self.prelu1 = nn.PReLU().double()
        self.prelu2 = nn.PReLU().double()

    def forward(self, x) :
        x = self.prelu1(self.fc1(x))
        x = self.prelu2(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()
criterion = nn.MSELoss()	#critère de distance
optimizer = optim.Adam(net.parameters(), lr=10**(-3))
index_test = []
for i in range(longueur, len(temperature_continu) - 8) :
	index_test.append(i)

for tour in range(50000) :
	optimizer.zero_grad()	#initialise pts de départ du gradient pour ce tour
	batch_source = []
	batch_target = []
	for j in range(50) :
		i = random.choice(index_test)
		batch_source.append(torch.tensor(temperature_continu[i-longueur:i]).double().view(1,-1))	#view : mettre ds une matrie de "1" colonne
		target = []
		for k in range(i, i+8) :
			target.append(temperature_continu[k][3])
		for k in range(i, i+8) :
			target.append (temperature_continu[k][4])
		batch_target.append(torch.tensor(target).double().unsqueeze(0)) #unsqueeze rajoute une dimension
	source = torch.cat(batch_source,0)	#cat : concaténation de tenseurs colonne -> grille
	target = torch.cat(batch_target,0)
	out = net(source)
	loss = criterion(out,target)	#criterion renvoie les pertes et le gradient
	loss.backward()		#rétropropagation
	optimizer.step()


taille = len(temperature_test[0]["2019"])
ecart= torch.tensor(np.zeros([1,16]))	
compt = 0
nb_tour = 1000

for tour in range(nb_tour) :
	i = rd.randint (0, taille - 8)
	entre = []
	sortie = []
	for j in range(56) :
		an = (2019.0 - ma)/sta
		cdt,sdt = convertiseur_date(temperature_test[0]["2019"][(j+i)%taille])	#à coller avec début 2020
		tp = (temperature_test[1]["2019"][(j+i)%taille] - mt)/stt
		hm = (humidite_test[1]["2019"][(j+i)%taille] - mh)/sth
		entre.append([an,cdt,sdt,tp,hm])
	for j in range(8) :
		sortie.append((temperature_test[1]["2019"][(j+i+56)%taille]- mt)/stt)
	for j in range(8) :
		sortie.append((humidite_test[1]["2019"][(j+i+56)%taille]- mh)/sth)
	entre = torch.tensor(entre).double().view(1,-1)
	rep = net(entre)
	ecart = ecart + (rep - torch.tensor(sortie).unsqueeze(0))**2

#print (ecart.view(2,8)[0])
ETt = ( ecart.view(2,8)[0] / nb_tour) ** (1/2) * stt
ETh = ( ecart.view(2,8)[1] / nb_tour) ** (1/2) * sth
print ("ETt = " + str (ETt))
print ("ETh = " + str (ETh))
