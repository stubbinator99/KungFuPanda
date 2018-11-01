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
from nltk import ne
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
        print(question)
        look_for_entity = []
        # Entity tags (from ace): ['LOCATION', 'ORGANIZATION', 'PERSON', 'DURATION',
        #             'DATE', 'CARDINAL', 'PERCENT', 'MONEY', 'MEASURE', 'FACILITY', 'GPE']

        if "Who" in question or "who" in question or "Whose" in question or "whose" in question:
          print("Who question, look for PERSON")
          look_for_entity.append("PERSON")
        elif "What" in question or "what" in question:
          # Other notes: 'at what point' (like a 'when' question), 'what type', 'what happened', 'what x' (what book, what organization, etc.)

          print("what question")
          continue
        elif "When" in question or "when" in question:
          print("When question, look for DATE or TIME")
          look_for_entity.append("DATE")
          look_for_entity.append("TIME")
        elif "Where" in question or "where" in question:
          # Other notes: 'where in x' (where in Canada, etc)
          print("Where question, look for LOCATION, FACILITY, or GPE")
          look_for_entity.append("LOCATION")
          look_for_entity.append("FACILITY")
          look_for_entity.append("GPE")
        elif "How" in question or "how" in question:
          # Other notes: 'how long', 'how many', 'how much', 'how often', 'how far', 'by how much'
          print("How question")
        elif "Why" in question or "why" in question:
          # Other notes: 'why will' (other tense)
          print("Why question")
        print()

        # Set count, questionId, question, and difficulty to default values before processing the next set question
        count = 0
        questionId = ""
        question = []
        difficulty = ""

print("Done!")
