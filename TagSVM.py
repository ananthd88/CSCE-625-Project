import Timer
import DataProcessor
import SVMClassifier
   
def main():
   # Handle for data processor
   processor = DataProcessor.DataProcessor()
   
   # Gather and clean training set data
   trainingSet = []
   dictionary = set()
   tags = []
   processor.compileTrainingSet("posts.xml", 1, trainingSet, dictionary, 161, tags)
   print "Size of training set = " + str(len(trainingSet))
   
   # Gather and clean test set data
   testSet = []
   processor.compileTestSet("test.xml", 1, testSet)
   print "Size of test set = " + str(len(testSet))
   
   # Construct the SVM classifiers and train each
   svmClassifiers = {}
   X = processor.packRowsForSVM(trainingSet)
   print "Training the SVM classifiers"
   timer = Timer.Timer("Training", len(tags))
   for tag in tags:
      svmClassifier = SVMClassifier.SVMClassifier()
      Y = processor.getTagVector(trainingSet, tag)
      svmClassifier.train(X, Y, list(dictionary))
      svmClassifiers[tag] = svmClassifier
      #print "Trained SVM classifier for tag: " + tag
      timer.tick()
   timer.stop()
   
   # Use the SVM classifiers to predict the tags
   print "Testing the SVM classifiers"
   timer = Timer.Timer("Testing", len(tags))
   X = processor.packRowsForSVM(testSet)
   metrics = {}
   for tag in tags:
      predictions = svmClassifiers[tag].classify(X)
      # TODO: Redundant call
      actual = processor.getTagVector(trainingSet, tag)
      metrics[tag] = svmClassifiers[tag].evaluatePredictions(predictions, actual)
      timer.tick()
   timer.stop()
   
   # Compile and print out the metrics for the prediction
   count = 1
   TPSum = 0
   FPSum = 0
   TNSum = 0
   FNSum = 0
   for tag in tags:
      TP = metrics[tag]["TP"]
      FP = metrics[tag]["FP"]
      TN = metrics[tag]["TN"]
      FN = metrics[tag]["FN"]
      if TP + FP:
         precision = float(float(TP)/(float(TP) + float(FP)))
      else:
         precision = "NA"
      if TP + FN:
         recall = float(float(TP)/(float(TP) + float(FN)))
      else:
         recall = "NA"
      if precision != 0 and precision != "NA" and recall != 0 and recall != "NA":
         fmeasure = float(2*precision*recall/(precision + recall))
      else:
         fmeasure = "NA"
      print str(count) + ". " + tag + "(" + str(TP) + ", " + str(FP) + ", " + str(TN) + ", " + str(FN) + ", " + str(precision) + ", " + str(recall) + ", " + str(fmeasure) + ")"
      count += 1
      TPSum += metrics[tag]["TP"]
      FPSum += metrics[tag]["FP"]
      TNSum += metrics[tag]["TN"]
      FNSum += metrics[tag]["FN"]
      
   print "Total hits (TP) = " + str(TPSum)
   print "Total FP = " + str(FPSum)
   print "Total TN = " + str(TNSum)
   print "Total FN = " + str(FNSum)
   precision = float(float(TPSum)/(float(TPSum) + float(FPSum)))
   print "Precision = " + str(precision)
   recall = float(float(TPSum)/(float(TPSum) + float(FNSum)))
   print "Recall = " + str(recall)
   fmeasure = float(2*precision*recall/(precision + recall))
   print "fMeasure = " + str(fmeasure)

   return
   
if __name__ == '__main__':
    main()
