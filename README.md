#KungFuPanda - Eric Stubbs and Jonathan Call
---------------------------------------------
NLP Question Answering System

External Resources
------------------
The Spacy python NLP library, including the en_core_web_md model, which was trained on OntoNotes and Common Crawl - https://spacy.io/

Time Estimate
-------------
Our program takes 2.5 minutes to run test set 1 (39 documents), so on average it takes 4 seconds to process each document.

Contributions
-------------
* Eric Stubbs: set up git repository, researched chunking and NER tools, researched Spacy library, helped implement Spacy library, researched getting the project working on CADE, worked on limiting answer length.  
* Jonathan Call: researched parsing, chunking, and NER tools, researched NLTK library, helped implement Spacy library, researched getting the project working on CADE, worked on improving question typing.  
* We have each contributed fairly equally to the project so far in terms of time and effort.  We spent upwards of 6 to 7 hours trying to get Spacy and our project working on CADE before Yuan Zhuang was able to post the guide on installing python libraries to a virtual environment for the CADE machines.  

Problems / Limitations
----------------------
The answer file that is created (called qa_response.txt) might contain python warnings at the top, above the question answers.  If so, delete these warnings before testing with the scoring program.  The script will navigate the user to the CADE directory containing our virtual python environment, where we have spacy installed. There are no other limitations or problems that we know of.    
