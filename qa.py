# Eric Stubbs and Jonathan Call
# CS 5340
# Fall 2018

import nltk
#from nltk.tokenize import word_tokenize, sent_tokenize
#from nltk.tag import pos_tag
import spacy
from nltk.chunk import conlltags2tree
import sys

nlp = spacy.load('en_core_web_sm')

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
    #storySents = sent_tokenize(storyString)

  doc = nlp(storyString)
  storySents = doc.sents
  #tokenized_sen = []
  tagged_sens = []
  chunked_sens = []
  ner_sens = []
  nltk_format_ner_sens = []

  for sen in storySents:
    #tokenized_sen = word_tokenize(sen)
    #tokenized_sen = []
    # for token in sen:
    #   print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(
    #     token.text,
    #     token.idx,
    #     token.lemma_,
    #     token.is_punct,
    #     token.is_space,
    #     token.shape_,
    #     token.pos_,
    #     token.tag_
    #   ))
    chunked_sens.append(sen.noun_chunks)

    tagged_sens.append([])
    #ner_sens.append([])
    for token in sen:
      tagged_sens[len(tagged_sens)-1].append([token.text, token.tag_])


      # Sentences in spacy ner format
      ner_sens.append([#[len(ner_sens)-1].append([
          token.text,
          token.tag_,
          "{0}-{1}".format(token.ent_iob_, token.ent_type_) if token.ent_iob_ != 'O' else token.ent_iob_
      ])
      # Sentence trees in nltk format
      #nltk_format_ner_sens.append(conlltags2tree(ner_sens[len(nltk_format_ner_sens)]))

    #tagged_sen = pos_tag(tokenized_sen)

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
        total_questions = total_questions + 1

        # Run NER on the question
        tagged = nltk.pos_tag(question_word_list)
        named_ent = nltk.ne_chunk(tagged)

        for element in named_ent:
          elementStr = str(element)
          if elementStr[1] != "'" and elementStr[1] != "\"":
            entity = str(element).split()[0][1:]

        #print(question)
        question_entity_types = []
        # Entity tags (from ace): ['LOCATION', 'ORGANIZATION', 'PERSON', 'DURATION',
        #             'DATE', 'CARDINAL', 'PERCENT', 'MONEY', 'MEASURE', 'FACILITY', 'GPE']

        if "Who" in question_word_list or "who" in question_word_list or "Whose" in question_word_list or "whose" in question_word_list:
          question_entity_types.append("PERSON")
          question_entity_types.append("ORGANIZATION")
          question_entity_types.append("GPE")
        elif "What" in question_word_list or "what" in question_word_list:
          # Other notes: 'at what point' (like a 'when' question), 'what type', 'what happened', 'what x' (what book, what organization, etc.)
          question_entity_types = []
        elif "When" in question_word_list or "when" in question_word_list:
          question_entity_types.append("DATE")
          question_entity_types.append("TIME")
        elif "Where" in question_word_list or "where" in question_word_list:
          # Other notes: 'where in x' (where in Canada, etc)
          question_entity_types.append("LOCATION")
          question_entity_types.append("FACILITY")
          question_entity_types.append("GPE")
        elif "How" in question_word_list or "how" in question_word_list:
          # Other notes: 'how long', 'how many', 'how much', 'how often', 'how far', 'by how much'
          question_entity_types = []
        elif "Why" in question_word_list or "why" in question_word_list:
          # Other notes: 'why will' (other tense)
          question_entity_types = []

        # Do NER for each sentence in the story
        question_answered = False
        for sen in storySents:
          #tokenized_sen = word_tokenize(sen)
          #tagged_sen = pos_tag(tokenized_sen)

          # Do NER for the sentence. Find any named entities in the sentence.
          # If the found NE matches the looked for NE, success
          # Print the question and the answer sentence.
          unique_sentence_entities = set()
          #named_ent_sentence = nltk.ne_chunk(tagged_sen)
          named_ent_sentence = []
          for element in named_ent_sentence:
            elementStr = str(element)
            if elementStr[1] != "'" and elementStr[1] != "\"":
              entity = str(element).split()[0][1:]
              unique_sentence_entities.add(entity)

          for entity in question_entity_types:
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


print("Total # of questions: {}\t\t# of questions attempted: {}\t\t# of questions answered: {}".format(total_questions, attempted_questions, answered_questions))
print("Done!")
