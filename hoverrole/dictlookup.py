# -*- coding: UTF-8-sig -*-

# Function combine() in 'createDicts.py' module can be used to generate
# the dictionary 'binstae' from stae.is and BIN databases.

# Author: Simon Bodvarsson
# 18.07.2016

import binstae
import minstae

# Look up icelandic searchterm 'word' in the dictionaries 'minstae' and 'binstae' 
# and return a dict containing the english and icelandic citation forms of the word.
def lookup(word):
	# Make sure that 'word' is a str type.
	if isinstance(word,str):
		pass
	elif isinstance(word, unicode):
		word = word.encode('utf-8')

	word = word.lower()
	# If 'word' is in citation form, look up in 'minstae' returns the translation.
	try:
		entry = minstae.minstae[word]
		entry['isTerm'] = word
		return entry
	# If 'word' is not found in 'minstae', it may not be in citation form and a
	# look up in 'binstae' is performed instead.
	except KeyError:
		try:
			entry = binstae.binstae[word]
			return entry
		# If 'word' is not found in 'binstae', the look-up has failed and an empty 
		# dict is returned.
		except KeyError:
			return {}
