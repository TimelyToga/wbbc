import dataset
import sys

dbFile = sys.argv[1]
connection = 'sqlite:///' + dbFile
db = dataset.connect(connection)
csvName = 'csv' + dbFile[2:len(dbFile)-2] + 'csv'
result = db['player_game_stats'].all()
dataset.freeze(result, format='csv', filename=csvName, prefix='.', meta={}, indent=2, mode='list')