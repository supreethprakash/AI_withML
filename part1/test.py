import os
import re
from stopWords import *

wordsList = list()


def readFile(fileName):
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close()
    for i in range(len(lines)):
        if lines[i].isspace() == True:
            return i, lines


def cleanHtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    removeLines = re.compile('\n')
    cleantext = re.sub(removeLines, '', cleantext)
    removeSpecialCases = re.compile('[\\]x[0-9][0-9]')
    cleantext1 = re.sub(removeSpecialCases,'', cleantext)
    return cleantext1


def addToArray(lines):
    for line in lines:
        cleanedLine = cleanHtml(line)
        word = cleanedLine.split(' ')
        for w in word:
            words = ''.join(e for e in w if e.isalnum())
            if words not in wordsList and words not in specialCharacters:
                wordsList.append(words.lower())


if __name__ == '__main__':
    start_path = 'train/spam/'
    for path, dirs, files in os.walk(start_path):
        for filename in files:
            if filename != 'cmds':
                x = os.path.join(path, filename)
                index, Lines = readFile(x)
                addToArray(Lines[index+1:len(Lines)])
    file1 = open('output.txt', 'w')
    for eachword in wordsList:
        if not 'nbsp' in eachword.lower() and eachword.lower() not in stopWords and eachword.isalpha():
            file1.write(eachword)
            file1.write(os.linesep)
    file1.close()
