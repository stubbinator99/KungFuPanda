# Eric Stubbs and Jonathan Call
# CS 5340
# Fall 2018

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk import ShiftReduceParser
#from nltk.chunk import ChunkParserI
import sys

#input = sys.argv[1]
input = "input.txt"
filePath = ""
storyIdList = []

with open(input, "r") as inputFile:
  filePath = inputFile.readline().strip()
  for line in inputFile:
    storyIdList.append(line.strip())


for storyDir in storyIdList:
  storyText = ""
  storySens = []

  # Read in the story file
  storyFilePath = filePath + storyDir + ".story"
  print(storyFilePath)

  with open(storyFilePath) as storyFile:
    line = storyFile.readline().strip()  # Date
    line = storyFile.readline().strip()  # Headline
    line = storyFile.readline().strip()  # StoryID
    storyID = line[1]
    line = storyFile.readline().strip()  # Blank line
    line = storyFile.readline().strip()  # TEXT:
    line = storyFile.readline()  # Blank line
    for line in storyFile:
      storyText += line.strip() + " "
    storySens = sent_tokenize(storyText)
    taggedSens = []
    sensWords = []
    for sen in storySens:
      sensWords.append(word_tokenize(sen))
    for sen in sensWords:
      taggedSens.append(pos_tag(sen))
    #find a grammar to include here, to use in the parser
    #parser = ShiftReduceParser(grammar)
    #for tree in parser.parse(taggedSens):
      #print(tree)

    # Read in the question file
  with open(filePath + storyDir + ".questions") as questionFile:
    count = 0
    questionId = ""
    question = []
    difficulty = ""
    for line in questionFile:
        line = line.split()
        if count == 0:
            questionId = line[1]
            count = 1
        elif count == 1:
            question = line[1:]
            count = 2
        elif count == 2:
            difficulty = line[1]
            count = 3
        elif count == 3:
            # Question block complete. Answer the question and output it

            # Set count, questionId, question, and difficulty to default values before processing the next set question
            count = 0

print("Done!")
