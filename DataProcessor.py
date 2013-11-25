import re
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
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
      p = re.compile(r'<.*?>')
      string = p.sub('', string)
      string = string.lower()
      tokens = re.findall(r"[\w-]+", string, re.UNICODE)
      tokens = filter(lambda x: x not in stopwords.words('english') and len(x) >= 3, tokens)
      return tokens
   def getTags(self, string):
      if not string:
         return []
      string = string.lower()
      array = re.findall("<([\w-]+)>", string)
      return set(array)
   def processRow(self, row):
      #row["Title"] = self.cleanColumn(row["Title"])
      #row["Body"] = self.cleanColumn(row["Body"])
      row["Tokens"] = self.cleanColumn(row["Title"]) + self.cleanColumn(row["Body"])
      row.pop("Title", None)
      row.pop("Body", None)
      row["Tags"] = self.getTags(row["Tags"])
      self.count += 1
      #if row["Tags"]:
      #   print row["Tags"]
      return
   def packRowsForSVM(self, rows, tag):
      X = []
      Y = []
      for row in rows:
         #X.append(row["Title"] + row["Body"])
         X.append(row["Tokens"])
         if tag in row["Tags"]:
            Y.append(1)
         else:
            Y.append(0)
      return {"X" : X, "Y" : Y}
