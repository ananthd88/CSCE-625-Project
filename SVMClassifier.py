from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

class SVMClassifier:
   def __init__(self):
      self.vectorizer = None
      self.classifier = svm.LinearSVC(C = 5.0, dual = True, verbose = 0)
   def train(self, X, Y, dictionary):
      self.vectorizer = CountVectorizer(vocabulary = dictionary, min_df = 1)
      strings = []
      for tokenArray in X:
         strings.append(" ".join(tokenArray))         
      X = self.vectorizer.fit_transform(strings)
      self.classifier.fit(X, Y)
   def classify(self, tokenArray):
      string = []
      string.append(" ".join(tokenArray))
      Z = self.vectorizer.fit_transform(string)
      return self.classifier.predict(Z)[0]
