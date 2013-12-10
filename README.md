CSCE-625-Project
================


Project:   Identify keywords and tags from millions of text questions on a StackExchange site. 

Team
---
Ananth Dileepkumar 

Johnu George 

Karthik Venugopal 

Sreevatsan Vaidyanathan




Executible programs:

classifier.py - Preprocesses the data using PCA and performs tagging using KNN algorithm.

How to Run
---------
python classifier.py

KNNclassifier.py - Modified form of classifier.py to produce results for various values of k, number of top tags.

How To Run
----------
python KNNClassifier.py

TagSVM.py - Performs tagging using SVM classifiers (Each tag gets it's own SVM classifier)

How to Run
----------
python TagSVM.py

TagOVR.py - Performs tagging using OneVsRest Classifier with LinearSVM Classifiers as estimators

How to Run
----------
python TagOVR.py

