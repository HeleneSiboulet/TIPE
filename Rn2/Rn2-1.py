import json
import torch
import numpy as np
import random as rd

with open("./donnees/donneesCompletees.json") as jsonfile :
	donnees = json.load(jsonfile)

with open("./donnees/donneesTestCompletees.json") as jsonfile :
	donnees_test = json.load(jsonfile)

print (donnees[0]["1996"][-1])

def convertiseur_date(dt) :
	angle = dt*2*np.pi/366
	return np.cos(angle), np.sin(angle)

def convertiseur_heure(dt):
	angle = dt*2*np.pi
	return np.cos(angle), np.sin(angle)

entrees_rn = []
annee = []
do = [ [],[],[],[],[],[],[],[],[],[],[],[] ]

for i in donnees[0].keys() :
	for j in range(len(donnees[0][i])) :
		annee.append(float(i))
		for k in range (12):
			do[k].append(donnees[k][i][j])
0
annee = torch.tensor(annee)

for k in range (12):
	do[k] = torch.tensor(do[k])

moyennes = []
ecart_type = []
for k in range (12):
	moyennes.append(float(torch.mean(do[k])))
	ecart_type.append(float(torch.std(do[k])))

ma = float(torch.mean(annee))
sta = float(torch.std(annee))

for i in donnees[0].keys() :
	for j in range(len(donnees[0][i])) :
		cdt,sdt = convertiseur_date(donnees[0][i][j])
		ch,sh = convertiseur_heure(donnees[0][i][j])
		liste = [(float(i) - ma)/sta,cdt,sdt,ch,sh]
		for k in [6,8] :
			liste.append((donnees[k][i][j] - moyennes[k]) / ecart_type[k] )
		#for k in range (1,12):
		#	if k != 4 :
		#		liste.append((donnees[k][i][j] - moyennes[k]) / ecart_type[k] )
		#	else :
		#		liste.append(np.cos ( donnees[k][i][j] * 2 * np.pi / 360 ))
		#		liste.append(np.sin ( donnees[k][i][j] * 2 * np.pi / 360 ))
		entrees_rn.append(liste)



longueurEntree = 7*8
longueurSortie = 1*8


import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import time
from matplotlib import pyplot as plt
import random


class Net(nn.Module) :

    def __init__(self) :
        super(Net, self).__init__()            
        self.fc1 = nn.Linear(longueurEntree * 7, longueurEntree * 9).double()
        self.fc2 = nn.Linear(longueurEntree * 9, longueurSortie * 20).double()
        self.fc3 = nn.Linear(longueurSortie * 20, longueurSortie * 2).double()
        self.fc4 = nn.Linear(longueurSortie * 6, longueurSortie * 2).double()
        self.prelu1 = nn.PReLU().double()
        self.prelu2 = nn.PReLU().double()
        self.prelu3 = nn.PReLU().double()

    def forward(self, x) :
        x = self.prelu1(self.fc1(x))
        x = self.prelu2(self.fc2(x))
        x = self.fc3(x)
        #x = self.prelu3(self.fc3(x))
        #x = self.fc4(x)
        return x

#def mesure_ecart(x,y):
#	torch.abs (x - y) ** 4

net = Net()
criterion = nn.MSELoss()
optimizer = optim.Adam(net.parameters(), lr=10**(-3))
index_test = []
for i in range(longueurEntree, len(entrees_rn) - longueurSortie) :
	index_test.append(i)



for tour in range(10000) :
	optimizer.zero_grad()
	batch_source = []
	batch_target = []
	for j in range(20) :
		i = random.choice(index_test)
		batch_source.append(torch.tensor(entrees_rn[i-longueurEntree : i]).double().view(1,-1))
		target = []
		for j in range(i, i + longueurSortie) :
			target.append(entrees_rn[j][5])        #11
		for j in range(i, i + longueurSortie) :
			target.append (entrees_rn[j][6])       #13
		batch_target.append(torch.tensor(target).double().unsqueeze(0)) 
	source = torch.cat(batch_source,0)
	target = torch.cat(batch_target,0)
	out = net(source)
	loss = criterion(out,target)
	optimizer.step()


taille = len(donnees_test[0]["2019"])
ecart= torch.tensor(np.zeros([1,16]))	
compt = 0
nb_tour = 1000

for tour in range(nb_tour) :
	i = rd.randint (0, taille - longueurSortie - longueurEntree)
	annee = rd.choice (["2008", "2019"])
	entre = []
	sortie = []
	for j in range(longueurEntree) :
		cdt,sdt = convertiseur_date(donnees_test[0][annee][i+j])
		ch,sh = convertiseur_heure(donnees_test[0][annee][i+j])
		liste = [(float(annee) - ma)/sta,cdt,sdt,ch,sh]
		for k in [6,8] :
			liste.append((donnees_test[k][annee][i+j] - moyennes[k]) / ecart_type[k] )
		#for k in range (1,12):
		#	if k != 4 :
		#		liste.append((donnees_test[k][annee][i+j] - moyennes[k]) / ecart_type[k] )
		#	else :
		#		liste.append(np.cos ( donnees_test[k][annee][i+j] * 2 * np.pi / 360 ))
		#		liste.append(np.sin ( donnees_test[k][annee][i+j] * 2 * np.pi / 360 ))
		entre.append([liste])
	for j in range(8) :
		sortie.append((donnees_test[6][annee][(j+i+longueurEntree)]- moyennes[6])/ecart_type[6])
	for j in range(8) :
		sortie.append((donnees_test[8][annee][(j+i+longueurEntree)]- moyennes[8])/ecart_type[8])
	entre = torch.tensor(entre).double().view(1,-1)
	rep = net(entre)
	#print (sortie)
	#print(rep)
	ecart = ecart + (rep - torch.tensor(sortie).unsqueeze(0))**2

ETt = ( ecart.view(2,8)[0] / nb_tour) ** (1/2) * ecart_type[6]
ETh = ( ecart.view(2,8)[1] / nb_tour) ** (1/2) * ecart_type[8]
print ("ETt = " + str (ETt))
print ("ETh = " + str (ETh))

torch.save(net.state_dict(), "./Rn2-1.nn")
