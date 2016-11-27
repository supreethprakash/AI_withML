#to remove HTML tags
'''import re


def cleanHtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

print(cleanHtml("<html><body><center><b><font color=\"blue\">*****Bonus Fat Absorbers As Seen On TV, Included Free With Purchase Of 2 Or More Bottle, $24.95 Value*****</font><br><br>***TAKE $10.00 OFF 2 & 3 MONTH SUPPLY ORDERS, $5.00 OFF 1 MONTH SUPPLY!***AND STILL GET YOUR BONUS!  PRICE WILL BE DEDUCTED DURING PROCESSING.<br><r>"))
'''

wordsList = list()

specialCharacters = ['\n','\t', ' ', '\r']

def readFile(fileName):
  file = open(fileName, 'r')
  lines = file.readlines()
  for i in range(len(lines)):
    if lines[i].isspace() == True:
      return i, lines

def addToArray(lines):
  for line in lines:
    word = line.split(' ')
    if word not in wordsList and word not in specialCharacters:
      wordsList.append(word)

if __name__ == '__main__':
  index, Lines = readFile('test/notspam/0002.b3120c4bcbf3101e661161ee7efcb8bf')
  addToArray(Lines[index+1:len(Lines)])
