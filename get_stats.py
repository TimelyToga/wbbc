from bs4 import BeautifulSoup
import urllib
import re
import csv
import argparse
import sqlite3
import time

statsCount = 0
playerCount = 0
teamCount = 0

## Creates the sql database. Currently filename is generated from time.
createTable_sql = open('create_pgs.sql', 'r').read()
time = 'db' + str(time.strftime("%d_%m_%H_%M_%S"))
dbName = time + '.db'
conn = sqlite3.connect(dbName)
c = conn.cursor()
conn.commit()

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
	global statsCount
	playerCount += 1

	# Gets demographic info about the player
	playerName = soup.find("div", attrs={'class : mod-content'})
	print playerName.h1.text

	# Gets the data from the page, and then stores it in the nested list datasets
	datasets = []
	for row in table.find_all("tr")[1:]:
		dataset = []		
		statsCount += 1
		dataset.append(statsCount)
		dataset.append(playerCount)
		for td in row.find_all("td"):
			data = td.get_text().encode('utf_8', 'ignore')
			dataset.append(data)
		if(dataset[2] != 'DATE'):
			datasets.append(dataset)

	# Verbose printing code given the -v in the terminal
	global args
	if(args.v):
		for k in datasets:
			print (datasets[datasets.index(k)])

	# DB that shit
	playerStore(datasets)

### This method stores the data from one player into the current db
def playerStore(datasets):
	### TODO: Insert the new player's data into a database
	global c
	global conn
	global playerCount
	for dataset in datasets:
		if len(dataset) == 19:
			# Store the row into  player_game_stats
			execututionString = "INSERT INTO player_game_stats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
			c.execute(execututionString, dataset)
	if(playerCount % 10 == 0):
		conn.commit()
		print "Successfully written " + str(playerCount)

# This method cycles through all the players on a team roster page
# and then calls the playerGet() for each of those players
def teamGet(url):
	global args
	if(args.s):
		print "working on: " + url[30:]
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
			if(args.s):
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
	parser.add_argument('-v', action='store_true') # verbose output of all data scraped
	parser.add_argument('-s', action='store_true') # some output; i.e. the url's of the websites scraped
	global args
	args = parser.parse_args()

main() ## MAIN METHOD CALL