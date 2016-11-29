import os
import re
from detectSpam import *
from stopWords import *
from collections import defaultdict
from collections import Counter

spamWordCount = Counter()
binarySpamWordCount = Counter()
nonspamWordCount = Counter()
binaryNonSpamWordCount = Counter()
noOfSpamFiles = 0
noOfNonSpamFiles = 0

def readFile(fileName):
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close()
    return 0,lines

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
        #cleanedLine = cleanHtml(line)
        word = line.split(' ')
        words = []
        for w in word:
            w = w.lower()
            #words = ''.join(e for e in w if e.isalnum())
            if not 'nbsp' in w and w not in stopWords and w.isalpha():
                if mode == 'spam':
                    spamWordCount[w] += 1
                    if w not in words:
                        words.append(w)
                        binarySpamWordCount[w] += 1
                else:
                    nonspamWordCount[w] += 1
                    if w not in words:
                        words.append(w)
                        binaryNonSpamWordCount[w] += 1



if __name__ == '__main__':
    spam_path = 'train/spam'
    nonspam_path = 'train/notspam'
    for path, dirs, files in os.walk(spam_path):
        noOfSpamFiles = len(files) - 1
        for filename in files:
            if filename != 'cmds':
                x = os.path.join(path, filename)
                index, Lines = readFile(x)
                addToArray(Lines,'spam')
    for path, dirs, files in os.walk(nonspam_path):
        noOfNonSpamFiles = len(files) - 1
        for filename in files:
            if filename != 'cmds':
                x = os.path.join(path, filename)
                index, Lines = readFile(x)
                addToArray(Lines,'nonspam')

    numOfSpams = noOfSpamFiles / ((noOfSpamFiles + noOfNonSpamFiles) * 1.0)
    numOfNonSpams = noOfNonSpamFiles / ((noOfSpamFiles + noOfNonSpamFiles) * 1.0)

    print numOfSpams
    print numOfNonSpams

    file = open('modelFile.txt', 'w')
    for eachword in spamWordCount:
        file.write(eachword.strip() + ' ' + str(spamWordCount[eachword]) + ' ' + str(binarySpamWordCount[eachword]) + ' ' + 's')
        file.write(os.linesep)
    for eachword in nonspamWordCount:
        file.write(eachword.strip() + ' ' + str(nonspamWordCount[eachword]) + ' ' + str(binaryNonSpamWordCount[eachword]) + ' ' + 'ns')
        file.write(os.linesep)
    file.close()

