import csv
import datetime
from lxml import html
import msvcrt as m
import requests
import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def wait():
    m.getch()

# Use vader sentiment to get public sentiment of the company
def getSentiment(api, term):
	tweets = api.search(q = term, rpp = 100)
	analyzer = SentimentIntensityAnalyzer()
	score = 0;
	for tweet in tweets:
		vs = analyzer.polarity_scores(tweet.text)
		score += vs['compound']
	
	if len(tweets) > 0:
		score = score / len(tweets)

	return score;
	
if len(sys.argv) != 3:
	print("ERROR: Script must have 3 arguments: getStockInfo.py <COMPANY_TICKERS>.csv <OUTPUT_FILE>.csv")
	sys.exit()

# Get the token and key information for the twitter API
f = open("config.txt", "r");
lines = f.readlines();
config = list()
for line in lines:
	if len(line) > 0 and line[0] != '#':
		config.append(line.rstrip())

# Access the twitter API
auth = tweepy.OAuthHandler(config[0], config[1])
auth.set_access_token(config[2], config[3])
api = tweepy.API(auth)
	
# Parse the inputted CSV file
#   Assume a data header row
#   Assume each ticker is on new row
#   Assume the ticker is field 0
inputTickerFile = csv.reader(open(sys.argv[1]))
outputDataFile = csv.writer(open(sys.argv[2], 'a', newline = ''))

next(inputTickerFile) # skip the data header row
outputFile = csv.writer

sectors = {} # dictionary of all sectors
sectorNum = 0
industries = {} # dictionary of all industries
industryNum = 0

secFile = csv.reader(open("sectors.csv"))
for row in secFile:
	sectors[row[0]] = float(row[1])
	
indusFile = csv.reader(open("industries.csv"))
for row in indusFile:
	industries[row[0]] = float(row[1])

for row in inputTickerFile:
	ticker = row[0] # get the ticker
	name = row[1] # get the company name
	sector = row[2] # get the sector
	industry = row[3] # get the industry
	
	# Scrape current stock information from marketwatch.com
	url = "http://www.marketwatch.com/investing/stock/" + ticker
	page = requests.get(url)
	htmlTree = html.fromstring(page.content) # get the of the page for the ticker
	
	keyData = htmlTree.xpath("//span[@class=\"kv__value kv__primary \"]/text()")
	if len(keyData) != 16:
		print("ERROR: Stock does not have all necessary fields: " + ticker)
	else:
		closed = htmlTree.xpath("//span[@class=\"value\"]/text()")
		if len(closed) == 0:
			closed = htmlTree.xpath("//bg-quote[@class=\"value\"]/text()")

		# load the information from marketwatch as floats into variables
		SYM = row[0] # stock ticker
		DATE = datetime.datetime.today() # the date and time this data was gathered
		CLOSE = float(closed[0]) # price at closing (the value to be predicted)
		OPEN = float(keyData[0][1:]) # stock opening
		MKT = float(keyData[3][1:len(keyData[3])-1]) # market capacity in millions
		SO = float(keyData[4][0:len(keyData[4])-1]) # shares outstanding in milllions
		PF = float(keyData[5][0:len(keyData[5])-1]) # public float
		B = float(keyData[6]) # beta
		RPP = float(keyData[7][1:len(keyData[7])-1]) # revenue per employee
		PER = float(keyData[8]) # P/E ratio
		EPS = float(keyData[9][1:]) # EPS
		Y = float(keyData[10][0:len(keyData[10])-1]) # percentage yield
		D = float(keyData[11][1:]) # dividend
		FS = float(keyData[14][0:len(keyData[14])-1]) # percentage of float shorted
		AV = float(keyData[15][0:len(keyData[15])-1]) # average volume in thousands
		SEC = float(sectors[sector]) # the sector of this company
		INDUS = float(industries[industry]) # the industry of this company
		SENT = getSentiment(api, name) # get the twitter sentiment of the company
	
		# Write the data to the data csv file
		outputDataFile.writerow( (SYM, DATE, CLOSE, OPEN, MKT, SO, PF, B, RPP, PER, EPS, Y, D, FS, AV, SEC, INDUS, SENT) )







