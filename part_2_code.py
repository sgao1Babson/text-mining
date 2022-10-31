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

def most_common_words(hist,range):
    """
    Makes a list of words freq pairs in descending order of frequency.
    hist: map from word to frequency
    returns: list of (frequency, word) pairs
    """
    a = sorted(hist.items(), key=lambda item:item[1],reverse=True)
    a_words = []
    for word, freq in a[0:range]:
        a_words.append(word)
    return a_words

def most_common_exclusive(hist1,range1, hist2, range2):
    """
    Makes a list which returns the most frequent unique words from one histogram that is not in the other histogram in a given range of frequency. 
    """
    a = most_common_words(hist1,range1)
    b = most_common_words(hist2,range2)

    c_words = []
    for word in a:
        if word not in b:
            c_words.append(word)
    return c_words


def most_common_both(hist1,range1,hist2,range2):
    """
    Makes a list which returns the most frequent unique words from the two histograms in a given range of frequency.
    """
    a = most_common_words(hist1,range1)
    b = most_common_words(hist2,range2)

    c_words = []
    for i in a:
        if i not in b:
            c_words.append(i)
    for y in b:
        if y not in a:
            c_words.append(y)
    return c_words



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

    print('The 10 most common words in hamlet are:')
    most_common(hist_hamlet, 10)
    print('The 10 most common words in macbeth are:')
    most_common(hist_macbeth, 10)
    
    print('The top 10 most common words and its frequency in Hamlet are:')
    print(most_common_words(hist_hamlet,10))
    print('The top 10 most common words and its frequency in Macbeth are:')
    print(most_common_words(hist_macbeth,10))

    print('The most common words in Hamlet that are not in Macbeth are:')
    print(most_common_exclusive(hist_hamlet,20,hist_macbeth,20))
    print('The most common words in Macbeth that are not in Hamlet are:')
    print(most_common_exclusive(hist_macbeth,20,hist_hamlet,20))


    print('The most common words from the two books that do not overlap looking at the 30 most frequient word:')
    print(most_common_both(hist_hamlet,30,hist_macbeth,30))
    print('The most common words from the two books that do not overlap looking at the 40 most frequient word:')
    print(most_common_both(hist_hamlet,40,hist_macbeth,40))


    print('This is the sentiment analysis for the Hamlet text:')
    sentiment_hist(hist_hamlet)
    print('This is the sentiment analysis for the Macbeth text:')
    sentiment_hist(hist_macbeth)

    #The last fuzz ratio analysis is not performed because it takes too long to process. 
    #print(ratio_difference(hist_hamlet,hist_macbeth))

if __name__ == '__main__':
    main()

