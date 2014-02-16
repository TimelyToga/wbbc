from bs4 import BeautifulSoup
import urllib
import re
import csv
import argparse

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

	global args
	if(args.v):
		for k in datasets:
			print (datasets[datasets.index(k)])

	### TODO: Insert the new player's data into a database

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