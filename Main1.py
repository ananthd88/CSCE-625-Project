import Reader
import DataProcessor
import operator
import SVMClassifier

   
def main():
   trains = []
   tests = []
   dictionary = set()
   
   reader = Reader.XMLReader("posts.xml", 1) # Read every row
   #reader = Reader.CSVReader("/data/CSCE 625 Project Files/Train.csv", 1000) # Read every 1000th row
   reader.openFile()
   processor = DataProcessor.DataProcessor()
   
   print "DEBUG: Begin reading and processing rows"
   testcountP = 0
   testcountN = 0
   countP = 0
   countN = 0
   while True:
      row = reader.readNext()
      if row.get("Id", False):
         processor.processRow(row)
         dictionary.update(row["Tokens"])
         if row["Tags"]:   # Consider only rows that have at least 1 tag
            if "cryptography" in row["Tags"]:
               if countP % 10 == 0:
                  tests.append(row) # Every 1 out of 10 +ve instances
                  testcountP += 1
               else:
                  trains.append(row)
               countP += 1
            elif "cryptography" not in row["Tags"]:
               if countN % 10 == 0:   # Every 1 out of 10 -ve instances
                  tests.append(row)
                  testcountN += 1
               else:
                  trains.append(row)
               countN += 1         
      else: # If there is no 'Id' then that's the end of the dataset
         break
   reader.closeFile()
   print "DEBUG: End reading and processing rows"
   print "Number of training set rows: " + str(len(trains))
   print "Number of test set rows with +ve tag: " + str(testcountP)
   print "Number of test set rows with -ve tag: " + str(testcountN)
   print "DEBUG: Begin printing list of tags sorted by frequency"
   #for tag in sorted(tags.iteritems(), key=operator.itemgetter(1), reverse = True):
   #for key in sorted(tags, key = lambda tag: tags[tag], reverse=True):
   #   print key + " = " + str(tags[key])
   print "DEBUG: End printing list of tags sorted by frequency"
   print "DEBUG: Begin SVM Training"
   svmclassifier = SVMClassifier.SVMClassifier()
   svmPackage = processor.packRowsForSVM(trains, "cryptography")
   svmclassifier.train(svmPackage["X"], svmPackage["Y"], list(dictionary))
   print "DEBUG: End SVM Training"
   
   FP = 0
   FN = 0
   TP = 0
   TN = 0
   for row in tests:
      prediction = svmclassifier.classify(row["Tokens"])
      if "cryptography" in row["Tags"]:
         if prediction:
            TP += 1
         else:
            FN += 1
      else:
         if prediction:
            FP += 1
         else:
            TN += 1
      
      #if "cryptography" in row["Tags"]:
      #   actual = "Yes"
      #else:
      #   actual = "No"
      #print row["Id"] + " - " + str(prediction) + " - " + actual
   print "True Positives = " + str(TP)
   print "False Positives = " + str(FP)
   print "True Negatives = " + str(TN)
   print "False Negatives = " + str(FN)
if __name__ == '__main__':
    main()
