import json 

with open("./donnees/temperature.json") as jsonfile :
	temperature = json.load(jsonfile)

with open("./donnees/temperatureTest.json") as jsonfile :
	temperature_test = json.load(jsonfile)

with open("./donnees/humidite.json") as jsonfile :
	humidite = json.load(jsonfile)

with open("./donnees/humiditeTest.json") as jsonfile :
	humidite_test = json.load(jsonfile)

temperature_continu = []
temperature_result = []
for i in temperature[0].keys() :
	for j in range(len(temperature[0][i])) :
		temperature_continu.append([[int(i),temperature[0][i][j],temperature[1][i][j]]])

#print(temperature_continu)

longueur = 8*7

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import time


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv1d(1,56,3)
        self.fc1 = nn.Linear(3136, 56)  # 6*6 from image dimension
        self.fc2 = nn.Linear(56, 8)

    def forward(self, x):
        x = self.conv1(x)
        x = x.view(1,-1)
        x = self.fc1(x)
        x = self.fc2(x)
        return x


#print('\n\n\n')

net = Net()
criterion = nn.MSELoss()
optimizer = optim.SGD(net.parameters(), lr=10**(-10))
print(net)

for i in range(longueur, len(temperature_continu) - 8) :
	optimizer.zero_grad()
	source = torch.tensor(temperature_continu[i-longueur:i])
	target = []
	for j in range(i, i+8) :
		target.append(temperature_continu[j][0][2])
	target = torch.tensor([target])


	out = net(source)
	print(out)
	print(target)
	loss = criterion(out,target)
	print(loss)

	loss.backward()
	optimizer.step()
	print('\n\n')