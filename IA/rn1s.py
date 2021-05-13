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

def convertisseur_date(dt) :
	angle = dt*2*np.pi/366
	return np.cos(angle), np.sin(angle)

def convertisseur_heure(dt):
	angle = dt*2*np.pi
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
		cdt,sdt = convertisseur_date(temperature[0][i][j])
		ch,sh = convertisseur_heure(temperature[0][i][j])
		temperature_continu.append([(float(i) - ma)/sta,cdt,sdt,ch,sh,(temperature[1][i][j]- mt)/stt, (humidite[1][i][j]- mh)/sth])

temperature_continu = torch.tensor(temperature_continu).double()

longueur_apprentissage = 8*7*3
longueur_prevision = 8*7


import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import time
from matplotlib import pyplot as plt
import random


class Net(nn.Module) :

    def __init__(self) :
        super(Net, self).__init__()            
        self.fc1 = nn.Linear(7*longueur_apprentissage, 6*longueur_apprentissage).double()
        self.fc2 = nn.Linear(6*longueur_apprentissage, 3*longueur_apprentissage).double()
        self.fc3 = nn.Linear(3*longueur_apprentissage, 2*longueur_apprentissage).double()
        self.fc4 = nn.Linear(2*longueur_apprentissage, 2*longueur_prevision).double()
        self.prelu1 = nn.PReLU().double()
        self.prelu2 = nn.PReLU().double()
        self.prelu3 = nn.PReLU().double()

    def forward(self, x) :
        x = self.prelu1(self.fc1(x))
        x = self.prelu2(self.fc2(x))
        x = self.prelu3(self.fc3(x))
        x = self.fc4(x)
        return x


net = Net()
criterion = nn.MSELoss()	#critère de distance
optimizer = optim.Adam(net.parameters(), lr=10**(-3))
index_test = []
for i in range(longueur_apprentissage, len(temperature_continu) - longueur_prevision) :
	index_test.append(i)

nb_tour_apprentissage = 1000

for tour in range(nb_tour_apprentissage) :
	optimizer.zero_grad()
	batch_source = []
	batch_target = 0
	for j in range(200) :
		i = random.choice(index_test)
		batch_source.append(temperature_continu[i-longueur_apprentissage:i].view(1,-1))	
		target = temperature_continu[i][5]
		target = target.unsqueeze(0)
		for k in range(1,longueur_prevision) :
			target = torch.cat([target,temperature_continu[i+k][5].unsqueeze(0)])
		for k in range(longueur_prevision) :
			target = torch.cat([target,temperature_continu[i+k][6].unsqueeze(0)])
		target = target.unsqueeze(0)
		try :
			batch_target = torch.cat([batch_target,target],0) 
		except :
			batch_target = target
	source = torch.cat(batch_source,0)
	target = batch_target
	#print(source.size())
	out = net(source)
	loss = criterion(out,target)	
	loss.backward()		
	optimizer.step()
	#print(tour/100)


taille = len(temperature_test[0]["2019"])
ecart= torch.tensor(np.zeros([1,2*longueur_prevision]))	
compt = 0
nb_tour = 5000

for tour in range(nb_tour) :
	i = rd.randint (0, taille - longueur_prevision - longueur_apprentissage)
	entre = []
	sortie = []
	for j in range(longueur_apprentissage) :
		an = (2019.0 - ma)/sta
		cdt,sdt = convertisseur_date(temperature_test[0]["2019"][(j+i)%taille])
		ch,sh = convertisseur_heure(temperature_test[0]["2019"][(j+i)%taille])	
		tp = (temperature_test[1]["2019"][(j+i)%taille] - mt)/stt
		hm = (humidite_test[1]["2019"][(j+i)%taille] - mh)/sth
		entre.append([an,cdt,sdt,ch,sh,tp,hm])
	sortie.append((torch.tensor(temperature_test[1]["2019"][i + longueur_apprentissage:i + longueur_apprentissage + longueur_prevision]) - mt)/stt)
	sortie.append((torch.tensor(humidite_test[1]["2019"][i + longueur_apprentissage:i + longueur_apprentissage + longueur_prevision]) - mh)/sth)
	entre = torch.tensor(entre).double().view(1,-1)
	sortie = torch.cat(sortie)
	rep = net(entre)
	ecart = ecart + (rep - sortie)**2	


ETt = ( ( ecart.view(2,longueur_prevision)[0] / nb_tour) ** (1/2) * stt ).view(int (longueur_prevision/8),8)
ETh = ( ( ecart.view(2,longueur_prevision)[1] / nb_tour) ** (1/2) * sth ).view(int (longueur_prevision/8),8)
print ("ETt = " + str (ETt))
print ("ETh = " + str (ETh))

torch.save(net.state_dict(), "./net1s.nn")
