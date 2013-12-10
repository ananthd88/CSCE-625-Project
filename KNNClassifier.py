import re
import signal
import sys
import json
import math
import bisect
import random
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
import numpy as np
from sklearn.decomposition import PCA


def innerdict():
	return defaultdict(float)

main_dict=defaultdict(innerdict)
query_dict=defaultdict(innerdict)
document_freq_dict=defaultdict(float)
resultSet=defaultdict(float)
predicted_set_cluster=defaultdict(set)
token_dict = defaultdict(list)

k_value=0
no_top_tags=0
testing_doc_count=0
matchResults = 0
training_set_cluster=defaultdict(set)
testing_set_cluster=defaultdict(set)
training_doc_count=0
st = LancasterStemmer()
wnl = WordNetLemmatizer()



def handler(signal, frame):
    print 'You pressed Ctrl+C!..Quiting'
    sys.exit(0)


def loadQueries(fileloc):
    setTags=set()
    global training_doc_count
    global set_of_tokens
    xml_data=open(fileloc,'r')
    buf=xml_data.readlines()
    xml_data.close()
    count = 10
    for line in buf:
        #if count < 0:
        #   break
        #count =count -1
        #print line
        match = re.search('<row(.*)Body="(.*)" OwnerUserId(.*)Title="(.*)"(.*)Tags="(.*)" Answer(.*)/>', line)
        if match:
            body=match.group(2)
            tokens_in_body = re.findall(r"[\w-]+", body,re.UNICODE)
            valid_tokens=filter(lambda x: x not in stopwords.words('english') and len(x) >= 3,tokens_in_body)
            title=match.group(4)
            tokens_in_title = re.findall(r"[\w-]+",title,re.UNICODE)
            valid_tokens_in_title=filter(lambda x: x not in stopwords.words('english') and len(x) >= 3, tokens_in_title)
            valid_tokens.extend(valid_tokens_in_title)
            tags=match.group(6)
            tokens_in_tags = re.findall(r"[\w-]+", tags,re.UNICODE)
            valid_tags=filter(lambda x: x not in stopwords.words('english') and len(x) >= 3, tokens_in_tags)
            #print valid_tokens
            #print valid_tags
            training_set_cluster[training_doc_count]=set(valid_tags)
            for x in valid_tags:
                setTags.add(x)
            add_values_to_dict(valid_tokens,training_doc_count)
            training_doc_count +=1
    print len(main_dict)
    print len(setTags)
    print len(document_freq_dict)


def calculate_pca():
    main_list=[]
    #for doc in main_dict:
    #    for token in document_freq_dict:
    #        token_dict[token].append(main_dict[doc][token])
    #for token in token_dict:
    #    main_list.append(token_dict[token])
    for doc in main_dict:
        for token in document_freq_dict:
            y=main_dict[doc][token]
            token_dict[doc].append(y)
    for doc in token_dict:
        main_list.append(token_dict[doc])
    #print main_list
    X = np.array(main_list)
    print X.shape
    pca = PCA()
    Y = pca.fit_transform(X)
    #print Y
    print Y.shape
    print len(pca.explained_variance_ratio_)




            


'''
Module to add term in Main dictionary and Document Frequency table
'''

def add_values_to_dict(tokens,id_val):
    set_of_tokens= set()
    for token in tokens:
        token =wnl.lemmatize(token.lower())
        main_dict[id_val][token]+=1
        set_of_tokens.add(token)
    for elem in set_of_tokens:
        elem=elem.lower()
        document_freq_dict[elem]+=1
    calculate_tf_value(id_val)
    return


'''
Module to calculate tf value for each term
'''

def calculate_tf_value(id_val):
    for token in main_dict[id_val]:
        value=main_dict[id_val][token]
        main_dict[id_val][token]=1+math.log(value,2)




def create_training_set():
	calculate_idf_value(training_doc_count)
	calculate_tf_idf_value()
	normalize_tf_idf_value()


'''
Module to normalize tf-idf values
'''

def normalize_tf_idf_value():
		global main_dict
		for doc in main_dict:
			square=0
			for term in main_dict[doc]:
				square=square+ main_dict[doc][term]* main_dict[doc][term]
			if square == 0:
				continue
			sq_root=math.sqrt(square)
			for term in main_dict[doc]:
				value= main_dict[doc][term]
				main_dict[doc][term]=value/sq_root


'''
Module to calculate tf-idf value for each term
'''

def calculate_tf_idf_value():
	for doc in main_dict:
		for term in main_dict[doc]:
			value= main_dict[doc][term]
                        #print "doc" ,doc ,"term",term, value, document_freq_dict[term]
			main_dict[doc][term]=value*document_freq_dict[term]


'''
Module to calculate idf value for each term
'''

def calculate_idf_value(total_docs):
	for token in document_freq_dict:
		value=document_freq_dict[token]
		document_freq_dict[token]=math.log(total_docs/value,2)
							       


def loadTestQuery(fileloc):
    global testing_doc_count
    global predicted_set_cluster
    global matchResults
    matchResults = 0
    predicted_set_cluster.clear()
    testing_doc_count = 0
    xml_data=open(fileloc,'r')
    buf=xml_data.readlines()
    xml_data.close()
    count = 10
    for line in buf:
        #if count < 0:
        #    break
        count =count -1
        #print "Post:"
        #print
        #print line
        #print " Testing doc Count ",testing_doc_count
        match = re.search('<row(.*)Body="(.*)" OwnerUserId(.*)Title="(.*)"(.*)Tags="(.*)" Answer(.*)/>', line)
        if match:
            body=match.group(2)
            tokens_in_body = re.findall(r"[\w-]+", body,re.UNICODE)
            valid_tokens=filter(lambda x: x not in stopwords.words('english') and len(x) >= 3,tokens_in_body)
            title=match.group(4)
            tokens_in_title = re.findall(r"[\w-]+",title,re.UNICODE)
            valid_tokens_in_title=filter(lambda x: x not in stopwords.words('english') and len(x) >= 3, tokens_in_title)
            valid_tokens.extend(valid_tokens_in_title)
            #print " Valid Tokens",valid_tokens
            tags=match.group(6)
            tokens_in_tags = re.findall(r"[\w-]+", tags,re.UNICODE)
            valid_tags=filter(lambda x: x not in stopwords.words('english') and len(x) >= 3, tokens_in_tags)
            #print " Valid Tags",valid_tags
            testing_set_cluster[testing_doc_count]=set(valid_tags)
            calculate_KNN(valid_tokens,testing_doc_count)
            testing_doc_count += 1


'''
Module to calculate the k nearest neigbours for a particular doc
'''

def calculate_nearest_k_neigbours(doc_id):
	global resultSet
        global no_top_tags
        global k_value
	resultSet=defaultdict(float)
	for doc in main_dict:
		value=0
		for token in query_dict[doc_id]:
			if token in main_dict[doc]:
				value=value+query_dict[doc_id][token]*main_dict[doc][token]
		if value > 0:
			resultSet[doc]=value
	results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
	k_nearest=[elem[0] for elem in results][-k_value:]
	k_nearest_similarity=[elem[1] for elem in results][-k_value:]
        #print "k_nearest",k_nearest
        #print "k_nearest_similarity",k_nearest_similarity
	resultSet=defaultdict(float)
        for elem in k_nearest:
            #print training_set_cluster[elem]
            for tag in training_set_cluster[elem]:
                resultSet[tag] +=1
        results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
        #print "Top 3 Tags"
        #print
        resultList=set()
        for i in range(1,no_top_tags+1):
            #print results[-i][0]
            if i > len(results):
                break
            resultList.add(results[-i][0])

	return resultList

'''
K-NN Algorithm
'''
def calculate_KNN(tokens,doc_id):
        global predicted_set_cluster
        global matchResults
	create_testSet(tokens,doc_id)
	predicted_set_cluster[doc_id]=calculate_nearest_k_neigbours(doc_id)
        outputList=[val for val in predicted_set_cluster[doc_id] if val in testing_set_cluster[doc_id]]
        if len(outputList) != 0:
            #print predicted_set_cluster[doc_id]," actual tags  ",testing_set_cluster[doc_id]
            matchResults +=1
        #if predicted_set_cluster[doc_id] == actual_cluster_id:
	#	match += 1


'''
Module to calculate tf-idf value for each term of a particular testing doc
'''
def create_testSet(tokens,doc_id):
	global query_dict
	query_dict=defaultdict(innerdict)
	square=0
	for token in tokens:
		token=wnl.lemmatize(token.lower())
		query_dict[doc_id][token]+=1
	for token in query_dict[doc_id]:
	        value=query_dict[doc_id][token]
	        value=1+math.log(value,2)
		if token in document_freq_dict:
	         	query_dict[doc_id][token]=value*document_freq_dict[token]
		square+=query_dict[doc_id][token] * query_dict[doc_id][token]	
        if square==0:
		return 2
        sq_root=math.sqrt(square)
        for token in query_dict[doc_id]:
	        value= query_dict[doc_id][token]
	        query_dict[doc_id][token]=value/sq_root
	return 1


def main():
    global k_value
    global no_top_tags
    print "Loading Training Set from Local file"
    print
    signal.signal(signal.SIGINT, handler)
    fileloc="posts.xml"
    loadQueries(fileloc)
    create_training_set();
    print "Loading Testing Set from Local file"
    print
    fileloc="test.xml"
    for k_value in [5, 10,20, 50,100,200]:
        for no_top_tags in [1,2, 3, 5, 7,10]:
            loadTestQuery(fileloc)
            print " K Value :",k_value," No of Top Tags",no_top_tags,"Total Matches",matchResults



if __name__ == '__main__':
    main()


