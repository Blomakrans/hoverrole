# -*- coding: UTF-8-sig -*-

# 'ordaskra.py' and 'ordasafn.py' define a dictionary of mathematical
# terms in Icelandic and English and functions to translate a given term from 
# Icelandic to English or vice versa.
# See functions: isTranslate(), enTranslate() and lookUp().

# Functions extractValues() and createDictFromFile() are used to generate the
# dictionary file 'ordasafn.py' from the file 'output'.

# To generate 'ordasafn.py' from 'output' run: 
# >> python ordaskra.py

# Author: Simon Bodvarsson
# 28.06.2016

import ordasafn

# Create dictionary file 'ordasafn.py' from 'output' by typing into the terminal: 
# >> python ordaskra.py
if __name__ == "__main__":
	ordasafn = createDictFromFile()
	targetfile = open('ordasafn.py','w+')
	print >>targetfile, r'# -*- coding: UTF-8-sig -*-'
	print >>targetfile, 'os =',
	print >>targetfile, ordasafn
	targetfile.close()

# Look-up and translate the Icelandic searchterm 'isTerm' to English.
# Returns a list containing a single translation if transNum is 'single' 
# and all found translations if transNum is 'all'.
def isTranslate(isTerm,transNum):
	results = lookUp(isTerm,'isTerm')
	topResult = results[0]
	translation = []
	if transNum == 'all':
		for item in results:
			try:
				translation.append(item['enTerm'])
			except KeyError:
				continue
		if len(translation) == 0:
			print ("No results found for Icelandic term: '%s'" %isTerm)
		return translation
	else:
		try:
			translation.append( topResult['enTerm'])
			return translation
		except KeyError:
			print("No results found for Icelandic term:  '%s'" %isTerm)
		return translation


# Look-up and translate the English searchterm 'enTerm' to Icelandic.
# Returns a list containing a single translation if transNum is 'single' 
# and all found translations if transNum is 'all'.
def enTranslate(enTerm,transNum):	
	results = lookUp(enTerm,'enTerm')
	topResult = results[0]
	translation = []
	if transNum == 'all':
		for item in results:
			try:
				translation.append(item['isTerm'])
			except KeyError:
				continue
		if len(translation) == 0:
			print ("No results found for English term: '%s'" %enTerm)
		return translation
	else:
		try:
			translation.append( topResult['isTerm'])
			return translation[0]
		except KeyError:
			print("No results found for English term:  '%s'" %enTerm)
		return translation

# Look-up all relevant info for the searchterm 'sTerm' under the key 'key'.
def lookUp(sTerm,key):

	if isinstance(sTerm,str):
		pass
	elif isinstance(sTerm, unicode):
		sTerm = sTerm.encode('utf-8')

	results = []
	# For each line in the dictionary 'os', find matching results and add
	# to the 'results' list.
	for line in ordasafn.os:
		try: 
			dictTerm = line[key]
		except KeyError:
			# Current line in 'os' does not have an entry for 'key'. It is skipped.
			continue
		
		if any(term == sTerm.lower() for term in dictTerm):
			# Exact dictionary match. Result is added to front of list of results.
			results.append(line)

	if results == []:
		# No results found.
		results.append({})

	return results

# Find and extract values from a given line into a dictionary.
def extractValues(line):
	# Values are seperated by TAB character. 
	data = line.split('	')
	if len(data) < 8:
		return{}
	# Put the data into a dict splitting multiple entries by ", "
	values= {
				'id':data[0].split(', '),
				'translNum':data[1].split(', '),
				'enTerm':data[2].split(', '),
				'context':data[3].split(', '),
				'class':data[4].split(', '),
				'isTerm':data[5].split(', '),
				'synonyms':data[6].split(', '),
				'relatedTerms':data[7].split(', '),
			}
	# Replace empty values with empty string.
	for key,value in values.iteritems():
		if len(value) == 1 and value[0].find('\\')>-1:
			# print r"replacing '%s' for key '%s'" %(value[0],key)
			value[0] = ""

	return values

# Print a given dictionary or list. Used for testing.
def printdict(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                printdict(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                printdict(v)
            else:
                print v
    else:
        print obj

# Read from file 'output' and write its content, line by line, to a list.
# 'dictList' is a list of dict. Each line in 'output' is contained in
# a single dict. 
def createDictFromFile():
	# Read the dictionary file 'osDB' which has been generated from a .dat file and write it's content, line by line, into a list.
	dictFile = open('output')
	dictList = dictFile.readlines()
	# Close the dictionary file when its contents have been read.
	dictFile.close()

	# Extract all 7 values for each line.
	# 1: Line number
	# 2: Number of translations
	# 3: English searchterm
	# 4: Context which term is used (e.g. "in Calculus" or "in set theory")
	# 5: Word class. Numbers 3,5 and 7 represent adjectives, nouns and verbs respectively.
	# 6: Icelandic translation of term.
	# 7: English synonyms
	# 8: Related terms, e.g. for a 'See also:...'.
	# Values are seperated by TAB-character and empty values are represented by \N.

	# Replace each line in dictList with the same content reformatted into a dict of lists
	# of the form: 
	# {'id':[], 'translationNum':[], 'enTerm':[], 'class':[], 'isTerm':[], 'synonyms':[], 'relatedTerms':[]}
	for index,line in enumerate(dictList):
		dictList[index] = extractValues(line)

	return dictList
