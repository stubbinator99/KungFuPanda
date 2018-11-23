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

    chunked_sens.append([])
    # Add noun chunks NOT sure what this is for...Don't think its used anywhere
    for chunk in sen.noun_chunks:
      # chunked_sens.append(sen.noun_chunks)
      chunked_sens[len(chunked_sens)-1].append(chunk)#[chunk.text, chunk.start_char, chunk.end_char, chunk.root.text, chunk.root.dep_])

    # Sentences with each word and its POS tag. Example: [Scotia, NNP]
    tagged_sens.append([])

    # Sentences with each word, its POS tag, and BIO/Entity tag. Ex: [[Nova, NNP, B-GPE],[Scotia, NNP, I-GPE]]
    ner_sens.append([])

    # Populate tagged_sens
    for token in sen:
      tagged_sens[len(tagged_sens)-1].append([token.text, token.tag_, token.lemma_, token.dep_])


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
          tagged_q.append([token.text, token.tag_, token.lemma_, token.dep_])
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
            if("money" in question_word_list or "cost" in question_word_list):
              question_entity_types.append("MONEY")
            elif("percent" in question_word_list):
              question_entity_types.append("PERCENT")
            else:
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

        ignored_verbs = ['be', 'has', 'have', 'had' 'did', 'do', 'will', 'would', 'should',
                         'could', 'can', 'may'] #'go', 'went'
        found_verb = False
        q_verb = '' # The stemmed verb
        # Search the question for a verb. If there is one, give it a higher weight
        for token in tagged_q:
          if token[1][0] == "V" and token[2] not in ignored_verbs:
            q_verb = token[2]
            found_verb = True
            break

        # Sentences that contain entities that the question is looking for
        sens_with_matching_ents = []
        sens_with_matching_verb = []

        # Do NER for each sentence in the story
        #for sen in doc.sents:
        entity_found = False
        unique_sentence_entities = set()
        named_ent_sentence = []

        for i in range(len(doc_ner)):   # For each sentence in the story
          # Find sentences with the question verb in
          for token in tagged_sens[i]:
            if q_verb == token[2]:
              sens_with_matching_verb.append(i)
              break

          # Find sentences with matching entity types
          entity_found = False # Set entitiyFound = False so we can see all the sentences that have matching entities
          for question_entity in question_entity_types:    # For each entity that the question is looking for
            if entity_found:
              break
            for entity_pair in doc_ner[i]:    # For each entity pair in the current sentence. Ex: [Liverpool, GPE]
              if question_entity == entity_pair[3]:
                sens_with_matching_ents.append(i) # Build a list of indices of sentences in doc_ner that have match
                entity_found = True
                break

        # Perform word overlap with stemmed words in the question and text
        word_overlap = []
        for i in range(len(tagged_sens)):
          word_overlap.append(0)
          for thing in tagged_sens[i]:
            for q_word in tagged_q:
              if q_word[3] != "punct":  # Disregard punctuation
                if q_word[2] in thing[2]:
                  word_overlap[len(word_overlap)-1] += 1

        # Pick the answer: See controlFlowNotes.txt for more information------------------------------------------------

        has_matching_verb_sentence = False
        answer_string = ""

        # If there are sentences with the matching verb
        if len(sens_with_matching_verb) > 0:
          target_sents = []
          # If one or more of the sentences has a matching entity
          for sentence_index in sens_with_matching_verb:
            if sentence_index in sens_with_matching_ents:
              target_sents.append(sentence_index)
          if len(target_sents) > 0:
            # Return the matching entity sentence with the highest word overlap
            highest_overlap = -1
            best_sentence_index = -1
            for sentence_index in target_sents:
              if word_overlap[sentence_index] > highest_overlap:
                highest_overlap = word_overlap[sentence_index]
                best_sentence_index = sentence_index

            # Return only the verb and the specified number of surrounding words in the answer sentence
            answer_tagged_sentence = tagged_sens[best_sentence_index]
            verb_index = -1
            # Find the index of the question verb
            for word_index in range(len(answer_tagged_sentence)):
              if q_verb == answer_tagged_sentence[word_index][2]:
                verb_index = word_index
                break

            # Adjust these indices as needed
            start_index = verb_index - 7
            end_index = verb_index + 7
            if start_index < 0:
              start_index = 0
            if end_index > len(answer_tagged_sentence) - 1:
              end_index = len(answer_tagged_sentence) - 1

            # Build the answer string from the words including the start and end indices
            while start_index < end_index:
              answer_string = answer_string + answer_tagged_sentence[start_index][0] + " "
              start_index = start_index + 1
            answer_string = answer_string + answer_tagged_sentence[end_index][0]

            has_matching_verb_sentence = True
          else:
            # Compare sentences with matching entities, by falling through to the if block below
            pass

        # Else if there are sentences with entities that match the question entities
        if not has_matching_verb_sentence:
          if len(sens_with_matching_ents) > 0:
            # Return the matching entity sentence with the highest word overlap
            highest_overlap = -1
            best_sentence_index = -1
            for sentence_index in sens_with_matching_ents:
              if word_overlap[sentence_index] > highest_overlap:
                highest_overlap = word_overlap[sentence_index]
                best_sentence_index = sentence_index

            # Return all the matching entities
            sentence_ents = doc_ner[best_sentence_index]
            for ent in sentence_ents:
              for q_ent in question_entity_types:
                if ent[3] == q_ent:
                  answer_string = answer_string + ent[0] + " "
          else:
            # Return the first sentence with the highest word overlap
            highest_overlap = -1
            best_sentence_index = -1
            for sentence_index in range(len(word_overlap)):
              if word_overlap[sentence_index] > highest_overlap:
                highest_overlap = word_overlap[sentence_index]
                best_sentence_index = sentence_index
            if best_sentence_index == -1:
              answer_string = storySents[0]
            else:
              answer_string = storySents[best_sentence_index]

        print("QuestionID: {}".format(questionId))
        print("Answer: {}".format(answer_string))
        print()

        # Set count, questionId, question, and difficulty to default values before processing the next set question
        count = 0
        questionId = ""
        question_word_list = []
        difficulty = ""
        question_text = ""
        word_overlap = []
