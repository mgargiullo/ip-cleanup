#!/usr/bin/env python3

import csv
import sys, getopt
from netaddr import *
inputfile = ''
outputfile = ''
action = ''
masterlist = []

def phelp(error=''):
	if error != '':
		print("Error: " + error)
	print(' ')
	print('parse-ips.py -i <inputfile> [-o <output-file-CIDR-Notaton>]')
	sys.exit()

def getArgs(argv):
	global inputfile
	global outputfile
	global action
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:a:")
	except getopt.GetoptError as err:
		phelp(err)
	if len(sys.argv) > 1:
		for opt, arg in opts:
			if opt == '-h':
				phelp()
			elif opt in ("-i"):
				inputfile = arg
				try:
					inputfile
				except NameError as err:
					phelp(err)
				else:
					print("Input file is " + inputfile)
			elif opt in ("-o","-a"):
				outputfile = arg
				if opt == "-a":
					action = "a"
				else:
					action = "w"
			else:
				phelp()
	else:
		phelp()
	return

def buildIPList(arr, iprange):
	if ',' in iprange:
		for iblock in re.split('\.\s*',iprange):
			if "-" in iblock:
				start,end=iblock.split('-')
				for ip in list(iter_iprange(start,end)):
					arr.extend([iip for iip in IPNetwork(ip)])
			else:
				arr.extend([ip for ip in IPNetwork(iblock)])
	else:
		if "-" in iprange:
			start,end=iprange.split('-')
			for ip in list(iter_iprange(start,end)):
					arr.extend([iip for iip in IPNetwork(ip)])
		else:
			arr.extend([ip for ip in IPNetwork(iprange)])
	return arr

def countIPs(iprange):
	ip_count = 0
	ip = ''
	ip_list = []
	
	if ',' in iprange:
		print("In multi Section")
		for iblock in re.split('\.\s*',iprange):
			if "-" in iblock:
				start,end=iblock.split('-')
				for ip in list(iter_iprange(start,end)):
					ip_list.extend([str(iip) for iip in IPNetwork(ip)])
			else:
				ip_list.extend([str(ip) for ip in IPNetwork(iblock)])
	else:
		if "-" in iprange:
			start,end=iprange.split('-')
			for ip in list(iter_iprange(start,end)):
				ip_list.extend([str(iip) for iip in IPNetwork(ip)])
		else:
			ip_list.extend([str(ip) for ip in IPNetwork(iprange)])
	return len(ip_list)
	


# Main
if __name__ == "__main__":
	getArgs(sys.argv[1:])
	filetoparse = inputfile
	total = 0
	grandtotal = 0
	# Open CSV and build IP List
	with open(filetoparse) as csvfile:
		myreader = csv.reader(csvfile, delimiter=',')
		for row in myreader:
			total = 0
			for srange in row:
				total = countIPs(srange)
				print(srange + " -  " + str(total))
				grandtotal += total
				masterlist = buildIPList(masterlist, srange)
				
	print("GRANDTOTAL: " + str(grandtotal))

	sortedlist = sorted(masterlist)
	
	cidrlist = cidr_merge(sortedlist)
	
	if outputfile == inputfile:
		outputfile = inputfile + ".out"
	f = open(outputfile, action)
	print(len(cidrlist))
	for item in cidrlist:
		print(item)
		f.write(str(item))
		f.write("\n")
	f.close()
exit()

			
		
		

			