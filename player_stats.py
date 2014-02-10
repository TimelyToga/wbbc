from bs4 import BeautifulSoup
import urllib

html_doc = urllib.urlopen('http://espn.go.com/mens-college-basketball/player/gamelog/_/id/66562/jabari-parker').read()

soup = BeautifulSoup(html_doc)

rows = soup.findAll("tr", {'class':['evenrow', 'oddrow']})

records = []

for row in rows:
	game = {}
	game['team'] = row.find("li", {"class" : "team-name"}).text
	game['result'] = row.find("span", {"class" : ['greenfont', 'redfont']}).text
	rowStats = []
	records.append(game)

print records

# links = soup.findAll("li", { "class" : "team-name" })

# for link in links:
# 	print link.a.text