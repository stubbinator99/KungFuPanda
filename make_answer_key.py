import sys

input_file = sys.argv[1]    # Index file to read in
storyIdList = []
data_directory_path = ""

with open(input_file, "r") as inputFile:
  data_directory_path = inputFile.readline().strip()
  for line in inputFile:
      storyIdList.append(line.strip())

# Process each story and its associated questions and answers
for storyId in storyIdList:
  answerFilePath = data_directory_path + storyId + ".answers"
  with open(answerFilePath) as storyFile:
    for line in answerFilePath:
      if line.split()[0] == "QuestionID:":
        print(line.strip())
      elif line.split()[0] == "Question:":
        print(line.strip())
      elif line.split()[0] == "Answer:":
        print(line.strip())
      elif line.split()[0] == "Difficulty:":
        print(line.strip())
        print()
