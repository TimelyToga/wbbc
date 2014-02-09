from bs4 import BeautifulSoup
import urllib

html_doc = urllib.urlopen('http://espn.go.com/mens-college-basketball/player/gamelog/_/id/66562/jabari-parker').read()

soup = BeautifulSoup(html_doc)

print(soup.find(id="li.team-name"))
