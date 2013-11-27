#!/usr/bin/python
import Timer
import DataProcessor
import OneVsRest

def main():
   # Handle for data processor
   processor = DataProcessor.DataProcessor()
   
   # Gather and clean training set data
   trainingSet = []
   dictionary = set()
   tags = []
   processor.compileTrainingSet("posts.xml", 1, trainingSet, dictionary, 20, tags)
   print "Size of training set = " + str(len(trainingSet))
   
   # Gather and clean test set data
   testSet = []
   processor.compileTestSet("test.xml", 1, testSet)
   print "Size of test set = " + str(len(testSet))
   
   # Prepare data to be passed to the OvR classifier to be trained
   X = processor.packRowsForOvR(trainingSet)
   Y = processor.getTagVectors(trainingSet, tags)
   
   # Initialize OvR classifier
   classifier = OneVsRest.OneVsRest()
   
   # Train the OvR classifier
   classifier.train(X, Y)
   
   # Prepare data to be tested with OvR classifier
   X = processor.packRowsForOvR(testSet)
   
   # Predict using OvR
   predicted = classifier.classify(X)
   
   # Print out post ids and their predicted tags
   for item, labels in zip(testSet, predicted):
      print '%s => %s' % (item["Id"], ', '.join(x for x in labels))
   
   # Compile metrics for the predcictions
   metrics = {}
   for tag in tags:
      metrics[tag] = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
   
   totalTP = 0
   totalFP = 0
   totalTN = 0
   totalFN = 0
   for tag in tags:
      rowIndex = 0
      for row in testSet:
         predictions = set(predicted[rowIndex])
         actuals     = testSet[rowIndex]["Tags"]
         # TODO: actuals may include the rare tags that were ignored, thus messing up the metrics
         if tag in actuals:
            if tag in predictions:     # Tag among actual tags, Tag among predictions
               metrics[tag]["TP"] += 1
            else:                      # Tag among actual tags, Tag not among predictions
               metrics[tag]["FN"] += 1
         else:
            if tag in predictions:     # Tag not among actual tags, Tag among predictions
               metrics[tag]["FP"] += 1
            else:                      # Tag not among actual tags, Tag not among predictions
               metrics[tag]["TN"] += 1
         rowIndex += 1
      totalTP += metrics[tag]["TP"]
      totalFP += metrics[tag]["FP"]
      totalTN += metrics[tag]["TN"]
      totalFN += metrics[tag]["FN"]
   
   # Print out metrics
   tagCount = 1
   for tag in tags:
      print str(tagCount) + ". " + tag + \
         " (" + \
            str(metrics[tag]["TP"]) + ", " + \
            str(metrics[tag]["FP"]) + ", " + \
            str(metrics[tag]["TN"]) + ", " + \
            str(metrics[tag]["FN"]) + \
         ")"
      tagCount += 1
   print "Total hits (TP)     = " + str(totalTP)
   print "Total Misses (FP)   = " + str(totalFP)
   print "Total TN            = " + str(totalTN)
   print "Total FN            = " + str(totalFN)
   return
   
if __name__ == '__main__':
    main()
