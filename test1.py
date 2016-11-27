import os
wordsList = list()

specialCharacters = ['\n','\t', ' ', '\r','']

def readFile(fileName):
  file = open(fileName, 'r')
  lines = file.readlines()
  for i in range(len(lines)):
    if lines[i].isspace() == True:
      return i, lines

def addToArray(lines):
  for line in lines:
    word = line.split(' ')
    for w in word:
      if w not in wordsList and w not in specialCharacters:
        words = ''.join(e for e in w if e.isalnum())
        wordsList.append(words)

if __name__ == '__main__':
  start_path = '/home/rkanchib/Downloads/AI/assignment 4/anupbhar-rkanchib-skeragod-a4/part1/train'
  for path, dirs, files in os.walk(start_path):
    for filename in files:
      if filename != 'cmds':
        x = os.path.join(path, filename)
        index, Lines = readFile(x)
        addToArray(Lines[index+1:len(Lines)])
  print wordsList

