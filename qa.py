# Eric Stubbs and Jonathan Call
# CS 5340
# Fall 2018

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk import ShiftReduceParser
# from nltk.chunk import ChunkParserI
#from nltk.corpus import treebank
#from nltk.grammar import CFG, nonterminals
import sys

input = sys.argv[1]
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
    # find a grammar to include here, to use in the parser
    # parser = ShiftReduceParser(grammar)
    # for tree in parser.parse(taggedSens):
    # print(tree)

  #treebankProd = set()

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

        # Run NER on the question
        tagged = nltk.pos_tag(question)
        named_ent = nltk.ne_chunk(tagged)
        print(named_ent)

        if "Who" in question or "who" in question:
          print("Who question")
        elif "What" in question or "what" in question:
          # Other notes: 'at what point' (like a 'when' question), 'what type', 'what happened', 'what x' (what book, what organization, etc.)
          print("what question")
        elif "When" in question or "when" in question:
          print("When question")
        elif "Where" in question or "where" in question:
          # Other notes: 'where in x' (where in Canada, etc)
          print("Where question")
        elif "How" in question or "how" in question:
          # Other notes: 'how long', 'how many', 'how much', 'how often', 'how far', 'by how much'
          print("How question")
        elif "Why" in question or "why" in question:
          # Other notes: 'why will' (other tense)
          print("Why question")
        elif "Whose" in question or "whose" in question:
          print("Whose question")
        
        # Set count, questionId, question, and difficulty to default values before processing the next set question
        count = 0
        questionId = ""
        question = []
        difficulty = ""

print("Done!")
