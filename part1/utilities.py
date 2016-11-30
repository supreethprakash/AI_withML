'''
This File contains utility functions which are used through out the Object
'''

def readFile(fileName):
	file = open(fileName, 'r')
	lines = file.readlines()
	file.close()
	return lines

