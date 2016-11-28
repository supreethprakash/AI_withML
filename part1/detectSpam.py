'''
This file is to detect whether the given Email is a spam or not
'''

import os
import re
from collections import OrderedDict
from heapq import nsmallest
from heapq import nlargest

spamWords = dict()
nonSpamWords = dict()

binarySpam = dict()
binaryNonSpam = dict()

topTenSpam = dict()
topTenNotSpam = dict()


topTenBSpam = dict()
topTenBNotSpam = dict()

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
        if values[3] == 's':
            spamWords[values[0]] = values[1]
            binarySpam[values[0]] = values[2]
        else:
            nonSpamWords[values[0]] = values[1]
            binaryNonSpam[values[0]] = values[2]

def cleanHtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    removeLines = re.compile('\n')
    cleantext = re.sub(removeLines, '', cleantext)
    removeSpecialCases = re.compile('[\\]x[0-9][0-9]')
    cleantext1 = re.sub(removeSpecialCases,'', cleantext)
    return cleantext1


def checkSpam(lines, mode, confusionMatrix, confusionMatrixB):
    Q1 = 0
    Q2 = 0
    numberOfWords = 0

    for line in lines:
        cleanedLine = cleanHtml(line)
        word = cleanedLine.split(' ')
        for w in word:
            numberOfWords += 1
            w = w.lower()
            words = ''.join(e for e in w if e.isalpha())
            if words in spamWords:
                spamProbability = float(spamWords[words])
                bSpamProbability = float(binarySpam[words])
            else:
                spamProbability = 0.00000000001
                bSpamProbability = 0

            if words in nonSpamWords:
                nonSpamProbability = float(nonSpamWords[words])
                bNonSpamProbability = float(binaryNonSpam[words])
            else:
                nonSpamProbability = 0.00000000001
                bNonSpamProbability = 0

            if spamProbability == 0 or nonSpamProbability == 0:
                Q1 += 0
            else:
                Q1 += spamProbability / (nonSpamProbability * 1.0)

            if bSpamProbability == 0 or bNonSpamProbability == 0:
                Q2 += 0
            else:
                Q2 += bSpamProbability / (bNonSpamProbability * 1.0)


            topTenSpam[words] = spamProbability
            topTenNotSpam[words] = nonSpamProbability
            topTenBSpam[words] = bSpamProbability
            topTenBNotSpam[words] = bNonSpamProbability


    if (Q1 / (numberOfWords * 1.0)) > k :
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

    if (Q2 / (numberOfWords * 1.0)) > k :
        m = 'spam'
    else:
        m = 'nonspam'

    if mode == 'spam':
        if m == 'spam':
            confusionMatrixB['tp'] += 1
        else:
            confusionMatrixB['fn'] += 1
    else:
        if m == 'spam':
            confusionMatrixB['fp'] += 1
        else:
            confusionMatrixB['tn'] += 1

if __name__ == '__main__':
    spam_path = 'test/spam'
    nonspam_path = 'test/notspam'
    confusionMatrix = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}
    confusionMatrixB = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}
    readModel('modelFile.txt')
    file = open('output.txt', 'w')
    for path, dirs, files in os.walk(spam_path):
        noOfSpamFiles = len(files) - 1
        for filename in files:
            if filename != 'cmds':
                x = os.path.join(path, filename)
                index, Lines = readFile(x)
                checkSpam(Lines[index+1:len(Lines)],'spam', confusionMatrix, confusionMatrixB)

    for path, dirs, files in os.walk(nonspam_path):
        noOfNonSpamFiles = len(files) - 1
        for filename in files:
            if filename != 'cmds':
                x = os.path.join(path, filename)
                index, Lines = readFile(x)
                checkSpam(Lines[index + 1:len(Lines)],'nonspam', confusionMatrix, confusionMatrixB)
    file.close()
    accuracy = ((confusionMatrix['tp'] + confusionMatrix['tn']) / (sum(confusionMatrix.values())* 1.0)) * 100.0

    accuracyB = ((confusionMatrixB['tp'] + confusionMatrixB['tn']) / (sum(confusionMatrixB.values()) * 1.0)) * 100.0

    print '\nThe total accuracy is ' + str(accuracy) + '%'

    print '\nThe total accuracy is ' + str(accuracyB) + '%'

    ctr1=0
    ctr2=0
    print ''
    print 'Top ten words associated with spam:'
    for word,val in nlargest(10, topTenSpam.iteritems(), key=lambda (k,v): (-v,k)):
        ctr1 +=1
        print ctr1,'.',word
    print ''
    print 'Top ten words least associated with spam:'
    for word, val in nsmallest(10, topTenNotSpam.iteritems(), key=lambda (k, v): (-v, k)):
        ctr2 += 1
        print ctr2,'.',word

    bctr1 = 0
    bctr2 = 0
    print ''
    print 'Top ten words associated with spam:'
    for word, val in nlargest(10, topTenBSpam.iteritems(), key=lambda (k, v): (-v, k)):
        bctr1 += 1
        print bctr1, '.', word
    print ''
    print 'Top ten words least associated with spam:'
    for word, val in nsmallest(10, topTenBNotSpam.iteritems(), key=lambda (k, v): (-v, k)):
        bctr2 += 1
        print bctr2, '.', word


