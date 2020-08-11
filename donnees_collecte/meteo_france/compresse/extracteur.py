import os

li = os.listdir()
for nom in li :
	if nom[-2:] == 'gz' and '(1)' not in nom:
		os.system("gunzip -f " + nom + " > " + nom[:-7].replace('.','_') + ".csv")
	elif '(1)' in nom :
		os.system('rm "' + nom + '"')