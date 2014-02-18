from bs4 import BeautifulSoup
import urllib
import re
import csv
import argparse
import sqlite3
import time

playerCount = 0
teamCount = 0

## Creates the sql database. Currently filename is generated from time.
createTable_sql = open('create_pgs.sql', 'r').read()
time = str(time.strftime("%d_%m %H:%M"))
conn = sqlite3.connect(time + '.db')
c = conn.cursor()
try:
    c.executescript(createTable_sql)
except Exception as e:
    errorMessage = time + ': ' + str(e)
    print'Error: ' + errorMessage
    c.close()
    raise

# This method scrapes the data from a certain player's 'gamelog'
# page. It outputs the data to the correct format.
def playerGet(url):
	opener = urllib.FancyURLopener({})
	html_doc = opener.open(url).read()
	soup = BeautifulSoup(html_doc)
	table = soup.find("table", attrs={"class":"tablehead"})

	# Create a unique player id
	global playerCount
	playerCount += 1

	datasets = []
	for row in table.find_all("tr")[1:]:
		dataset = []
		dataset.append(playerCount)
		for td in row.find_all("td"):
			data = td.get_text()
			dataset.append(data)
			print dataset[1]
		datasets.append(dataset)

	# DB that shit
	playerStore(datasets)

	# Verbose printing code given the -v in the terminal
	global args
	if(args.v):
		for k in datasets:
			print (datasets[datasets.index(k)])

def playerStore(datasets):
	### TODO: Insert the new player's data into a database
	for dataset in datasets:
		if len(dataset) != 3:
			game_date = dataset[0]
			# TODO: add all the data to variables that make sense

			# TODO: Store those variables in the database via the 
	print datasets

# This method cycles through all the players on a team roster page
# and then calls the playerGet() for each of those players
def teamGet(url):
	print "working on" + url[30:]
	team_url = urllib.urlopen(url).read()
	teamSoup = BeautifulSoup(team_url)
	playerTable = teamSoup.find("table", attrs={"class":"tablehead"})

	for player in playerTable.find_all("tr")[1:]:
		playerPage_url = str(player.find('a').get('href')) # Must cast to string, as the BS4 works soley with unicode objects
		playerPage = urllib.urlopen(playerPage_url)
		playerSoup = BeautifulSoup(playerPage)
		reg = re.compile(r'Game Log') # The search query; only grabs li objects with this text in them
		elements = [e for e in playerSoup.find_all('li') if reg.match(e.text)]
		if len(elements) != 0:
			# Formats the team url correctly
			player_url = 'http://espn.go.com' + elements[0].a.get('href')
			print player_url
			playerGet(player_url)

# Grabs and then loops through all the NCAA Men's Basketball teams, and then calls teamGet() for each
def main():
	cmdOptions() # allows output supression 

	# Cycles through all the teams on the main league page
	league_url = "http://espn.go.com/mens-college-basketball/teams"
	leaguePage = urllib.urlopen(league_url)
	leagueSoup = BeautifulSoup(leaguePage)

	# Builds a list of team roster links as found on the above url
	teamRosterList = []
	reg = re.compile(r'Roster') # The search condition; only grabs a objects with text equal to this
	teamRosterList = [e for e in leagueSoup.find_all('a') if reg.match(e.text)]

	# Gets stats for each team found
	for team in teamRosterList:
		baseRoster_url = 'http://espn.go.com/mens-college-basketball/team/roster/_/id/'
		# Grabs only the numbers out of the link and then formats it correctly to be called with teamGet()
		callingTeam_url = baseRoster_url + re.findall(r'\d+', team.get('href'))[0]
		teamGet(callingTeam_url)

def cmdOptions():
	parser = argparse.ArgumentParser(description='Scrape player data from ESPN')
	parser.add_argument('-v', action='store_true')
	global args
	args = parser.parse_args()

main() ## MAIN METHOD CALL