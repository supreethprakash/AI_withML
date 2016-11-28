'''
This file is to detect whether the given Email is a spam or not
'''

import os
import re

spamWords = {}
nonSpamWords = {}
k = 0.7

def readFile(fileName):
    flag = False
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close()
    for i in range(len(lines)):
        if lines[i].isspace() == True:
            flag = True
            return i, lines
    if flag == False:
        return len(lines), lines


def readModel(fileName):
    file = open(fileName, 'r')
    eachline = file.readlines()
    file.close()
    for line in eachline:
        values = line.split('\t')
        if values[2] == 's':
            spamWords[values[0]] = values[1]
        else:
            nonSpamWords[values[0]] = values[1]


def cleanHtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    removeLines = re.compile('\n')
    cleantext = re.sub(removeLines, '', cleantext)
    removeSpecialCases = re.compile('[\\]x[0-9][0-9]')
    cleantext1 = re.sub(removeSpecialCases,'', cleantext)
    return cleantext1


def checkSpam(lines, mode, confusionMatrix):
    Q = 0
    numberOfWords = 0

    for line in lines:
        cleanedLine = cleanHtml(line)
        word = cleanedLine.split(' ')
        for w in word:
            numberOfWords += 1
            w = w.lower()
            words = ''.join(e for e in w if e.isalnum())
            if words in spamWords:
                spamProbability = float(spamWords[words])
            else:
                spamProbability = 0.00000000001

            if words in nonSpamWords:
                nonSpamProbability = float(nonSpamWords[words])
            else:
                nonSpamProbability = 0.00000000001

            Q += spamProbability / (nonSpamProbability * 1.0)

    if (Q / (numberOfWords * 1.0)) > k :
        m = 'spam'
    else:
        m = 'nonspam'

    if mode == 'spam':
        if m == 'spam':
            confusionMatrix['tp'] += 1
        else:
            confusionMatrix['fn'] += 1
    else:
        if m == 'spam':
            confusionMatrix['fp'] += 1
        else:
            confusionMatrix['tn'] += 1

    file.write(str(Q / (numberOfWords * 1.0)) + '\t' + mode + '\t' + m)
    file.write(os.linesep)

if __name__ == '__main__':
    spam_path = 'test/spam'
    nonspam_path = 'test/notspam'
    confusionMatrix = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}

    readModel('modelFile.txt')
    file = open('output.txt', 'w')
    for path, dirs, files in os.walk(spam_path):
        noOfSpamFiles = len(files) - 1
        for filename in files:
            if filename != 'cmds':
                x = os.path.join(path, filename)
                index, Lines = readFile(x)
                checkSpam(Lines[index+1:len(Lines)],'spam', confusionMatrix)

    for path, dirs, files in os.walk(nonspam_path):
        noOfNonSpamFiles = len(files) - 1
        for filename in files:
            if filename != 'cmds':
                x = os.path.join(path, filename)
                index, Lines = readFile(x)
                checkSpam(Lines[index + 1:len(Lines)],'nonspam', confusionMatrix)
    file.close()
    accuracy = ((confusionMatrix['tp'] + confusionMatrix['tn']) / (sum(confusionMatrix.values())* 1.0)) * 100.0
    print '\nThe total accuracy is ' + str(accuracy) + '%'