# Eric Stubbs and Jonathan Call
# CS 5340
# Fall 2018

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import sys

input = sys.argv[1]
filePath = ""
storyIdList = []

with open(input, "r") as inputFile:
  filePath = inputFile.readline()
  line = inputFile.readline()
  while line:
    storyIdList.append(inputFile.readline())

storyText = ""
storySens = []
for storyDir in storyIdList:
  with open(filePath + storyDir + ".story") as storyFile:
    line = storyFile.readline() # Headline
    line = storyFile.readline() # Date
    line = storyFile.readline() # StoryID
    storyID = line[1]
    line = storyFile.readline() # Blank line
    line = storyFile.readline() # TEXT:
    line = storyFile.readline()  # Blank line
    while line:
      line = storyFile.readLine()
      storyText += line
    storySens = sent_tokenize(storyText)

  with open(filePath + storyDir + ".questions") as questionFile:
    while line:
      line = questionFile.readline()
      questionId = line[1]
      line = questionFile.readline()
      question = line[1:]
      line = questionFile.readLine() # The difficulty
      #difficulty = line[1]
      line = questionFile.readLine() # The blank line

      #find answer to the question and output it

