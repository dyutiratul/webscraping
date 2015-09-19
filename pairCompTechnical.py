from bs4 import BeautifulSoup

import requests
import xml.etree.cElementTree as ET

pair = raw_input("Enter pair with a hyphen between them (ex:- gbp-usd)... ")
url = "http://www.investing.com/currencies/" + str(pair) + "-technical"
r  = requests.get(url)
if r.status_code == 200:
	data = r.text
else:
	print "Invalid pair, hence getting euro-dollar data (eur-usd)"
	r  = requests.get("http://www.investing.com/currencies/eur-usd-technical")
	data = r.text
soup = BeautifulSoup(data, "lxml")

root = ET.Element("pair-comparison")
doc = ET.SubElement(root, "technical")

page = soup.find("h1", "headerWithInfoBox float_lang_base_1")
page = str(str(page).rpartition('<')[0]).rpartition('>')[2]

val = ""
boccat = soup.find("div", "top bold inlineblock")
for dd in boccat.findAll("span"):
	val = val + str(str(dd).rpartition('<')[0]).rpartition('>')[2] + " "
	
ET.SubElement(doc, "summary", name=page).text = val.decode("utf8")

val = ""
details = soup.find("div", "bottomText float_lang_base_1")
for dd in details.findAll("span"):
	val = val + str(str(dd).rpartition('<')[0]).rpartition('>')[2] + " "
	
ET.SubElement(doc, "summary").text = val.decode("utf8")

summary = soup.find("div", "studySummary bold arial_14")
for dd in summary.findAll("span"):
	adv = str(str(dd).rpartition('<')[0]).rpartition('>')[2]
	advice = ET.SubElement(doc, "advice").text = adv.decode("utf8")

mah = ET.SubElement(doc, "Moving_Averages")
avg = soup.find("div", "studySummaryTable bold")
for dd in avg.findAll("span"):
	moav = str(str(dd).rpartition('<')[0]).rpartition('>')[2]
	moavVal = moav.decode("utf8")
	if moavVal != '':
		ET.SubElement(mah, "Moving_Averages").text = moavVal

tin = ET.SubElement(doc, "Technical_Indicators")
ind = soup.find("div", "studySummaryTable bottom bold")
for dd in ind.findAll("span"):
	ti = str(str(dd).rpartition('<')[0]).rpartition('>')[2]
	tiVal = ti.decode("utf8")
	if tiVal != '':
		ET.SubElement(tin, "Technical_Indicators").text = tiVal
	
pp = ET.SubElement(doc, "Pivot_Points")
ppName = ["Name", "S3", "S2", "S1", "Pivot Points", "R1", "R2", "R3"]
table = soup.find('table', "genTbl closedTbl crossRatesTbl")
rows = table.findAll('tr')[1:]

for tr in rows:
	name = -1
	cols = tr.findAll('td')
	for td in cols:
		val = str(td.find(text=True))
		if val != 'None':
			name = name + 1
			ET.SubElement(pp, "value", name=ppName[name]).text = val.decode("utf8")

'''for ind in soup.findAll("td", "first left lastRow"):
	for sp in ind.findAll("p"):
		for dd in sp.find("span"):
			#print str(str(dd).rpartition('<')[0]).rpartition('>')[2]'''
			
ti = ET.SubElement(doc, "Technical_Indicators")
tiName = ["Name", "Value", "Action"]
table = soup.find('table', "genTbl closedTbl technicalIndicatorsTbl smallTbl float_lang_base_1")
rows = table.findAll('tr')[1:]
buy = 0
sell = 0
for tr in rows:
	name = -1
	cols = tr.findAll('td')
	for td in cols:
		val = str(td.find(text=True))
		if val != 'None' and val != "Buy:":
			name = name + 1
			ET.SubElement(ti, "value", name=tiName[name]).text = val.decode("utf8")
			if val.decode("utf8") == "Buy":
				buy += 1
			elif val.decode("utf8") == "Sell":
				sell += 1
ET.SubElement(ti, "value", name="Summary").text = "Buy: " + str(buy) + " Sell: " + str(sell) + " Neutral: " + str(12-(buy+sell))

ma = ET.SubElement(doc, "Moving_Averages")
maName = ["Period", "Simple", "Exceptional"]
name = -1	
table = soup.find('table', "genTbl closedTbl movingAvgsTbl float_lang_base_2")
rows = table.findAll('tr')[1:]
buy = 0
sell = 0
for tr in rows:
	name = -1
	cols = tr.findAll('td')
	for td in cols:
		val = str(td.find(text=True))
		adv = str(str(td.find("span")).rpartition('<')[0]).rpartition('>')[2]
		if val != 'None' and val != "Buy:":
			name = name + 1
			ET.SubElement(ma, "value", name=maName[name]).text = val.decode("utf8") + " " + adv
			if adv == "Buy":
				buy += 1
			elif adv == "Sell":
				sell += 1
ET.SubElement(ma, "value", name="Summary").text = "Buy: " + str(buy) + " Sell: " + str(sell) + " Neutral: " + str(12-(buy+sell))

tree = ET.ElementTree(root)
tree.write("currencyPairTechnical.xml")