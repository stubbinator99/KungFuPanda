# Eric Stubbs and Jonathan Call
# CS 5340
# Fall 2018

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
import sys

input_file = sys.argv[1]    # Index file to read in
data_directory_path = ""    # Path to the directory containing the data
storyIdList = []            # List of story IDs to be read
total_questions = 0       # Count of the total questions that have been read in
attempted_questions = 0   # Count of the number of questions we tried to answer (Should be the same as total questions)
answered_questions = 0    # Count of the number of questions that have an answer (answer other than "None.")


# Open the input file to:
#   1. Get the path of the directory containing the data files
#   2. Read in a list of story IDs that we need to process
with open(input_file, "r") as inputFile:
  data_directory_path = inputFile.readline().strip()
  for line in inputFile:
    print(line.strip())
    storyIdList.append(line.strip())


# Process each story and its associated questions and answers
for storyId in storyIdList:
  storyString = ""
  storySents = []

  # Read in the story file to: ------------------------------------------------------------------------------
  #   1. Get the story text as a string
  #   2. Separate the text into individual sentences
  storyFilePath = data_directory_path + storyId + ".story"

  with open(storyFilePath) as storyFile:
    line = storyFile.readline().strip()  # Date
    line = storyFile.readline().strip()  # Headline
    line = storyFile.readline().strip()  # StoryID
    line = storyFile.readline().strip()  # Blank line
    line = storyFile.readline().strip()  # TEXT:
    line = storyFile.readline()  # Blank line

    # Read the entire contents of the story into a single string (storyString)
    for line in storyFile:
      storyString += line.strip() + " "

    # Tokenize the story string into a list of sentences
    storySents = sent_tokenize(storyString)

  # Read in the question file to: ---------------------------------------------------------------------------
  #   1.
  #   2.
  with open(data_directory_path + storyId + ".questions") as questionFile:

    count = 0           # Count
    questionId = ""
    question = ""
    difficulty = ""
    question_word_list = []
    num_questions_in_file = 0

    for orig_line in questionFile:
      line = orig_line.split()
      if count == 0:
        questionId = line[1]
        count = 1
      elif count == 1:
        question_word_list = line[1:]
        question = orig_line.strip()[10:]
        count = 2
      elif count == 2:
        difficulty = line[1]
        count = 3
      elif count == 3:
        # Question block complete. Answer the question and output it
        num_questions_in_file = num_questions_in_file + 1

        # Run NER on the question
        tagged = nltk.pos_tag(question_word_list)
        named_ent = nltk.ne_chunk(tagged)

        for element in named_ent:
          elementStr = str(element)
          if elementStr[1] != "'" and elementStr[1] != "\"":
            entity = str(element).split()[0][1:]

        #print(question)
        look_for_entity = []
        # Entity tags (from ace): ['LOCATION', 'ORGANIZATION', 'PERSON', 'DURATION',
        #             'DATE', 'CARDINAL', 'PERCENT', 'MONEY', 'MEASURE', 'FACILITY', 'GPE']

        if "Who" in question_word_list or "who" in question_word_list or "Whose" in question_word_list or "whose" in question_word_list:
          look_for_entity.append("PERSON")
        elif "What" in question_word_list or "what" in question_word_list:
          # Other notes: 'at what point' (like a 'when' question), 'what type', 'what happened', 'what x' (what book, what organization, etc.)
          continue
        elif "When" in question_word_list or "when" in question_word_list:
          look_for_entity.append("DATE")
          look_for_entity.append("TIME")
        elif "Where" in question_word_list or "where" in question_word_list:
          # Other notes: 'where in x' (where in Canada, etc)
          look_for_entity.append("LOCATION")
          look_for_entity.append("FACILITY")
          look_for_entity.append("GPE")
        elif "How" in question_word_list or "how" in question_word_list:
          # Other notes: 'how long', 'how many', 'how much', 'how often', 'how far', 'by how much'
          continue
        elif "Why" in question_word_list or "why" in question_word_list:
          # Other notes: 'why will' (other tense)
          continue

        # Do NER for each sentence in the story
        question_answered = False
        for sen in storySents:
          tokenized_sen = word_tokenize(sen)
          tagged_sen = pos_tag(tokenized_sen)

          # Do NER for the sentence. Find any named entities in the sentence.
          # If the found NE matches the looked for NE, success
          # Print the question and the answer sentence.
          unique_sentence_entities = set()
          named_ent_sentence = nltk.ne_chunk(tagged_sen)
          for element in named_ent_sentence:
            elementStr = str(element)
            if elementStr[1] != "'" and elementStr[1] != "\"":
              entity = str(element).split()[0][1:]
              unique_sentence_entities.add(entity)

          for entity in look_for_entity:
            if entity in unique_sentence_entities:
              # Success
              attempted_questions = attempted_questions + 1
              answered_questions = answered_questions + 1
              print("STORY:\t\t{}".format(storyFilePath))
              print("QUESTION:\t{}".format(question))
              print("ANSWER:\t\t{}".format(sen))
              print()
              question_answered = True

          # IMPORTANT!!! This will only display the first possible answer to the question.
          # If you want to see all possible answers, comment out the following if statement
          if question_answered:
            break

        if not question_answered:
          # Failure
          attempted_questions = attempted_questions + 1
          print("STORY:\t\t{}".format(storyFilePath))
          print("QUESTION:\t{}".format(question))
          print("ANSWER:\t\tNone.")
          print()

        # Set count, questionId, question, and difficulty to default values before processing the next set question
        count = 0
        questionId = ""
        question_word_list = []
        difficulty = ""
        question = ""

    total_questions = total_questions + num_questions_in_file

print("Total # of questions: {}\t\t# of questions attempted: {}\t\t# of questions answered: {}".format(total_questions, attempted_questions, answered_questions))
print("Done!")
