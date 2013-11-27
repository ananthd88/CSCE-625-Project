from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
import Timer

class OneVsRest:
   def __init__(self):
      self.classifier = None
      return
   def train(self, X, Y):
      self.classifier = Pipeline([
         ('vectorizer', CountVectorizer(min_n=1,max_n=2)),
         ('tfidf', TfidfTransformer()),
         ('clf', OneVsRestClassifier(LinearSVC(class_weight='auto'), n_jobs = -2))])
      timer = Timer.Timer("Training")
      self.classifier.fit(X, Y)
      timer.stop()
      return
   def classify(self, X):
      timer = Timer.Timer("Testing")
      predicted = self.classifier.predict(X)
      timer.stop()
      return predicted
