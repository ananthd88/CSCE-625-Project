import re;

postHasTags = re.compile(r'<row.*Tags="([^ ]*)" .*/>', re.IGNORECASE);
postHasBody = re.compile(r'<row.*Body="([^"]*)" .*/>', re.IGNORECASE);

if __name__=="__main__":
    orig_fileName = 'posts.xml';
    copied_fileName = "copied-"+orig_fileName;

    copiedPosts = 0;

    writeToFile = open(copied_fileName, 'w');
    writeToFile.write('<?xml version="1.0" encoding="utf-8"?>\n');
    writeToFile.write('<posts>\n');

    for line in open(orig_fileName, 'r'):
        tagsMatcher = postHasTags.match(line.strip());
        bodyMatcher = postHasBody.match(line.strip());
        if tagsMatcher and bodyMatcher:
            writeToFile.write(line);
            copiedPosts +=1;

    writeToFile.write('</posts>');
    writeToFile.close();

    print str(copiedPosts)+" posts copied.";
