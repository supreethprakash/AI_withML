import os
import re
from stopWords import *
from collections import defaultdict
from collections import Counter

spamWordCount = Counter()
nonspamWordCount = Counter()
noOfSpamFiles = 0
noOfNonSpamFiles = 0

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


def addToArray(lines, mode):
    for line in lines:
        cleanedLine = cleanHtml(line)
        word = cleanedLine.split(' ')
        for w in word:
            w = w.lower()
            words = ''.join(e for e in w if e.isalnum())
            if not 'nbsp' in words and words not in stopWords and words.isalpha():
                if mode == 'spam':
                    spamWordCount[words] += 1
                else:
                    nonspamWordCount[words] += 1


if __name__ == '__main__':
    spam_path = 'train/spam'
    nonspam_path = 'train/notspam'
    for path, dirs, files in os.walk(spam_path):
        noOfSpamFiles = len(files) - 1
        for filename in files:
            if filename != 'cmds':
                x = os.path.join(path, filename)
                index, Lines = readFile(x)
                addToArray(Lines[index+1:len(Lines)],'spam')
    for path, dirs, files in os.walk(nonspam_path):
        noOfNonSpamFiles = len(files) - 1
        for filename in files:
            if filename != 'cmds':
                x = os.path.join(path, filename)
                index, Lines = readFile(x)
                addToArray(Lines[index + 1:len(Lines)],'nonspam')

    numOfSpams = noOfSpamFiles / ((noOfSpamFiles + noOfNonSpamFiles) * 1.0)
    numOfNonSpams = noOfNonSpamFiles / ((noOfSpamFiles + noOfNonSpamFiles) * 1.0)

    file = open('modelFile.txt', 'w')
    for eachword in spamWordCount:
        file.write(eachword + '\t' + '{0:.16f}'.format((spamWordCount[eachword]/ (sum(spamWordCount.values()) * 1.0)) * numOfSpams) + '\t' + 's')
        file.write(os.linesep)
    for eachword in nonspamWordCount:
        file.write(eachword + '\t' + '{0:.16f}'.format((nonspamWordCount[eachword] / (sum(nonspamWordCount.values()) * 1.0)) * numOfNonSpams) + '\t' + 'ns')
        file.write(os.linesep)
    file.close()

