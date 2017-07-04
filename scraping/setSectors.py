import csv
import sys

if (len(sys.argv) != 4):
	print("ERROR: Script must have 4 arguments: getStockInfo.py <COMPANY_TICKERS>.csv <SEC_OUTPUT_FILE>.csv <INDUS_OUTPUT_FILE>.csv")
	sys.exit()
	
inFile = csv.reader(open(sys.argv[1]))
secOutFile = csv.writer(open(sys.argv[2], 'w', newline = ''))
indusOutFile = csv.writer(open(sys.argv[3], 'w', newline = ''))
next(inFile) # skip the data header row

sectors = {} # dictionary of all sectors
sectorNum = 0
industries = {} # dictionary of all industries
industryNum = 0

for row in inFile:
	sector = row[2];
	industry = row[3];
	
	# fill dictionaries for sectors and industries
	if sector not in sectors:
		sectors[sector] = sectorNum
		sectorNum = sectorNum + 1
		
	if industry not in industries:
		industries[industry] = industryNum
		industryNum = industryNum + 1

i = 0
for sector in sectors:
	secOutFile.writerow((sector, i))
	i += 1
	
i = 0
for indus in industries:
	indusOutFile.writerow((indus, i))
	i += 1