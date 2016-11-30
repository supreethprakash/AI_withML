from utilities import *
import os
from stopWords import *
from collections import Counter

documentMatrix = dict()


def createMatrix(lines, mode, fileName):
	wordCount = Counter()
	valCount = []
	documentMatrix[fileName] = []
	for line in lines:
		word = line.split(' ')
		for w in word:
			w = w.lower()
			words = ''.join(e for e in w if e.isalnum())
			wordCount[words] += 1

	for word in bagOfWords:
		if word in wordCount:
			valCount.append(wordCount[word])
		else:
			valCount.append(0)

	if mode == 'spam':
		documentMatrix[fileName].append(valCount)
		documentMatrix[fileName].append('spam')
	else:
		documentMatrix[fileName].append(valCount)
		documentMatrix[fileName].append('notspam')


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
					createMatrix(Lines, 'spam', filename) if i == 0 else createMatrix(Lines, 'notspam', filename)

if __name__ == '__main__':
	bagOfWords = readModelFile()
	addTrainingData()