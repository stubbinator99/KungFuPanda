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
    storyIdList.append(line.strip())


# Process each story and its associated questions and answers
for storyId in storyIdList:
  storyString = ""
  storySents = []

  # Read in the story file ---------------------------------------------------------------------------------------------
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
  #storySents = doc.sents

  tagged_sens = []
  chunked_sens = []
  ner_sens = []
  doc_ner = []
  nltk_format_ner_sens = []
  sen_index = 0

  # For each sentence in the story
  for sen in doc.sents:#storySents:
    storySents.append(sen.text)

    # Add noun chunks NOT sure what this is for...Don't think its used anywhere
    chunked_sens.append(sen.noun_chunks)

    # Sentences with each word and its POS tag. Example: [Scotia, NNP]
    tagged_sens.append([])

    # Sentences with each word, its POS tag, and BIO/Entity tag. Ex: [[Nova, NNP, B-GPE],[Scotia, NNP, I-GPE]]
    ner_sens.append([])

    # Populate tagged_sens
    for token in sen:
      tagged_sens[len(tagged_sens)-1].append([token.text, token.tag_])


      # Populatet ner_sens, sentences in spacy BIO tag format
      ner_sens[sen_index].append([#[len(ner_sens)-1].append([
          token.text,
          token.tag_,
          "{0}-{1}".format(token.ent_iob_, token.ent_type_) if token.ent_iob_ != 'O' else token.ent_iob_
      ])

    # List of entities with its type, for each sentence.
    # Ex: (one sentence ahs two GPE entities): [[[Liverpool, GPE], [Nova Scotia, GPE]]]
    doc_ner.append([])
    for question_entity in sen.ents:
      doc_ner[len(doc_ner)-1].append([question_entity.text, question_entity.start_char, question_entity.end_char,
                                      question_entity.label_])

    # Move on to the nexte sentence in the story
    sen_index += 1


  # Read in the question file ------------------------------------------------------------------------------------------
  with open(data_directory_path + storyId + ".questions") as questionFile:

    count = 0           # Count for reading in the questions
    questionId = ""
    question_text = ""
    difficulty = ""
    question_word_list = []

    for orig_line in questionFile:
      line = orig_line.split()
      if count == 0:            # Get the question ID
        questionId = line[1]
        count = 1
      elif count == 1:          # Get the question text
        question_word_list = line[1:]
        question_text = orig_line.strip()[10:]
        count = 2
      elif count == 2:          # Get the question difficulty
        difficulty = line[1]
        count = 3
      elif count == 3:          # Consume the blank line, answer the question
        total_questions = total_questions + 1

        # Process the question with spacy
        spacy_q = nlp(question_text)

        tagged_q = []
        q_bio = [] #BIO tags for the question
        q_ner = [] #NER tags for the question
        for token in spacy_q:
          tagged_q.append([token.text, token.tag_])
          q_bio.append([
            token.text,
            token.tag_,
            "{0}-{1}".format(token.ent_iob_, token.ent_type_) if token.ent_iob_ != 'O' else token.ent_iob_
          ])

        for question_entity in spacy_q.ents:
          q_ner.append([question_entity.text,  #ent.start_char, ent.end_char,
                        question_entity.label_])

        # List of possible entities the question is asking for
        question_entity_types = []
        question_type = ""

        # Spacy Entity tags: ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART',
        #             'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']

        if "Who" in question_word_list or "who" in question_word_list or "Whose" in question_word_list or "whose" in question_word_list:
          question_type = "who"
          question_entity_types.append("PERSON")
          question_entity_types.append("NORP")
          question_entity_types.append("ORG")
          question_entity_types.append("GPE")
        elif "What" in question_word_list or "what" in question_word_list:
          question_type = "what"
          # Other notes: 'at what point' (like a 'when' question), 'what type', 'what happened', 'what x' (what book, what organization, etc.)
          question_entity_types = []
          # Find the index of the word "what"
          what_index = -1
          for current_index in range(len(q_bio)):
            if q_bio[current_index][0] == "What" or q_bio[current_index][0] == "what":
              what_index = current_index;
              break
          # If the next word is a verb, look for sentences with the q_entity and a verb
          if q_bio[what_index + 1][1] == "VBZ" or q_bio[what_index + 1][1] == "VBN":
            # Answer must contain the same entity type as the question
            for entity_tuple in q_ner:
              question_entity_types.append(entity_tuple[1])
          # If the next word is a noun, look for person, place, or thing entities
          elif q_bio[what_index + 1][1] == "NN":
            for entity_tuple in q_ner:
              question_entity_types.append(entity_tuple[1])
          else:
            # TODO: Might be someting smarter we can do here
            # The entity type in the question has to match the entity type in the answer
            for entity_tuple in q_ner:
              question_entity_types.append(entity_tuple[1])
        elif "When" in question_word_list or "when" in question_word_list:
          question_type = "when"
          question_entity_types.append("DATE")
          question_entity_types.append("TIME")
          #question_entity_types.append("ORDINAL") #first, second, etc.
        elif "Where" in question_word_list or "where" in question_word_list:
          question_type = "where"
          # Other notes: 'where in x' (where in Canada, etc)
          question_entity_types.append("FAC")
          #question_entity_types.append("ORG")
          question_entity_types.append("GPE")
          question_entity_types.append("LOC")
        elif "How" in question_word_list or "how" in question_word_list:
          # Other notes: 'how long', 'how many', 'how much', 'how often', 'how far', 'by how much'
          # See if the how question is looking for a quantity
          question_type = "how"
          # TODO: Add more quantity words
          quantity_words = ["big", "far", "long", "many", "much", "often", "old", "tall", "cost"]
          looking_for_quantity = False
          for word in quantity_words:
            if word in question_word_list:
              looking_for_quantity = True
              question_type = "quantity"
          if looking_for_quantity:
            question_entity_types.append("PERCENT")
            question_entity_types.append("MONEY")
            question_entity_types.append("QUANTITY")
            question_entity_types.append("ORDINAL")
            question_entity_types.append("CARDINAL")
          else:
            # The entity type in the question has to match the entity type in the answer
            for entity_tuple in q_ner:
              question_entity_types.append(entity_tuple[1])
        elif "Why" in question_word_list or "why" in question_word_list:
          question_type = "why"
          # Other notes: 'why will' (other tense)
          # The entity type in the question has to match the entity type in the answer
          for entity_tuple in q_ner:
            question_entity_types.append(entity_tuple[1])

        # Sentences that contain entities that the question is looking for
        sens_with_matching_ents = []

        # Do NER for each sentence in the story
        #for sen in doc.sents:
        entity_found = False
        unique_sentence_entities = set()
        named_ent_sentence = []

        for i in range(len(doc_ner)):   # For each sentence in the story
          entity_found = False # Set entitiyFound = False so we can see all the sentences that have matching entities
          for question_entity in question_entity_types:    # For each entity that the question is looking for
            if entity_found:
              break
            for entity_pair in doc_ner[i]:    # For each entity pair in the current sentence. Ex: [Liverpool, GPE]
              if question_entity == entity_pair[3]:
                sens_with_matching_ents.append(i) # Build a list of indices of sentences in doc_ner that have match
                entity_found = True
                break


        # Count word overlap between all matching sentences and the question
        question_array = question_text.split()
        word_overlap = []
        for i in sens_with_matching_ents:   # For each matching sentence
          word_overlap.append(0)
          for thing in ner_sens[i]:         # For each word in the matching sentence
            for q_word in question_array:   # For each word in the question
              if q_word == thing[0]:        # If the words match, increment the word overlap
                word_overlap[len(word_overlap)-1] += 1


        # Word overlap array is done. Find the sentence with the most word overlap
        tied_sentence_indices = []
        max_overlap = -1
        for i in range(len(word_overlap)):
          if word_overlap[i] > max_overlap:
            max_overlap = word_overlap[i]
            tied_sentence_indices = []
            tied_sentence_indices.append(i)
          elif word_overlap[i] == max_overlap:
            tied_sentence_indices.append(i)

        # If no matching ents, return none
        if len(sens_with_matching_ents) == 0:
          attempted_questions = attempted_questions + 1
          print("QuestionID: {}".format(questionId))
          #print("QUESTION:\t{}".format(question_text))
          print("ANSWER:")
          print()
        else:
          # Print the first sentence with the highest word overlap
          # TODO: Add more features to get the correct sentence instead of just the first one
          attempted_questions = attempted_questions + 1
          answered_questions = answered_questions + 1
          print("QuestionID: {}".format(questionId))
          #print("QUESTION:\t{}".format(question_text))
          print("ANSWER: ", end="")
          print(storySents[tied_sentence_indices[0]])
          #for thing in ner_sens[tied_sentence_indices[0]]:
            #print(thing[0], end=" ")
          # print()
          print()


        # Set count, questionId, question, and difficulty to default values before processing the next set question
        count = 0
        questionId = ""
        question_word_list = []
        difficulty = ""
        question_text = ""
        word_overlap = []


print("Total # of questions: {}\t\t# of questions attempted: {}\t\t# of questions answered: {}".format(total_questions, attempted_questions, answered_questions))
print("Done!")
