'''
This File contains utility functions which are used through out the Object
'''


def readFile(fileName):
	file = open(fileName, 'r')
	lines = file.readlines()
	file.close()
	return lines


def readModelFile():
	bagOfWords = []
	wordsInModelFile = readFile('modelFile.txt')
	for eachLine in wordsInModelFile:
		line = eachLine.split('\t')
		bagOfWords.append((line[0], line[4]))
	bagOfWords.sort(key=lambda tup: tup[1])
	return bagOfWords[-1000:]
