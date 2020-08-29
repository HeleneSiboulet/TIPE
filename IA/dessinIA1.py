import json
import torch
import numpy as np

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import time
from matplotlib import pyplot as plt
import random

class Netj(nn.Module) :

    def __init__(self) :
        super(Netj, self).__init__()            
        self.fc1 = nn.Linear(280, 112).double()
        self.fc2 = nn.Linear(112, 112).double()
        self.fc3 = nn.Linear(112, 16).double() 
        self.prelu1 = nn.PReLU().double()
        self.prelu2 = nn.PReLU().double()

    def forward(self, x) :
        x = self.prelu1(self.fc1(x))
        x = self.prelu2(self.fc2(x))
        x = self.fc3(x)
        return x


class Nets(nn.Module) :

    def __init__(self) :
        super(Nets, self).__init__()            
        self.fc1 = nn.Linear(560, 224).double()
        self.fc2 = nn.Linear(224, 224).double()
        self.fc3 = nn.Linear(224, 12).double() 
        self.prelu1 = nn.PReLU().double()
        self.prelu2 = nn.PReLU().double()

    def forward(self, x) :
        x = self.prelu1(self.fc1(x))
        x = self.prelu2(self.fc2(x))
        x = self.fc3(x)
        return x

netj = Netj()
nets = Nets()

netj.load_state_dict(torch.load("./net1j.nn"))
netj.eval()
nets.load_state_dict(torch.load("./net1s.nn"))
nets.eval()

with open('./donnees/temperatureTest.json') as jsonfile :
    temperature = json.load(jsonfile)

with open('./donnees/HumiditeTest.json') as jsonfile :
    humidite = json.load(jsonfile)


longueur = 7
debut = 30.25   
ideb = temperature[0]["2019"].index(debut)
imili = temperature[0]["2019"].index(debut + longueur) + 1
ifin = temperature[0]["2019"].index(debut + 2*longueur) + 1
temperature_reference = [temperature[0]["2019"][ideb:imili], temperature[1]["2019"][ideb:imili]]
temperature_obs = [temperature[0]["2019"][imili:ifin], temperature[1]["2019"][imili:ifin]]
humidite_reference = [temperature[0]["2019"][ideb:imili], temperature[1]["2019"][ideb:imili]]
humidite_obs = [temperature[0]["2019"][imili:ifin], temperature[1]["2019"][imili:ifin]]

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

taille = len(temperature[0]["2019"])

def convertiseur_date(dt) :
    angle = dt/366*2*np.pi
    return np.cos(angle), np.sin(angle)

annee = torch.tensor(annee)
temp = torch.tensor(temp)
humi = torch.tensor (humi)

ma = float(torch.mean(annee))
sta = float(torch.std(annee)) #ecart type
mt = float(torch.mean(temp))
stt = float(torch.std(temp))
mh = float(torch.mean(humi))
sth = float(torch.std(humi))

entre = []

for j in range(56) :
    an = (2019.0 - ma)/sta
    cdt,sdt = convertiseur_date((j+debut+longueur)%taille)
    tp = (temperature[1]["2019"][temperature[0]["2019"].index((j+debut+longueur)%taille)] - mt)/stt
    hm = (humidite[1]["2019"][temperature[0]["2019"].index(j+debut+longueur)%taille] - mh)/sth
    entre.append([an,cdt,sdt,tp,hm])

repj = netj (torch.tensor(entre).double().view(1,-1))
repjT = repj.view(2,8)[0] * stt + mt
repjH = repj.view(2,8)[1] * sth + mh
xj = []
for k in range (1,9):
    xj.append(debut + longueur + 0.125*k)









plt.plot (temperature_reference[0], temperature_reference[1], label = "semaine précédante")
plt.plot (temperature_obs[0], temperature_obs[1], label = "semaine suivante")
plt.plot (xj, list(repjT), label = "previsions pour le jour suivant")
plt.legend()
plt.show()
