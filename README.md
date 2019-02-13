# KungFuPanda - NLP Question Answering System
##### Eric Stubbs and Jonathan Call

### Overview

KungFuPanda is a question answering system.  It takes in a reading comprehension story and questions about that story through text files and answers them to the best of its ability.  The system uses many factors, including Cosine Similarity between the question and the story text, Named Entity Recognition, and question and verb typing, to determine the answer.  Over the course of 6 weeks, we achieved a 32% score, marked by the precision and accuracy of the answer given by the system compared to the _expected_ answer.  This was a project for our Natural Language Processing class.

### External Resources

The Spacy python NLP library, including the en_core_web_md model, which was trained on OntoNotes and Common Crawl - https://spacy.io/

### Time Estimate

Our program takes 2.5 minutes to run test set 1 (39 documents), so on average it takes 4 seconds to process each document.

### Contributions

* Eric Stubbs: set up git repository, researched chunking and NER tools, researched Spacy library, helped implement Spacy library, researched getting the project working on CADE, worked on limiting answer length.  
* Jonathan Call: researched parsing, chunking, and NER tools, researched NLTK library, helped implement Spacy library, researched getting the project working on CADE, worked on improving question typing.  

### Problems / Limitations

The answer file that is created (called qa_response.txt) might contain python warnings at the top, above the question answers.  If so, delete these warnings before testing with the scoring program.  The script will navigate the user to the CADE directory containing our virtual python environment, where we have spacy installed. There are no other limitations or problems that we know of.    
