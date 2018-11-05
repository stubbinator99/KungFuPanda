#!/bin/bash
sudo apt-get install build-essential python-dev git
#PROGDIR=$PWD
#PYTHONDIR="/usr/bin/"
# change directory to that of python (3.6) install /Scripts
pip3.6.exe install -U spacy
#cd ../
python3.6 -m spacy download en
python3.6 -m spacy download en_core_web_md
# change directory to that of our qa.py
#cd PROGDIR
python3.6 qa.py input.txt