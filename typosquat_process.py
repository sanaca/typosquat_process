#!/usr/bin/env python

import re
import sys
import csv


def sigint_handler(signal, frame):
	print('You pressed Ctrl+C!')
	sys.exit(0)

# Internationalized processuss not supported
def validate_processus(processus):
	if len(processus) > 255:
		return False
	if processus[-1] == ".":
		processus = processus[:-1]
	allowed = re.compile('\A([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}\Z', re.IGNORECASE)
	return allowed.match(processus)

def bitsquatting(processus):
	out = []
	prcess = processus.rsplit('.', 1)[0]
	extension = processus.rsplit('.', 1)[1]
	masks = [1, 2, 4, 8, 16, 32, 64, 128]

	for i in range(0, len(prcess)):
		c = prcess[i]
		for j in range(0, len(masks)):
			b = chr(ord(c) ^ masks[j])
			o = ord(b)
			if (o >= 48 and o <= 57) or (o >= 97 and o <= 122) or o == 45:
				out.append(prcess[:i] + b + prcess[i+1:] + '.' + extension)

	return out

def homoglyph(processus):
	glyphs = {
	'd':['b', 'cl'], 'm':['n', 'rn'], 'l':['1', 'i'], 'o':['0'],
	'w':['vv'], 'n':['m'], 'b':['d'], 'i':['l'], 'g':['q'], 'q':['g']
	}
	out = []
	prcess = processus.rsplit('.', 1)[0]
	extension = processus.rsplit('.', 1)[1]

	for ws in range(0, len(prcess)):
		for i in range(0, (len(prcess)-ws)+1):
			win = prcess[i:i+ws]

			j = 0
			while j < ws:
				c = win[j]
				if c in glyphs:
					for g in range(0, len(glyphs[c])):
						win = win[:j] + glyphs[c][g] + win[j+1:]

						if len(glyphs[c][g]) > 1:
							j += len(glyphs[c][g]) - 1
						out.append(prcess[:i] + win + prcess[i+ws:] + '.' + extension)

				j += 1

	return list(set(out))

def repetition(processus):
	out = []
	prcess = processus.rsplit('.', 1)[0]
	extension = processus.rsplit('.', 1)[1]

	for i in range(0, len(prcess)):
		if prcess[i].isalpha():
			out.append(prcess[:i] + prcess[i] + prcess[i] + prcess[i+1:] + '.' + extension)

	return out

def transposition(processus):
	out = []
	prcess = processus.rsplit('.', 1)[0]
	extension = processus.rsplit('.', 1)[1]

	for i in range(0, len(prcess)-1):
		if prcess[i+1] != prcess[i]:
			out.append(prcess[:i] + prcess[i+1] + prcess[i] + prcess[i+2:] + '.' + extension)

	return out

def replacement(processus):
	keys = {
	'1':'2q', '2':'3wq1', '3':'4ew2', '4':'5re3', '5':'6tr4', '6':'7yt5', '7':'8uy6', '8':'9iu7', '9':'0oi8', '0':'po9',
	'q':'12wa', 'w':'3esaq2', 'e':'4rdsw3', 'r':'5tfde4', 't':'6ygfr5', 'y':'7uhgt6', 'u':'8ijhy7', 'i':'9okju8', 'o':'0plki9', 'p':'lo0',
	'a':'qwsz', 's':'edxzaw', 'd':'rfcxse', 'f':'tgvcdr', 'g':'yhbvft', 'h':'ujnbgy', 'j':'ikmnhu', 'k':'olmji', 'l':'kop',
	'z':'asx', 'x':'zsdc', 'c':'xdfv', 'v':'cfgb', 'b':'vghn', 'n':'bhjm', 'm':'njk'
	}
	out = []
	prcess = processus.rsplit('.', 1)[0]
	extension = processus.rsplit('.', 1)[1]

	for i in range(0, len(prcess)):
		if prcess[i] in keys:
			for c in range(0, len(keys[prcess[i]])):
				out.append(prcess[:i] + keys[prcess[i]][c] + prcess[i+1:] + '.' + extension)

	return out


def omission(processus):
	out = []
	prcess = processus.rsplit('.', 1)[0]
	extension = processus.rsplit('.', 1)[1]

	for i in range(0, len(prcess)):
		out.append(prcess[:i] + prcess[i+1:] + '.' + extension)

	return out

def insertion(processus):
	keys = {
	'1':'2q', '2':'3wq1', '3':'4ew2', '4':'5re3', '5':'6tr4', '6':'7yt5', '7':'8uy6', '8':'9iu7', '9':'0oi8', '0':'po9',
	'q':'12wa', 'w':'3esaq2', 'e':'4rdsw3', 'r':'5tfde4', 't':'6ygfr5', 'y':'7uhgt6', 'u':'8ijhy7', 'i':'9okju8', 'o':'0plki9', 'p':'lo0',
	'a':'qwsz', 's':'edxzaw', 'd':'rfcxse', 'f':'tgvcdr', 'g':'yhbvft', 'h':'ujnbgy', 'j':'ikmnhu', 'k':'olmji', 'l':'kop',
	'z':'asx', 'x':'zsdc', 'c':'xdfv', 'v':'cfgb', 'b':'vghn', 'n':'bhjm', 'm':'njk'
	}
	out = []
	prcess = processus.rsplit('.', 1)[0]
	extension = processus.rsplit('.', 1)[1]

	for i in range(1, len(prcess)-1):
		if prcess[i] in keys:
			for c in range(0, len(keys[prcess[i]])):
				out.append(prcess[:i] + keys[prcess[i]][c] + prcess[i] + prcess[i+1:] + '.' + extension)
				out.append(prcess[:i] + prcess[i] + keys[prcess[i]][c] + prcess[i+1:] + '.' + extension)

	return out

def fuzz_processus(processus):
	processuss = []

	for i in bitsquatting(processus):
			processuss.append({ 'type':'Bitsquatting', 'processus':i })
	for i in homoglyph(processus):
		processuss.append({ 'type':'Homoglyph', 'processus':i })
	for i in repetition(processus):
		processuss.append({ 'type':'Repetition', 'processus':i })
	for i in transposition(processus):
		processuss.append({ 'type':'Transposition', 'processus':i })
	for i in replacement(processus):
		processuss.append({ 'type':'Replacement', 'processus':i })
	for i in omission(processus):
		processuss.append({ 'type':'Omission', 'processus':i })
	for i in insertion(processus):
		processuss.append({ 'type':'Insertion', 'processus':i })

	return processuss
processus = fuzz_processus(sys.argv[1].lower())

for i in processus:
	print('%s,%s' % (i.get('type'), i.get('processus')))
