from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

class SVMClassifier:
   def __init__(self):
      self.vectorizer = None
      self.classifier = None
   def train(self, X, Y, dictionary):
      self.classifier = svm.LinearSVC(C = 5.0, dual = True, verbose = 0)
      self.vectorizer = CountVectorizer(vocabulary = dictionary, min_df = 1)
      strings = []
      for tokenArray in X:
         strings.append(" ".join(tokenArray))         
      X = self.vectorizer.fit_transform(strings)
      self.classifier.fit(X, Y)
   def classify(self, X):
      strings = []
      for tokenArray in X:
         strings.append(" ".join(tokenArray))         
      X = self.vectorizer.fit_transform(strings)
      return self.classifier.predict(X)
   def evaluatePredictions(self, predictions, actual):
      TP = 0
      FP = 0
      TN = 0
      FN = 0
      for i in range(len(predictions)):
         if actual[i]:
            if predictions[i]:
               TP += 1
            else:
               FN += 1
         else:
            if predictions[i]:
               FP += 1
            else:
               TN += 1
      return {"TP": TP, "FP": FP, "TN": TN, "FN": FN}

   #TODO: Remove this function if no longer needed
   def classify0(self, tokenArray):
      string = []
      string.append(" ".join(tokenArray))
      Z = self.vectorizer.fit_transform(string)
      return self.classifier.predict(Z)[0]
