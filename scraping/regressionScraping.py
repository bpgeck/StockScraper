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
inFile = csv.reader(open(sys.argv[1]))
outFile = csv.writer(open(sys.argv[2], 'w', newline = ''))
next(inFile) # skip the data header row
for row in inFile:
	ticker = row[0] # get the ticker
	
	url = "https://www.google.com/finance/historical?q=NASDAQ%3A" + ticker
	page = requests.get(url)
	htmlTree = html.fromstring(page.content); # get the of the page for the ticker
	
	prices = htmlTree.xpath("//table//tr/td[@class=\"rgt\"]/text()")
	for i in range(3,len(prices),4):
		if (i + 10*4) >= len(prices):
			break
			
		outFile.writerow((prices[i].rstrip(), prices[i+4].rstrip(), prices[i+8].rstrip(), prices[i+12].rstrip(), prices[i+16].rstrip(), prices[i+20].rstrip(), 
		                  prices[i+24].rstrip(), prices[i+28].rstrip(), prices[i+32].rstrip(), prices[i+36].rstrip(), prices[i+40].rstrip()))				  