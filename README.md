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
KNNclassifier.py - Modified form of classifier.py to produce results for various values of k, number of top tags.
TagSVM.py - Performs tagging using SVM classifiers (Each tag gets it's own SVM classifier)
TagOVR.py - Performs tagging using OneVsRest Classifier with LinearSVM Classifiers as estimators

