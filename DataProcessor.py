import re
import Reader
import Timer
import numpy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class DataProcessor:
   def __init__(self):
      self.count = 0
      return
   def reset(self):
      self.count = 0
      return
   def cleanColumn(self, string):
      if not string:
         return []
      p = re.compile(r'<.*?>')   # RegEx to find html tags
      string = p.sub('', string) # Remove html tags
      string = string.lower()    # Convert
      tokens = re.findall(r"[\w-]+", string, re.UNICODE)
      tokens = filter(lambda x: x not in stopwords.words('english') and len(x) >= 3, tokens)
      #wnl = WordNetLemmatizer()
      #for i in range(len(tokens)):
      #   tokens[i] = wnl.lemmatize(tokens[i])
      return tokens
   def getTags(self, string):
      if not string:
         return []
      string = string.lower()
      array = re.findall("<([\w-]+)>", string)
      return set(array)
   def processRow(self, row):
      row["Tokens"] = self.cleanColumn(row["Title"]) + self.cleanColumn(row["Body"])
      row.pop("Title", None)
      row.pop("Body", None)
      row["Tags"] = self.getTags(row["Tags"])
      self.count += 1
      return
   def compileTrainingSet(self, filename, perCount, trainingSet, dictionary, tagLimit, tags):
      reader = Reader.XMLReader(filename, perCount) # Read every 'perCount' row
      #reader = Reader.CSVReader("/data/CSCE 625 Project Files/Train.csv", 1000) # Read every 1000th row
      reader.openFile()
      print "Compiling the training set"
      timer = Timer.Timer("Compiling training set", 5523)
      while True:
         row = reader.readNext()
         if row.get("Id", False):
            self.processRow(row)
            dictionary.update(row["Tokens"])
            trainingSet.append(row)
            timer.tick()
         else: # If there is no 'Id' then that's the end of the dataset
            break
      reader.closeFile()
      timer.stop()
      tags += self.analyzeTags(trainingSet, tagLimit)
      return
   def compileTestSet(self, filename, perCount, testSet):
      reader = Reader.XMLReader(filename, perCount) # Read every 'perCount' row
      reader.openFile()
      print "Compiling the test set"
      timer = Timer.Timer("Compiling test set", 614)
      while True:
         row = reader.readNext()
         if row.get("Id", False):
            self.processRow(row)
            testSet.append(row)
            timer.tick()
         else: # If there is no 'Id' then that's the end of the dataset
            break
      reader.closeFile()
      timer.stop()
      return
   def analyzeTags(self, rows, limit):
      tags = {}
      for row in rows:
         for tag in row["Tags"]:
            if tag in tags:
               tags[tag] += 1
            else:
               tags[tag] = 1
      count = 0
      freqTags = []
      for tag1 in sorted(tags, key = lambda tag: tags[tag], reverse=True):
         #if count < limit:
         if tags[tag1] > limit:
            count += 1
            #print str(count) + ". " + tag1 + " - " + str(tags[tag1])
            freqTags.append(tag1)
         else:
            break
      return freqTags
   def packRowsForSVM(self, rows):
      X = []
      for row in rows:
         X.append(row["Tokens"])         
      return X
   def packRowsForOvR(self, rows):
      X = []
      for row in rows:
         X.append(" ".join(row["Tokens"]))
         # Delete the tokens to conserve memory
         row.pop("Tokens", None)
      return numpy.array(X)
   def getTagVectors(self, rows, tags):
      Y = [[] for i in range(len(rows))]
      #tagIndex = 0
      for tag in tags:
         rowIndex = 0
         for row in rows:
            if tag in row["Tags"]:
               #Y[rowIndex].append(tagIndex)
               Y[rowIndex].append(tag)
            rowIndex += 1
         #tagIndex += 1
      return Y
   def getTagVector(self, rows, tag):
      Y = []
      for row in rows:
         if tag in row["Tags"]:
            Y.append(1)
         else:
            Y.append(0)
      return Y
