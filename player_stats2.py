from bs4 import BeautifulSoup
import urllib
import re

def playerGet(url):
	opener = urllib.FancyURLopener({})
	html_doc = opener.open(url).read()
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

team_url = urllib.urlopen('http://espn.go.com/mens-college-basketball/team/roster/_/id/150/duke-blue-devils').read()
teamSoup = BeautifulSoup(team_url)
playerTable = teamSoup.find("table", attrs={"class":"tablehead"})

players = []
for player in playerTable.find_all("tr")[1:]:
	playerPage_url = str(player.find('a').get('href'))
	playerPage = urllib.urlopen(playerPage_url)
	playerSoup = BeautifulSoup(playerPage)
	reg = re.compile(r'Game Log')
	elements = [e for e in playerSoup.find_all('li') if reg.match(e.text)]
	if len(elements) != 0:
		player_url = 'http://espn.go.com' + elements[0].a.get('href')
		print player_url
		playerGet(player_url)

#playerGet('http://espn.go.com/mens-college-basketball/player/gamelog/_/id/66562/jabari-parker')