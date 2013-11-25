import re;

postHasTags = re.compile(r'<row.*Tags="([^ ]*)" .*/>', re.IGNORECASE);
postHasBody = re.compile(r'<row.*Body="([^"]*)" .*/>', re.IGNORECASE);

if __name__=="__main__":
    orig_fileName = 'posts.xml';
    training_fileName = "training-"+orig_fileName;
    test_fileName = "test-"+orig_fileName;

    validPosts = 0;

    writeToTrainingFile = open(training_fileName, 'w');
    writeToTrainingFile.write('<?xml version="1.0" encoding="utf-8"?>\n');
    writeToTrainingFile.write('<posts>\n');
    
    writeToTestFile = open(test_fileName, 'w');
    writeToTestFile.write('<?xml version="1.0" encoding="utf-8"?>\n');
    writeToTestFile.write('<posts>\n');

    for line in open(orig_fileName, 'r'):
        tagsMatcher = postHasTags.match(line.strip());
        bodyMatcher = postHasBody.match(line.strip());
        if tagsMatcher and bodyMatcher:
            validPosts+=1;

    testPosts=0;
    copiedPosts=0;

    for line in open(orig_fileName, "r"):
        tagsMatcher = postHasTags.match(line.strip());
        bodyMatcher = postHasBody.match(line.strip());
        if tagsMatcher and bodyMatcher:
            if(copiedPosts%10==0):
                print "Using post number "+str(copiedPosts);
                testPosts+=1;
                writeToTestFile.write(line);
            else:
                writeToTrainingFile.write(line);

            copiedPosts+=1;

    writeToTrainingFile.write('</posts>');
    writeToTrainingFile.close();

    writeToTestFile.write('</posts>');
    writeToTestFile.close();

    print str(copiedPosts)+" posts in training set.";
    print str(testPosts)+" posts in test set.";
