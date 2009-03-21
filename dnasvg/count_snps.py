#! /usr/bin/env python

import csv
from optparse import OptionParser

def main():
	usage = "usage: %prog inputfile"
	parser = OptionParser(usage=usage)
	parser.add_option("-p", "--pages", 		default=3, help="Number of pages to spread the DNA drawing over")
	(options, args) = parser.parse_args()
	if len(args) != 1:
		parser.error('incorrect number of arguments')

	file  = open(args[0])
	reader = csv.reader(file)
	counter = 0
	chromosome = {} 
	while True:
		try:
			row = reader.next()
			if row[5] == '--': continue				
			chromosome[row[2]] = chromosome.get(row[2], 0) + 1
			counter=counter+1
		except StopIteration:
			print "Total Length: %d" % counter
			snps_per_page = counter / options.pages 
			print "SNPs per page (count)", snps_per_page
			for page in range(options.pages):
				print "Page %d offset: %d" % (page+1, page*snps_per_page)
			for k in chromosome:
				print k, chromosome[k]
			break
	file.close()

if __name__ == '__main__':
	main()
