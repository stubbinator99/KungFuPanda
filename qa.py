# Eric Stubbs and Jonathan Call
# CS 5340
# Fall 2018

#import nltk
#from nltk.chunk import conlltags2tree
import spacy
import sys

# Load spacy
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

  # Process the story with spacy
  doc = nlp(storyString)

  # Get a list of sentences in the story
  storySents = doc.sents

  #tokenized_sen = []

  tagged_sens = []
  chunked_sens = []
  ner_sens = []
  nltk_format_ner_sens = []
  sen_index = 0
  doc_ner = []

  for sen in storySents:
    # Add noun chunks NOT sure what this is for...Don't think its used anywhere
    chunked_sens.append(sen.noun_chunks)

    # Sentences with each word and its POS tag. Example: [Scotia, NNP]
    tagged_sens.append([])

    # Sentences with each word, its POS tag, and BIO/Entity tag. Ex: [[Nova, NNP, B-GPE],[Scotia, NNP, I-GPE]]
    ner_sens.append([])


    for token in sen:
      tagged_sens[len(tagged_sens)-1].append([token.text, token.tag_])


      # Sentences in spacy BIO tag format
      ner_sens[sen_index].append([#[len(ner_sens)-1].append([
          token.text,
          token.tag_,
          "{0}-{1}".format(token.ent_iob_, token.ent_type_) if token.ent_iob_ != 'O' else token.ent_iob_
      ])
      # Sentence trees in nltk format
      #nltk_format_ner_sens.append(conlltags2tree(ner_sens[len(nltk_format_ner_sens)]))

    # List of entities with its type, for each sentence.
    # Ex: (one sentence ahs two GPE entities): [[[Liverpool, GPE], [Nova Scotia, GPE]]]
    doc_ner.append([])
    for entity in sen.ents:
      doc_ner[len(doc_ner)-1].append([entity.text,  # ent.start_char, ent.end_char,
                    entity.label_])

    sen_index += 1

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

        spacy_q = nlp(question)

        tagged_q = []
        q_bio = [] #BIO tags for the question
        q_ner = [] #NER tags for the question
        for token in spacy_q:
          tagged_q.append([token.text, token.tag])
          q_bio.append([
            token.text,
            token.tag_,
            "{0}-{1}".format(token.ent_iob_, token.ent_type_) if token.ent_iob_ != 'O' else token.ent_iob_
          ])

        for entity in doc.ents:
          q_ner.append([entity.text, #ent.start_char, ent.end_char,
                        entity.label_])

        question_entity_types = []

        # Spacy Entity tags: ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART',
        #             'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']

        if "Who" in question_word_list or "who" in question_word_list or "Whose" in question_word_list or "whose" in question_word_list:
          # nltk entity types
          #question_entity_types.append("PERSON")
          #question_entity_types.append("ORGANIZATION")
          #question_entity_types.append("GPE")

          # spacy entity types
          question_entity_types.append("PERSON")
          question_entity_types.append("NORP")
          question_entity_types.append("ORG")
          question_entity_types.append("GPE")
        elif "What" in question_word_list or "what" in question_word_list:
          # Other notes: 'at what point' (like a 'when' question), 'what type', 'what happened', 'what x' (what book, what organization, etc.)
          question_entity_types = []
        elif "When" in question_word_list or "when" in question_word_list:
          #question_entity_types.append("DATE")
          #question_entity_types.append("TIME")

          question_entity_types.append("DATE")
          question_entity_types.append("TIME")
          #question_entity_types.append("ORDINAL") #first, second, etc.
        elif "Where" in question_word_list or "where" in question_word_list:
          # Other notes: 'where in x' (where in Canada, etc)
          #question_entity_types.append("LOCATION")
          #question_entity_types.append("FACILITY")
          #question_entity_types.append("GPE")

          question_entity_types.append("FAC")
          #question_entity_types.append("ORG")
          question_entity_types.append("GPE")
          question_entity_types.append("LOC")
        elif "How" in question_word_list or "how" in question_word_list:
          # Other notes: 'how long', 'how many', 'how much', 'how often', 'how far', 'by how much'
          question_entity_types = []
        elif "Why" in question_word_list or "why" in question_word_list:
          # Other notes: 'why will' (other tense)
          question_entity_types = []

        sens_with_matching_ents = []

        # Do NER for each sentence in the story
        #entity_found = False
        #for sen in doc.sents:
        entity_found = False
        unique_sentence_entities = set()
        named_ent_sentence = []

        for i in range(len(doc_ner)):  # for sent in doc_ner:
          entity_found = False
          for entity in question_entity_types:
            if entity_found:
              break
            for ent in doc_ner[i]: #for ent in spacy_q.ents:
              if entity == ent[1]:#ent.label:
                sens_with_matching_ents.append(i)
                #if entity in unique_sentence_entities:
                # Success
                attempted_questions = attempted_questions + 1
                answered_questions = answered_questions + 1
                print("STORY:\t\t{}".format(storyFilePath))
                print("QUESTION:\t{}".format(question))
                print("ANSWER:\t\t{}".format(sen))
                print()
                entity_found = True
                break

        # IMPORTANT!!! This will only display the first possible answer to the question.
        # If you want to see all possible answers, comment out the following if statement
        # if entity_found:
        #   break

        if not entity_found:
          # Failure
          attempted_questions = attempted_questions + 1
          print("STORY:\t\t{}".format(storyFilePath))
          print("QUESTION:\t{}".format(question))
          print("ANSWER:\t\tNone.")
          print()

        # Count word overlap between sentences and the question
        question_array = question.split()
        word_overlap = []
        for sen in doc.sents:
          word_overlap.append(0)
          for q_word in question_array:
            if q_word in sen.text:
              word_overlap[len(word_overlap)-1] += 1
            #print("")
        #  if q_word in

        print(word_overlap)


        # Set count, questionId, question, and difficulty to default values before processing the next set question
        count = 0
        questionId = ""
        question_word_list = []
        difficulty = ""
        question = ""
        word_overlap = []


print("Total # of questions: {}\t\t# of questions attempted: {}\t\t# of questions answered: {}".format(total_questions, attempted_questions, answered_questions))
print("Done!")
