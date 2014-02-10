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
	rowStats = [] # DATE	OPP	RESULT	MIN	FGM-FGA	FG%	3PM-3PA	3P%	FTM-FTA	FT%	REB	AST	BLK	STL	PF	TO	PTS
	rowStats = row.find("td", {'span' : "text-align: right;"})
	game['min'] = rowStats
	records.append(game)

for k in records:
	print (records[records.index(k)])