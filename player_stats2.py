from bs4 import BeautifulSoup
import urllib
import re
import csv

# This method scrapes the data from a certain player's 'gamelog'
# page. It outputs the data to the correct format.
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

	# for k in datasets:
	# 	print (datasets[datasets.index(k)])

	### TODO: Insert the new player's data into a database

# This method cycles through all the players on a team roster page
# and then calls the playerGet() for each of those players
def teamGet(url):
	team_url = urllib.urlopen(url).read()
	teamSoup = BeautifulSoup(team_url)
	playerTable = teamSoup.find("table", attrs={"class":"tablehead"})

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

def main():
	league_url = "http://espn.go.com/mens-college-basketball/teams"
	leaguePage = urllib.urlopen(league_url)
	leagueSoup = BeautifulSoup(leaguePage)

	teamRosterList = []
	reg = re.compile(r'Roster')
	teamRosterList = [e for e in leagueSoup.find_all('a') if reg.match(e.text)]

	for team in teamRosterList:
		baseRoster_url = 'http://espn.go.com/mens-college-basketball/team/roster/_/id/'
		callingTeam_url = baseRoster_url + re.findall(r'\d+', team.get('href'))[0]
		teamGet(callingTeam_url)

main()