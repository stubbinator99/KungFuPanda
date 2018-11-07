#!/usr/bin/bash
cd /home/jocall/KungFuPanda
source ./env/bin/activate
read -p "Enter the path to the input file: " input
echo Starting program with file $input:
python qa.py $input > qa_response.txt
cat qa_response.txt
