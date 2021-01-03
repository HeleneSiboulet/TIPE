import json
import torch
import numpy as np
import random as rd

with open("./donnees/donnees.json") as jsonfile :
	donnees = json.load(jsonfile)

with open("./donnees/donneesTest.json") as jsonfile :
	donnees_test = json.load(jsonfile)




print (donnees[9]["2015"][0])