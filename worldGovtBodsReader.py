from bs4 import BeautifulSoup

import requests
import xml.etree.cElementTree as ET

root = ET.Element("bonds")

r  = requests.get("http://www.investing.com/rates-bonds/world-government-bonds")
data = r.text

soup = BeautifulSoup(data, "lxml")

tableIds = [37, 18, 17, 14, 77, 47, 44, 51, 42, 54, 55, 45, 56, 15, 33, 16, 9, 4, 41, 21, 23, 52, 46, 57, 58, 26, 6, 20, 59, 80, 81, 62, 86, 53, 7, 83, 8, 63, 64, 65,
25, 10, 35, 43, 40, 28, 19, 84, 66, 22, 60, 11, 67, 12, 5, 68, 69, 49, 76, 70, 3, 1, 71, 72]
columns = ["Name", "Yield", "Prev.", "High", "Low", "Chg.", "Chg. %", "Time", ""]

for Id in tableIds:
	tabId = "rates_bonds_table_"+str(Id)
	#print tabId
	doc = ET.SubElement(root, tabId)
	table = soup.find('table', id=tabId)
	if table != None:
		rows = table.findAll('tr')[1:]
		for tr in rows:
			cols = tr.findAll('td')
			country = cols[1].find(text=True)
			col = 0;
			for td in cols[1:]:
				val = td.find(text=True)
				if val != None and val != '':
					#print val.encode('utf-8')
					ET.SubElement(doc, country.rpartition(' ')[0], name=columns[col]).text = val
					col = col+1
			
tree = ET.ElementTree(root)
tree.write("world-government-bonds.xml")