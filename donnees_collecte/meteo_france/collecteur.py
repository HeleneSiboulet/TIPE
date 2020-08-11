from webbot import Browser
import time

web = Browser()
for annee in range(2020,1995,-1) :
	for moi in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] :
		web.go_to('https://donneespubliques.meteofrance.fr/?fond=donnee_libre&prefixe=Txt%2FSynop%2FArchive%2Fsynop&extension=csv.gz&date=' + str(annee) + moi)
		time.sleep(1)
		web.click('Accès aux données')
		time.sleep(1)
