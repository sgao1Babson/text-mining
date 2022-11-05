import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from thefuzz import fuzz

def process_file(filename, skip_header):
    """Makes a histogram that contains the words from a file.
    filename: string
    skip_header: boolean, whether to skip the Gutenberg header
    returns: map from each word to the number of times it appears.
    """
    hist = {}
    fp = open(filename, encoding='UTF8')

    if skip_header:
        for line in fp:
            if line.startswith('David Reed'):
                break

    strippables = string.punctuation + string.whitespace

    for line in fp:
        if line.startswith('FINIS'):
            break

        line = line.replace('-', ' ')
        line = line.replace('”', ' ')
        line = line.replace('“', ' ')


        for word in line.split():
            # word could be 'Sussex.'
            word = word.strip(strippables)
            word = word.lower()

            # update the dictionary
            hist[word] = hist.get(word, 0) + 1

    return hist

def total_words(hist):
    """
    Returns the total frequencies(word count) of the histogram text.
    """
    total = 0
    for freq in hist.values():
        total += freq
    return total

def different_words(hist):
    """
    Returns the number of different/unique words in the histogram.
    """
    return len(hist)


def most_common(hist, range):
    """
    Makes a list of word-freq pairs in descending order of frequency.
    hist: map from word to frequency
    returns: list of (word, frequency pairs
    """
    a = sorted(hist.items(), key=lambda item:item[1],reverse=True)
    for word, freq in a[0:range]:
        print(word, '\t', freq)


def stopwords():
    stopwords = process_file('data/stopwords.txt', False)
    stopwords = list(stopwords.keys())
    
    return stopwords

def most_common_exclude_stopwords(hist,range):
    """
    Makes a list of words freq pairs in descending order of frequency excluding stopwords in a given range
    returns: list of (frequency, word) pairs
    """

    s = stopwords()
    a = []
    for word, freq in hist.items():
        if word in s:
            continue
        a.append((freq,word))

    a.sort(reverse=True)

    return a[0:range]

def most_common_exclusive(hist1, hist2, range):
    """
    Makes a list which returns the unique words that excludes the stopwords in a given range.
    """

    s = stopwords()

    a = []
    for word1, freq1 in hist1.items():
        if word1 in s:
            continue
        a.append((freq1,word1))
    a.sort(reverse=True)

    b = []
    for word2, freq2 in hist2.items():
        if word2 in s:
            continue
        b.append((word2))


    c = []
    for freq,word in a:
        if word not in b:
            c.append((freq,word))
    
    c.sort(reverse=True)
    return c[0:range]


def sentiment_hist(hist):
    """
    Convert the text histogram dictionary into a string to perform the sentiment analysis
    """
    sentence = str(hist)
    score = SentimentIntensityAnalyzer().polarity_scores(sentence)
    print (score)


def ratio_difference(hist1, hist2):
    """
    Difference between the two histograms in partial ratios, so punctuations are not considered.
    """
    fuzz.partial_ratio(hist1, hist2) 
    return ratio_difference(hist1, hist2)

    


def main():
    hist_hamlet = process_file('data/Hamlet.txt', skip_header=True)
    hist_macbeth = process_file('data/Macbeth.txt', skip_header=True)
    print('Total number of words in Hamlet:', total_words(hist_hamlet),'Total number of words in Macbeth:',total_words(hist_macbeth))
    print('Number of different words in Hamlet:', different_words(hist_hamlet),'Number of different words in Macbeth',different_words(hist_macbeth))

    print('The 20 most common words in hamlet are:')
    most_common(hist_hamlet, 20)
    print('The 20 most common words in macbeth are:')
    most_common(hist_macbeth, 20)
    
    print('The top 20 most common words and its frequency in Hamlet excluding stopwords are:')
    print(most_common_exclude_stopwords(hist_hamlet,20))
    print('The top 20 most common words and its frequency in Macbeth excluding stopwords are:')
    print(most_common_exclude_stopwords(hist_macbeth,20))

    print('The most common words in Hamlet that are not in Macbeth are:')
    print(most_common_exclusive(hist_hamlet,hist_macbeth,20))
    print('The most common words in Macbeth that are not in Hamlet are:')
    print(most_common_exclusive(hist_macbeth,hist_hamlet,20))



    print('This is the sentiment analysis for the Hamlet text:')
    sentiment_hist(hist_hamlet)
    print('This is the sentiment analysis for the Macbeth text:')
    sentiment_hist(hist_macbeth)

    #The last fuzz ratio analysis is not performed because it takes too long to process. 
    #print(ratio_difference(hist_hamlet,hist_macbeth))

if __name__ == '__main__':
    main()

