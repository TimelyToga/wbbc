from bs4 import BeautifulSoup
import urllib

html_doc = urllib.urlopen('http://espn.go.com/mens-college-basketball/player/gamelog/_/id/66562/jabari-parker').read()

soup = BeautifulSoup(html_doc)
table = soup.find("table", attrs={"class":"tablehead"})

datasets = []
for row in table.find_all("tr")[1:]:
	dataset = []
	for td in row.find_all("td"):
		data = td.get_text()
		dataset.append(data)
	datasets.append(dataset)

for k in datasets:
	print (datasets[datasets.index(k)])