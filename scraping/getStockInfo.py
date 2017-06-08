import csv
from lxml import html
import requests
import sys

if (len(sys.argv) != 3):
	print("ERROR: Script must have 3 arguments: getStockInfo.py <COMPANY_TICKERS>.csv <OUTPUT_FILE>.csv")
	sys.exit()

# Parse the inputted CSV file
#   Assume a data header row
#   Assume each ticker is on new row
#   Assume the ticker is field 0
inputTickerFile = csv.reader(open(sys.argv[1]))
next(inputTickerFile) # skip the data header row
for row in inputTickerFile:
	ticker = row[0] # get the ticker
	
	url = "http://www.marketwatch.com/investing/stock/" + ticker
	page = requests.get(url)
	htmlTree = html.fromstring(page.content); # get the of the page for the ticker
	
	keyData = htmlTree.xpath("//span[@class=\"kv__value kv__primary \"]/text()")
	if len(keyData) != 16:
		print("ERROR: Stock does not have all necessary fields: " + ticker)
	
	closed = htmlTree.xpath("//span[@class=\"value\"]/text()")
	
	SYM = row[0] # stock ticker
	OPEN = keyData[0][1:] # stock opening
	CLOSE = closed[0] # price at closing
	MKT = keyData[3][1:len(keyData[3])-1] # market capacity in millions
	SO = keyData[4][0:len(keyData[4])-1] # shares outstanding in milllions
	PF = keyData[5][0:len(keyData[5])-1] # public float
	B = keyData[6] # beta
	RPP = keyData[7][1:len(keyData[7])-1] # revenue per employee
	PER = keyData[8] # P/E ratio
	EPS = keyData[9][1:] # EPS
	Y = keyData[10][0:len(keyData[10])-1] # yield
	D = keyData[11][1:] # dividend
	FS = keyData[14][0:len(keyData[14])-1] # percentage of float shorted
	AV = keyData[15][0:len(keyData[15])-1] # average volume in thousands
	
	sys.exit()


#outFile = csv.writer(open(sys.argv[2], 'a', newline = ''), delimiter = ',')
#for gt in goodTickers:
#	outFile.writerow([gt])







