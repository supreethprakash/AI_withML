from utilities import *
import os
from stopWords import *
from collections import Counter

documentMatrix = dict()


def createMatrix(lines, mode, fileName):
	spamWordCount = Counter()
	nonSpamWordCount = Counter()

	for line in lines:
		word = line.split(' ')
		for w in word:
			w = w.lower()
			words = ''.join(e for e in w if e.isalnum())
			if not 'nbsp' in words and words not in stopWords and words.isalpha():
				if mode == 'spam':
					spamWordCount[words] += 1
				else:
					nonSpamWordCount[words] += 1

	if mode == 'spam':
		documentMatrix[fileName] = spamWordCount
	else:
		documentMatrix[fileName] = nonSpamWordCount


def addTrainingData():
	counter = 0
	for i in range(0,2):
		folderpath = 'train/spam' if i == 0 else 'train/notspam'
		for path, dirs, files in os.walk(folderpath):
			for filename in files:
				counter += 1
				if filename != 'cmds':
					x = os.path.join(path, filename)
					Lines = readFile(x)
					if i == 0:
						createMatrix(Lines, 'spam', filename)
					else:
						createMatrix(Lines, 'notspam', filename)

if __name__ == '__main__':
	addTrainingData()