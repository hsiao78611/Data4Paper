
# NLTK  (Natural Language Tool Kit)
## 彭師孝 (Sean)
2017/08/10

# Agenda

1. Introduction to NLTK
2. Getting Started with NLTK
3. Accessing Text Corpora and Lexical Resources
4. Processing Raw Text with NLTK
5. Categorizing and Tagging Words
6. Learning to Classify Text
7. Extracting Information from Text
8. Scikit-Learn Sklearn with NLTK
9. Sentiment Analysis with NLTK
10. Saving Classifiers with NLTK (Python object serialization)


# 1. Introduction to NLTK

* A suite of libraries and programs for symbolic and statistical NLP in the Python.
* First developed in 2001 as part of a computational linguistics course at University of Pennsylvania.
* Available for Windows, Mac OS X, and Linux. 
* Free, Open-source


# Wiki
The Natural Language Toolkit, or more commonly NLTK, is a suite of libraries and programs for symbolic and statistical natural language processing (NLP) for English written in the Python programming language. It was developed by Steven Bird and Edward Loper in the Department of Computer and Information Science at the University of Pennsylvania.[5] NLTK includes graphical demonstrations and sample data. It is accompanied by a book that explains the underlying concepts behind the language processing tasks supported by the toolkit,[6] plus a cookbook.[7]

NLTK is intended to support research and teaching in NLP or closely related areas, including empirical linguistics, cognitive science, artificial intelligence, information retrieval, and machine learning.[8] NLTK has been used successfully as a teaching tool, as an individual study tool, and as a platform for prototyping and building research systems. There are 32 universities in the US and 25 countries using NLTK in their courses. NLTK supports classification, tokenization, stemming, tagging, parsing, and semantic reasoning functionalities.[9]



## Goals of NLTK


### GOALS
* Simplicity
* Consistency
* Extensibility
* Modularity

### NON-GOALS
* Encyclopedic coverage
* Optimization
* Clever tricks 
 

## Over 50 Corpora and Lexical Resources
http://www.nltk.org/nltk_data/

* WordNet
* Libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning
* Wrappers for industrial-strength NLP libraries

<img style="width: 600px;" src="https://github.com/hsiao78611/Data4Paper/blob/master/notebooks/pic/resources.png">

## Explanation of Common NLP Terms

### Corpus or Corpora
A usually large collection of documents that can be used to infer and validate linguistic rules, 
as well as to do statistical analysis and hypothesis testing.
### Lexicon
Words and their meanings. Example: English dictionary. 
Consider, however, that various fields will have different lexicons.
### Token
Each "entity" that is a part of whatever was split up based on rules. 
For examples, 
* each word is a token when a sentence is "tokenized" into words. 
* each sentence can also be a token, if you tokenized the sentences out of a paragraph.


# 2. Getting Started with NLTK
## Installation on Mac

    pip3 install nltk
    nltk.download()
    
<img style="width: 600px;" src="https://github.com/hsiao78611/Data4Paper/blob/master/notebooks/pic/nltk_download.png">

## 3. Accessing Text Corpora and Lexical Resources

### 3.1 Common structures for text corpora
<br/>
<img style="width: 800px;" src="http://www.nltk.org/images/text-corpus-structure.png">


```python
from nltk.corpus import twitter_samples
```


```python
twitter_samples.fileids()
```




    ['negative_tweets.json', 'positive_tweets.json', 'tweets.20150430-223406.json']




```python
neg_tweets = twitter_samples.strings('negative_tweets.json')
pos_tweets = twitter_samples.strings('positive_tweets.json')
tweets = twitter_samples.strings('tweets.20150430-223406.json')
```


```python
list(map(len,[neg_tweets, pos_tweets, tweets]))
```




    [5000, 5000, 20000]




```python
neg_tweets[0]
```




    'hopeless for tmr :('




```python
pos_tweets[0]
```




    '#FollowFriday @France_Inte @PKuchly57 @Milipol_Paris for being top engaged members in my community this week :)'




```python
from nltk.corpus import stopwords
```


```python
print(stopwords.words('english'))
```

    ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']



```python
print(stopwords.fileids())
```

    ['danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'kazakh', 'norwegian', 'portuguese', 'romanian', 'russian', 'spanish', 'swedish', 'turkish']


## 3.2 Conditional Frequency Distributions


```python
from nltk.corpus import brown
```

The Brown Corpus was the first million-word electronic corpus of English, created in 1961 at Brown University. This corpus contains text from 500 sources, and the sources have been categorized by genre, such as news, editorial, and so on.


```python
cfd = nltk.ConditionalFreqDist((genre, word)
    for genre in brown.categories()
    for word in brown.words(categories=genre))
genres = ['romance', 'humor']
modals = ['can', 'could', 'may', 'might', 'must', 'will']
cfd.tabulate(conditions=genres, samples=modals)
```

              can could   may might  must  will 
    romance    74   193    11    51    45    43 
      humor    16    30     8     8     9    13 



```python
print(brown.categories())
```

    ['adventure', 'belles_lettres', 'editorial', 'fiction', 'government', 'hobbies', 'humor', 'learned', 'lore', 'mystery', 'news', 'religion', 'reviews', 'romance', 'science_fiction']



```python
print(brown.words(categories='humor'))
```

    ['It', 'was', 'among', 'these', 'that', 'Hinkle', ...]



```python
print(cfd.conditions())
```

    ['adventure', 'belles_lettres', 'editorial', 'fiction', 'government', 'hobbies', 'humor', 'learned', 'lore', 'mystery', 'news', 'religion', 'reviews', 'romance', 'science_fiction']



```python
print(cfd['romance'].most_common(200))
```

    [(',', 3899), ('.', 3736), ('the', 2758), ('and', 1776), ('to', 1502), ('a', 1335), ('of', 1186), ('``', 1045), ("''", 1044), ('was', 993), ('I', 951), ('in', 875), ('he', 702), ('had', 692), ('?', 690), ('her', 651), ('that', 583), ('it', 573), ('his', 559), ('she', 496), ('with', 460), ('you', 456), ('for', 410), ('at', 402), ('He', 366), ('on', 362), ('him', 339), ('said', 330), ('!', 316), ('--', 291), ('be', 289), ('as', 282), (';', 264), ('have', 258), ('but', 252), ('not', 250), ('would', 244), ('She', 232), ('The', 230), ('out', 217), ('were', 214), ('up', 211), ('all', 209), ('from', 202), ('could', 193), ('me', 193), ('like', 185), ('been', 179), ('so', 174), ('there', 169), ('they', 168), ('one', 166), ('about', 164), ('my', 156), ('an', 152), ('or', 150), ('is', 150), ('this', 149), ('It', 144), ('them', 142), ('if', 142), ('into', 136), ('But', 135), ('And', 129), ('down', 127), ('when', 126), ('back', 126), ('no', 123), ('what', 121), ('did', 115), ('their', 114), ('do', 109), ('by', 107), ('only', 106), ('your', 106), ('thought', 105), ('which', 104), ('You', 102), ("didn't", 101), ('then', 101), ('just', 100), ('little', 99), ('time', 93), ('too', 92), ('get', 92), ('who', 89), ('got', 89), ('before', 88), ('know', 88), ('over', 88), ('man', 87), ('because', 85), ('more', 85), ('never', 84), ('way', 83), ('now', 83), ('went', 82), ('we', 78), ("I'm", 77), ('eyes', 76), ('go', 76), ('came', 75), ('see', 74), ('can', 74), ('old', 73), ('come', 73), ('even', 73), ('are', 72), ('looked', 72), ('other', 70), ('They', 69), ('its', 69), ('knew', 69), ('some', 69), ('much', 69), ('around', 68), ('any', 67), ('There', 66), ('here', 65), ('long', 65), ('than', 65), ('good', 65), ('away', 64), ('felt', 64), ('day', 63), ('own', 63), ('still', 62), ('made', 62), ('take', 62), ("don't", 62), ('say', 60), ('going', 60), ('how', 60), ('something', 59), ('after', 58), ('through', 56), (':', 56), ('off', 56), ('think', 56), ('In', 55), ('right', 55), ('night', 54), ('where', 54), ('look', 54), ('those', 53), ('again', 53), ('himself', 53), ("I'll", 53), ('thing', 52), ('first', 52), ('might', 51), ('seemed', 51), ('life', 51), ('very', 50), ('What', 50), ("wasn't", 50), ('always', 49), ('left', 49), ('make', 49), ('young', 49), ('put', 49), ('being', 49), ('people', 48), ('while', 48), ('took', 48), ('two', 48), ('turned', 48), ('A', 48), ('nothing', 47), ('saw', 47), ('told', 47), ('head', 46), ("couldn't", 46), ('home', 46), ('asked', 45), ('place', 45), ('room', 45), ('must', 45), ('His', 44), ('mother', 44), ('face', 44), ('wanted', 44), ('last', 44), ('Phil', 44), ('door', 43), ('next', 43), ('will', 43), ('against', 42), ('anything', 42), ('us', 42), ('Then', 42), ('No', 40), ('herself', 40), ('enough', 40), ('morning', 40), ('let', 39), ('Mrs.', 39), ('John', 39), ('once', 38), ('This', 38)]



```python
cfd['romance']['could']
```




    193




```python
twitter_samples.categories()
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-430-b9c8fe382662> in <module>()
    ----> 1 twitter_samples.categories()
    

    AttributeError: 'TwitterCorpusReader' object has no attribute 'categories'



```python
twitter_samples.words()
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-420-1075e8274ffe> in <module>()
    ----> 1 twitter_samples.words()
    

    AttributeError: 'TwitterCorpusReader' object has no attribute 'words'



```python
from nltk.tokenize import TweetTokenizer as tknzr
pos_tweets = twitter_samples.tokenized('positive_tweets.json')
```


```python
tweet_words = [word
               for i in range(len(pos_tweets))
               for word in pos_tweets[i]]
```


```python
print(nltk.FreqDist(tweet_words).most_common(200))
```

    [(':)', 3691), ('!', 1844), ('you', 1341), ('.', 1341), ('to', 1065), ('the', 999), (',', 964), ('I', 890), ('a', 888), ('for', 749), (':-)', 701), ('and', 660), (':D', 658), ('?', 581), (')', 525), ('my', 484), ('in', 481), ('it', 460), ('is', 418), ('of', 403), ('have', 342), ('me', 330), ('your', 320), ('on', 313), ('...', 290), ('follow', 284), ('"', 264), ('this', 263), ('be', 249), (':', 249), ('that', 246), ('so', 234), ('u', 228), ('with', 221), ('-', 213), ('like', 209), ('Thanks', 209), ('i', 203), ('day', 202), ('all', 197), ('are', 184), ('love', 184), ('thanks', 182), ('&', 174), ('will', 168), ('at', 167), ('good', 162), ("I'm", 161), ('back', 154), ('just', 152), ('we', 146), ('but', 141), ('know', 141), ('Hi', 141), ('can', 139), ('get', 139), (':p', 138), ('great', 138), ('up', 138), ('<3', 135), ('was', 133), ('Thank', 131), ('do', 131), ('our', 130), ('if', 130), ('..', 129), ('too', 127), ('new', 126), ('not', 123), ('one', 113), ('now', 113), ('thank', 113), ('about', 112), ('an', 110), ('out', 110), ('us', 109), ('see', 109), ('time', 105), ("it's", 105), ('Happy', 104), ('today', 104), ('from', 103), ('more', 100), ("'", 100), ('as', 98), ('You', 97), ('here', 95), ('Friday', 92), ('Have', 89), ('some', 87), ('via', 85), ('hope', 84), ('nice', 84), ("I'll", 83), ('much', 83), ('(', 82), ('The', 82), ('what', 81), ('Love', 80), ('happy', 79), ('We', 77), ('lot', 76), ('when', 76), ('there', 75), ('*', 73), ('go', 71), ('1', 71), ('no', 71), ('really', 71), ('week', 70), ('want', 69), ('>', 68), ('Good', 68), ('very', 68), ('am', 67), ('/', 67), ('x', 66), ("you're", 66), ('weekend', 66), ('arrived', 65), ('work', 65), ('going', 63), ('@jnlazts', 62), ('http://t.co/RCvcYYO0Iq', 62), ('morning', 62), ('them', 62), ('please', 62), ("don't", 61), ('NO', 61), ('would', 61), ('got', 60), ('Stats', 60), ('unfollowers', 60), ('My', 60), ('being', 58), ('Can', 58), ('how', 58), ('always', 58), ('night', 57), ('See', 57), ('make', 57), ('again', 57), ('or', 56), ("It's", 56), ('Hey', 55), ('fun', 55), ('well', 55), ('welcome', 55), ('2', 55), ('think', 55), ('lovely', 52), ('^', 52), ('need', 51), ('they', 51), ('sure', 50), ('loves', 50), ('everyone', 50), ('better', 50), ('he', 50), ('made', 50), ('bestfriend', 49), ('only', 49), ('She', 48), ('its', 48), ('still', 47), ('look', 47), ('yes', 47), ('next', 46), ('A', 46), ('follower', 46), ('best', 46), ('guys', 46), ('people', 46), ('him', 45), ('soon', 45), ('If', 45), ('amazing', 44), ('It', 44), ('BAM', 44), ('@BarsAndMelody', 44), ('@969Horan696', 44), ('Warsaw', 44), ('way', 44), ('been', 44), ('has', 43), ('done', 43), ('start', 43), ('Just', 43), ('So', 43), ('by', 42), ('birthday', 42), ('then', 42), ("that's", 42), ('xx', 41), ('right', 41), ('…', 40), ('come', 40), ('wait', 40), ('who', 40), ('Hello', 39)]


## 3.3 WordNet
WordNet is a semantically-oriented dictionary of English, similar to a traditional thesaurus but with a richer structure. NLTK includes the English WordNet, with 155,287 words and 117,659 synonym sets.

1. Benz is credited with the invention of the motorcar.
2. Benz is credited with the invention of the automobile.


```python
from nltk.corpus import wordnet as wn
wn.synsets('motorcar')
```




    [Synset('car.n.01')]



Thus, motorcar has just one possible meaning and it is identified as car.n.01, the first noun sense of car. The entity car.n.01 is called a synset, or "synonym set", a collection of synonymous words (or "lemmas"):


```python
wn.synset('car.n.01').lemma_names()
```




    ['car', 'auto', 'automobile', 'machine', 'motorcar']




```python
wn.synsets('auto')
```




    [Synset('car.n.01')]




```python
wn.synset('car.n.01').definition()
```




    'a motor vehicle with four wheels; usually propelled by an internal combustion engine'




```python
wn.synset('car.n.01').examples()
```




    ['he needs a car to get to work']



### Get all the lemmas for a given synset


```python
wn.synset('car.n.01').lemmas()
```




    [Lemma('car.n.01.car'),
     Lemma('car.n.01.auto'),
     Lemma('car.n.01.automobile'),
     Lemma('car.n.01.machine'),
     Lemma('car.n.01.motorcar')]



To eliminate ambiguity, we will identify these words as car.n.01.automobile, and so on. This pairing of a synset with a word is called a lemma.

### Look up a particular lemma


```python
wn.lemma('car.n.01.automobile')
```




    Lemma('car.n.01.automobile')



### Get the synset corresponding to a lemma


```python
wn.lemma('car.n.01.automobile').synset()
```




    Synset('car.n.01')



### Get the "name" of a lemma


```python
wn.lemma('car.n.01.automobile').name()
```




    'automobile'



For convenience, we can access all the lemmas involving the word car as follows.


```python
wn.lemmas('car')
```




    [Lemma('car.n.01.car'),
     Lemma('car.n.02.car'),
     Lemma('car.n.03.car'),
     Lemma('car.n.04.car'),
     Lemma('cable_car.n.01.car')]



### Compare the similarity of two words and their tenses


```python
w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('boat.n.01')
print(w1.wup_similarity(w2))
```

    0.9090909090909091



```python
w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('car.n.01')
print(w1.wup_similarity(w2))
```

    0.6956521739130435



```python
w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('cat.n.01')
print(w1.wup_similarity(w2))
```

    0.32


# 4. Processing Raw Text with NLTK

## 4.1 Normalizing Text
Often we want to go further than converting text to lowercase, and strip off any affixes, a task known as stemming. A further step is to make sure that the resulting form is a known word in a dictionary, a task known as lemmatization.


```python
raw = """DENNIS: Listen, strange women lying in ponds distributing 
        swords is no basis for a system of government.  Supreme 
        executive power derives from a mandate from the masses, 
        not from some farcical aquatic ceremony."""
tokens = word_tokenize(raw)
print(tokens)
```

    ['DENNIS', ':', 'Listen', ',', 'strange', 'women', 'lying', 'in', 'ponds', 'distributing', 'swords', 'is', 'no', 'basis', 'for', 'a', 'system', 'of', 'government', '.', 'Supreme', 'executive', 'power', 'derives', 'from', 'a', 'mandate', 'from', 'the', 'masses', ',', 'not', 'from', 'some', 'farcical', 'aquatic', 'ceremony', '.']


### Stemmers
NLTK includes several off-the-shelf stemmers, and if you ever need a stemmer you should use one of these in preference to crafting your own using regular expressions, since these handle a wide range of irregular cases.

For example, the Porter and Lancaster stemmers follow their own rules for stripping affixes: 


```python
print(tokens)
```

    ['DENNIS', ':', 'Listen', ',', 'strange', 'women', 'lying', 'in', 'ponds', 'distributing', 'swords', 'is', 'no', 'basis', 'for', 'a', 'system', 'of', 'government', '.', 'Supreme', 'executive', 'power', 'derives', 'from', 'a', 'mandate', 'from', 'the', 'masses', ',', 'not', 'from', 'some', 'farcical', 'aquatic', 'ceremony', '.']



```python
porter = nltk.PorterStemmer() # it's better
print([porter.stem(t) for t in tokens])
```

    ['denni', ':', 'listen', ',', 'strang', 'women', 'lie', 'in', 'pond', 'distribut', 'sword', 'is', 'no', 'basi', 'for', 'a', 'system', 'of', 'govern', '.', 'suprem', 'execut', 'power', 'deriv', 'from', 'a', 'mandat', 'from', 'the', 'mass', ',', 'not', 'from', 'some', 'farcic', 'aquat', 'ceremoni', '.']



```python
lancaster = nltk.LancasterStemmer()
print([lancaster.stem(t) for t in tokens])
```

    ['den', ':', 'list', ',', 'strange', 'wom', 'lying', 'in', 'pond', 'distribut', 'sword', 'is', 'no', 'bas', 'for', 'a', 'system', 'of', 'govern', '.', 'suprem', 'execut', 'pow', 'der', 'from', 'a', 'mand', 'from', 'the', 'mass', ',', 'not', 'from', 'som', 'farc', 'aqu', 'ceremony', '.']


### Lemmatization
The WordNet lemmatizer only removes affixes if the resulting word is in its dictionary. This additional checking process makes the lemmatizer slower than the above stemmers.


```python
print(tokens)
```

    ['DENNIS', ':', 'Listen', ',', 'strange', 'women', 'lying', 'in', 'ponds', 'distributing', 'swords', 'is', 'no', 'basis', 'for', 'a', 'system', 'of', 'government', '.', 'Supreme', 'executive', 'power', 'derives', 'from', 'a', 'mandate', 'from', 'the', 'masses', ',', 'not', 'from', 'some', 'farcical', 'aquatic', 'ceremony', '.']



```python
wnl = nltk.WordNetLemmatizer()
print([wnl.lemmatize(t) for t in tokens])
```

    ['DENNIS', ':', 'Listen', ',', 'strange', 'woman', 'lying', 'in', 'pond', 'distributing', 'sword', 'is', 'no', 'basis', 'for', 'a', 'system', 'of', 'government', '.', 'Supreme', 'executive', 'power', 'derives', 'from', 'a', 'mandate', 'from', 'the', 'mass', ',', 'not', 'from', 'some', 'farcical', 'aquatic', 'ceremony', '.']


Notice that it doesn't handle lying, but it converts women to woman.

The WordNet lemmatizer is a good choice if you want to compile the vocabulary of some texts and want a list of valid lemmas.

## 4.2 Tokenizing Text
Tokenization is an instance of a more general problem of segmentation.

### Tokenizing Sentences and Words


```python
from nltk.tokenize import sent_tokenize, word_tokenize
example = '''Good muffins cost $3.88\nin New York.  Please buy me two of them.\n\nThanks.'''
```


```python
sent_tokenize(example)
```




    ['Good muffins cost $3.88\nin New York.',
     'Please buy me two of them.',
     'Thanks.']




```python
[word_tokenize(sentence) for sentence in sent_tokenize(example)]
```




    [['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York', '.'],
     ['Please', 'buy', 'me', 'two', 'of', 'them', '.'],
     ['Thanks', '.']]



The sent_tokenize() uses a pre-trained model from nltk_data/tokenizers/**punkt**/english.pickle. You can also specify other languages, the list of available languages with pre-trained models in NLTK are:


```python
import os
[pickle for pickle in os.listdir('/Users/Shih-Hsiao/nltk_data/tokenizers/punkt') if 'pickle' in pickle]
```




    ['czech.pickle',
     'danish.pickle',
     'dutch.pickle',
     'english.pickle',
     'estonian.pickle',
     'finnish.pickle',
     'french.pickle',
     'german.pickle',
     'greek.pickle',
     'italian.pickle',
     'norwegian.pickle',
     'polish.pickle',
     'portuguese.pickle',
     'slovene.pickle',
     'spanish.pickle',
     'swedish.pickle',
     'turkish.pickle']



### PunktSentenceTokenizer
PunktSentenceTokenizer is the abstract class for **the default sentence tokenizer**, i.e. sent_tokenize(), provided in NLTK. It is an implmentation of Unsupervised Multilingual Sentence Boundary Detection (Kiss and Strunk (2005). 


```python
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
tokenized = custom_sent_tokenizer.tokenize(sample_text)
```


```python
sample_text[150:432]
```




    'Mr. Speaker, Vice President Cheney, members of Congress, members of the Supreme Court and diplomatic corps, distinguished guests, and fellow citizens: Today our nation lost a beloved, graceful, courageous woman who called America to its founding ideals and carried on a noble dream.'




```python
tokenized[:5]
```




    ["PRESIDENT GEORGE W. BUSH'S ADDRESS BEFORE A JOINT SESSION OF THE CONGRESS ON THE STATE OF THE UNION\n \nJanuary 31, 2006\n\nTHE PRESIDENT: Thank you all.",
     'Mr. Speaker, Vice President Cheney, members of Congress, members of the Supreme Court and diplomatic corps, distinguished guests, and fellow citizens: Today our nation lost a beloved, graceful, courageous woman who called America to its founding ideals and carried on a noble dream.',
     'Tonight we are comforted by the hope of a glad reunion with the husband who was taken so long ago, and we are grateful for the good life of Coretta Scott King.',
     '(Applause.)',
     'President George W. Bush reacts to applause during his State of the Union Address at the Capitol, Tuesday, Jan.']



### TweetTokenizer


```python
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer()
example = "@remy: This is a cooool #dummysmiley: :-) :-P <3 and some arrows < > -> <--"
print(tknzr.tokenize(example))
print(word_tokenize(example))
```

    ['@remy', ':', 'This', 'is', 'a', 'cooool', '#dummysmiley', ':', ':-)', ':-P', '<3', 'and', 'some', 'arrows', '<', '>', '->', '<--']
    ['@', 'remy', ':', 'This', 'is', 'a', 'cooool', '#', 'dummysmiley', ':', ':', '-', ')', ':', '-P', '<', '3', 'and', 'some', 'arrows', '<', '>', '-', '>', '<', '--']



```python
# using strip_handles and reduce_len parameters:
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
example = '@remy: This is waaaaayyyy too much for you!!!!!!'
print(tknzr.tokenize(example))
```

    [':', 'This', 'is', 'waaayyy', 'too', 'much', 'for', 'you', '!', '!', '!']


### nltk.corpus.reader.twitter module


```python
tweets_tokens = twitter_samples.tokenized('negative_tweets.json')
```


```python
tweets_tokens[0]
```




    ['hopeless', 'for', 'tmr', ':(']



# 5. Categorizing and Tagging Words
A part-of-speech tagger, or POS-tagger, processes a sequence of words, and attaches a part of speech tag to each word.
## 5.1 Using a Tagger

### POS tag list:
CC	coordinating conjunction<br/>
CD	cardinal digit<br/>
DT	determiner<br/>
EX	existential there (like: "there is" ... think of it like "there exists")<br/>
FW	foreign word<br/>
IN	preposition/subordinating conjunction<br/>
JJ	adjective	'big'<br/>
JJR	adjective, comparative	'bigger'<br/>
JJS	adjective, superlative	'biggest'<br/>
LS	list marker	1)<br/>
MD	modal	could, will<br/>
NN	noun, singular 'desk'<br/>
NNS	noun plural	'desks'<br/>
NNP	proper noun, singular	'Harrison'<br/>
NNPS	proper noun, plural	'Americans'<br/>
PDT	predeterminer	'all the kids'<br/>
POS	possessive ending	parent's<br/>
PRP	personal pronoun	I, he, she<br/>
PRP\$	possessive pronoun	my, his, hers<br/>
RB	adverb	very, silently,<br/>
RBR	adverb, comparative	better<br/>
RBS	adverb, superlative	best<br/>
RP	particle	give up<br/>
TO	to	go 'to' the store.<br/>
UH	interjection	errrrrrrrm<br/>
VB	verb, base form	take<br/>
VBD	verb, past tense	took<br/>
VBG	verb, gerund/present participle	taking<br/>
VBN	verb, past participle	taken<br/>
VBP	verb, sing. present, non-3d	take<br/>
VBZ	verb, 3rd person sing. present	takes<br/>
WDT	wh-determiner	which<br/>
WP	wh-pronoun	who, what<br/>
WP$	possessive wh-pronoun	whose<br/>
WRB	wh-abverb	where, when<br/>


```python
import nltk
text = word_tokenize("They refuse to permit us to obtain the refuse permit")
nltk.pos_tag(text)
```




    [('They', 'PRP'),
     ('refuse', 'VBP'),
     ('to', 'TO'),
     ('permit', 'VB'),
     ('us', 'PRP'),
     ('to', 'TO'),
     ('obtain', 'VB'),
     ('the', 'DT'),
     ('refuse', 'NN'),
     ('permit', 'NN')]



### Similar Words
The text.similar() method takes a word w, finds all contexts w1w w2, then finds all words w' that appear in the same context, i.e. w1w'w2.


```python
text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
```


```python
text.similar('woman')
```

    man time day year car moment world house family child country boy
    state job place way war girl work word



```python
text.similar('bought')
```

    made said done put had seen found given left heard was been brought
    set got that took in told felt



```python
text.similar('over')
```

    in on to of and for with from at by that into as up out down through
    is all about



```python
text.similar('the')
```

    a his this their its her an that our any all one these my in your no
    some other and


### Reading Tagged Corpora

NLTK's corpus readers provide a uniform interface so that you don't have to be concerned with the different file formats. **Not all corpora employ the same set of tags.** Initially we want to avoid the complications of these tagsets, so we use a built-in mapping to the **"Universal Tagset"**:


```python
nltk.corpus.brown.tagged_words()
```




    [('The', 'AT'), ('Fulton', 'NP-TL'), ...]




```python
nltk.corpus.brown.tagged_words(tagset='universal')
```




    [('The', 'DET'), ('Fulton', 'NOUN'), ...]



## 5.2 The Default Tagger

Let's find out which tag is most likely (now using the unsimplified tagset):


```python
tags = [tag for (word, tag) in brown.tagged_words(categories='news')]
nltk.FreqDist(tags).max()
```




    'NN'



We can also create a tagger that tags everything as NN.


```python
raw = 'I do not like green eggs and ham, I do not like them Sam I am!'
tokens = word_tokenize(raw)
default_tagger = nltk.DefaultTagger('NN')
print(default_tagger.tag(tokens))
```

    [('I', 'NN'), ('do', 'NN'), ('not', 'NN'), ('like', 'NN'), ('green', 'NN'), ('eggs', 'NN'), ('and', 'NN'), ('ham', 'NN'), (',', 'NN'), ('I', 'NN'), ('do', 'NN'), ('not', 'NN'), ('like', 'NN'), ('them', 'NN'), ('Sam', 'NN'), ('I', 'NN'), ('am', 'NN'), ('!', 'NN')]


### Evaluation

We evaluate the performance of a tagger relative to the tags a human expert would assign. Since we don't usually have access to an expert and impartial human judge, we make do instead with **gold standard test data**. This is a corpus which has been manually annotated and which is accepted as a standard against which the guesses of an automatic system are assessed. The tagger is regarded as being correct if the tag it guesses for a given word is the same as the gold standard tag.


```python
default_tagger.evaluate(brown_tagged_sents)
```




    0.13089484257215028



Unsurprisingly, this method performs rather poorly. On a typical corpus, it will tag only about an eighth of the tokens correctly, as we see below:

## 5.3 N-Gram Tagging

Slide Type
A 1-gram tagger is another term for a unigram tagger: i.e., the context used to tag a token is just the text of the token itself. 2-gram taggers are also called bigram taggers, and 3-gram taggers are called trigram taggers.

<img style="width: 800px;" src="http://www.nltk.org/images/tag-context.png">

### Unigram Tagging

Unigram taggers are based on **a simple statistical algorithm**: for each token, assign the tag that is most likely for that particular token. 

For example, it will assign the tag JJ to any occurrence of the word frequent, since frequent is used as an adjective (e.g. a frequent word) more often than it is used as a verb (e.g. I frequent this cafe). 


```python
from nltk.corpus import brown
brown_tagged_sents = brown.tagged_sents(categories='news')
brown_sents = brown.sents(categories='news')

unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
print(unigram_tagger.tag(brown_sents[2007]))
```

    [('Various', 'JJ'), ('of', 'IN'), ('the', 'AT'), ('apartments', 'NNS'), ('are', 'BER'), ('of', 'IN'), ('the', 'AT'), ('terrace', 'NN'), ('type', 'NN'), (',', ','), ('being', 'BEG'), ('on', 'IN'), ('the', 'AT'), ('ground', 'NN'), ('floor', 'NN'), ('so', 'QL'), ('that', 'CS'), ('entrance', 'NN'), ('is', 'BEZ'), ('direct', 'JJ'), ('.', '.')]



```python
unigram_tagger.evaluate(brown_tagged_sents)
```




    0.9349006503968017




```python
size = int(len(brown_tagged_sents) * 0.9)
size
```




    4160




```python
train_sents = brown_tagged_sents[:size]
test_sents = brown_tagged_sents[size:]
unigram_tagger = nltk.UnigramTagger(train_sents)
unigram_tagger.evaluate(test_sents)
```




    0.8121200039868434



### Bigram Tagging


```python
bigram_tagger = nltk.BigramTagger(train_sents)
bigram_tagger.tag(brown_sents[2007])
```




    [('Various', 'JJ'),
     ('of', 'IN'),
     ('the', 'AT'),
     ('apartments', 'NNS'),
     ('are', 'BER'),
     ('of', 'IN'),
     ('the', 'AT'),
     ('terrace', 'NN'),
     ('type', 'NN'),
     (',', ','),
     ('being', 'BEG'),
     ('on', 'IN'),
     ('the', 'AT'),
     ('ground', 'NN'),
     ('floor', 'NN'),
     ('so', 'CS'),
     ('that', 'CS'),
     ('entrance', 'NN'),
     ('is', 'BEZ'),
     ('direct', 'JJ'),
     ('.', '.')]




```python
unseen_sent = brown_sents[4203]
bigram_tagger.tag(unseen_sent)
```




    [('The', 'AT'),
     ('population', 'NN'),
     ('of', 'IN'),
     ('the', 'AT'),
     ('Congo', 'NP'),
     ('is', 'BEZ'),
     ('13.5', None),
     ('million', None),
     (',', None),
     ('divided', None),
     ('into', None),
     ('at', None),
     ('least', None),
     ('seven', None),
     ('major', None),
     ('``', None),
     ('culture', None),
     ('clusters', None),
     ("''", None),
     ('and', None),
     ('innumerable', None),
     ('tribes', None),
     ('speaking', None),
     ('400', None),
     ('separate', None),
     ('dialects', None),
     ('.', None)]




```python
bigram_tagger.evaluate(test_sents)
```




    0.10206319146815508



## 5.4 Combining Taggers

For example, we could combine the results of a bigram tagger, a unigram tagger, and a default tagger, as follows:

Try tagging the token with the bigram tagger.
If the bigram tagger is unable to find a tag for the token, try the unigram tagger.
If the unigram tagger is also unable to find a tag, use a default tagger.



```python
bigram_tagger = nltk.BigramTagger(train_sents)

t0 = nltk.DefaultTagger('NN')
t1 = nltk.UnigramTagger(train_sents, backoff=t0)
t2 = nltk.BigramTagger(train_sents, backoff=t1)
t2.evaluate(test_sents)
```




    0.8452108043456593



# 6. Learning to Classify Text

## Supervised Classification

A classifier is called supervised if it is built based on training corpora containing the correct label for each input.

<img style="width: 600px;" src="http://www.nltk.org/images/supervised-classification.png">


## 6.1 Gender Identification
Names ending in a, e and i are likely to be female, while names ending in k, o, r, s and t are likely to be male.


```python
from nltk.corpus import names
labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
                 [(name, 'female') for name in names.words('female.txt')])
import random
random.shuffle(labeled_names)

def gender_features(word):
    return {'last_letter': word[-1]}

# Choosing The Right Features
def gender_features2(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features
```


```python
gender_features2('John')
```




    {'count(a)': 0,
     'count(b)': 0,
     'count(c)': 0,
     'count(d)': 0,
     'count(e)': 0,
     'count(f)': 0,
     'count(g)': 0,
     'count(h)': 1,
     'count(i)': 0,
     'count(j)': 1,
     'count(k)': 0,
     'count(l)': 0,
     'count(m)': 0,
     'count(n)': 1,
     'count(o)': 1,
     'count(p)': 0,
     'count(q)': 0,
     'count(r)': 0,
     'count(s)': 0,
     'count(t)': 0,
     'count(u)': 0,
     'count(v)': 0,
     'count(w)': 0,
     'count(x)': 0,
     'count(y)': 0,
     'count(z)': 0,
     'first_letter': 'j',
     'has(a)': False,
     'has(b)': False,
     'has(c)': False,
     'has(d)': False,
     'has(e)': False,
     'has(f)': False,
     'has(g)': False,
     'has(h)': True,
     'has(i)': False,
     'has(j)': True,
     'has(k)': False,
     'has(l)': False,
     'has(m)': False,
     'has(n)': True,
     'has(o)': True,
     'has(p)': False,
     'has(q)': False,
     'has(r)': False,
     'has(s)': False,
     'has(t)': False,
     'has(u)': False,
     'has(v)': False,
     'has(w)': False,
     'has(x)': False,
     'has(y)': False,
     'has(z)': False,
     'last_letter': 'n'}



### Naive Bayes Classifier and Error Analysis


```python
train_names = labeled_names[1500:]
devtest_names = labeled_names[500:1500]
test_names = labeled_names[:500]

train_set = [(gender_features(n), gender) for (n, gender) in train_names]
devtest_set = [(gender_features(n), gender) for (n, gender) in devtest_names]
test_set = [(gender_features(n), gender) for (n, gender) in test_names]

# Naive Bayes Classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, devtest_set))
```

    0.751


Once an initial set of features has been chosen, a very productive method for refining the feature set is error analysis. The training set is used to train the model, and the dev-test set is used to perform error analysis. The test set serves in our final evaluation of the system.

<img style="width: 400px;" src="http://www.nltk.org/images/corpus-org.png">


```python
errors = []
for (name, tag) in devtest_names:
    guess = classifier.classify(gender_features(name))
    if guess != tag:
        errors.append( (tag, guess, name) )

for (tag, guess, name) in sorted(errors)[:30]: # Here only show the first 30 result
    print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))
```

    correct=female   guess=pos      name=Abbey                         
    correct=female   guess=pos      name=Acacia                        
    correct=female   guess=pos      name=Adore                         
    correct=female   guess=pos      name=Ag                            
    correct=female   guess=pos      name=Agace                         
    correct=female   guess=pos      name=Aileen                        
    correct=female   guess=pos      name=Ailina                        
    correct=female   guess=pos      name=Ainslie                       
    correct=female   guess=pos      name=Alanna                        
    correct=female   guess=pos      name=Alayne                        
    correct=female   guess=pos      name=Albina                        
    correct=female   guess=pos      name=Alexi                         
    correct=female   guess=pos      name=Alfie                         
    correct=female   guess=pos      name=Alica                         
    correct=female   guess=pos      name=Allene                        
    correct=female   guess=pos      name=Allyce                        
    correct=female   guess=pos      name=Almeta                        
    correct=female   guess=pos      name=Aloisia                       
    correct=female   guess=pos      name=Aloysia                       
    correct=female   guess=pos      name=Alvinia                       
    correct=female   guess=pos      name=Alyda                         
    correct=female   guess=pos      name=Alyse                         
    correct=female   guess=pos      name=Amaleta                       
    correct=female   guess=pos      name=Amargo                        
    correct=female   guess=pos      name=Amity                         
    correct=female   guess=pos      name=Andy                          
    correct=female   guess=pos      name=Anette                        
    correct=female   guess=pos      name=Angelique                     
    correct=female   guess=pos      name=Angelle                       
    correct=female   guess=pos      name=Angil                         


For example, names ending in **yn** appear to be predominantly female, despite the fact that names ending in **n** tend to be male; and names ending in **ch** are usually male, even though names that end in **h** tend to be female. 

We therefore adjust our feature extractor to include features for two-letter suffixes:


```python
def gender_features(word):
    return {'suffix1': word[-1:], 'suffix2': word[-2:]}

train_set = [(gender_features(n), gender) for (n, gender) in train_names]
devtest_set = [(gender_features(n), gender) for (n, gender) in devtest_names]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, devtest_set))
```

    0.773


## 6.2 Document Classification

we saw several examples of corpora where documents have been labeled with categories. Using these corpora, we can build classifiers that will automatically tag new documents with appropriate category labels.


```python
from nltk.corpus import movie_reviews
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features[word] = (word in document_words) # contains word or not
    return features
```


```python
print(str(document_features(movie_reviews.words('pos/cv957_8737.txt'))) [:1000],', ...}')
```

    {'plot': True, ':': True, 'two': True, 'teen': False, 'couples': False, 'go': False, 'to': True, 'a': True, 'church': False, 'party': False, ',': True, 'drink': False, 'and': True, 'then': True, 'drive': False, '.': True, 'they': True, 'get': True, 'into': True, 'an': True, 'accident': False, 'one': True, 'of': True, 'the': True, 'guys': False, 'dies': False, 'but': True, 'his': True, 'girlfriend': True, 'continues': False, 'see': False, 'him': True, 'in': True, 'her': False, 'life': False, 'has': True, 'nightmares': False, 'what': True, "'": True, 's': True, 'deal': False, '?': False, 'watch': True, 'movie': True, '"': True, 'sorta': False, 'find': False, 'out': True, 'critique': False, 'mind': False, '-': True, 'fuck': False, 'for': True, 'generation': False, 'that': True, 'touches': False, 'on': True, 'very': True, 'cool': False, 'idea': True, 'presents': False, 'it': True, 'bad': False, 'package': False, 'which': True, 'is': True, 'makes': False, 'this': True, 'review': False, 'eve , ...}



```python
featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5)
```

    0.77
    Most Informative Features
                  schumacher = True              neg : pos    =     12.5 : 1.0
                      justin = True              neg : pos    =      9.8 : 1.0
               unimaginative = True              neg : pos    =      7.8 : 1.0
                      welles = True              neg : pos    =      7.8 : 1.0
                        mena = True              neg : pos    =      7.1 : 1.0


Apparently in this corpus, a review that mentions **"Justin"** is almost 10 times more likely to be negative than positive, while a review that mentions **"Mena"** is about 7 times more likely to be negative.

# 7. Extracting Information from Text

## 7.1 Information Extraction Architecture

<img style="width: 800px;" src="http://www.nltk.org/images/ie-architecture.png">


Simple Pipeline Architecture for an Information Extraction System. This system takes the raw text of a document as its input, and generates a list of (entity, relation, entity) tuples as its output. For example, given a document that indicates that the company Georgia-Pacific is located in Atlanta, it might generate the tuple ([ORG: 'Georgia-Pacific'] 'in' [LOC: 'Atlanta']).


## 7.2 Chunking

The basic technique we will use for entity detection is chunking, which segments and labels multi-token sequences as illustrated in the following figure.

<img style="width: 800px;" src="http://www.nltk.org/images/chunk-segmentation.png">


```python
import nltk
grammar = r"""                # Regular Expressions
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
      {<NNP>+}                # chunk sequences of proper nouns
"""

cp = nltk.RegexpParser(grammar)
sentence = [("Rapunzel", "NNP"), ("let", "VBD"), ("down", "RP"),
                 ("her", "PP$"), ("long", "JJ"), ("golden", "JJ"), ("hair", "NN")]

print(cp.parse(sentence))
```

    (S
      (NP Rapunzel/NNP)
      let/VBD
      down/RP
      (NP her/PP$ long/JJ golden/JJ hair/NN))


## 7.3 Chinking

Sometimes it is easier to define what we want to exclude from a chunk. We can define a chink to be a sequence of tokens that is not included in a chunk. 


```python
grammar = r"""       # Regular Expressions
  NP:
    {<.*>+}          # Chunk everything
    }<VBD|IN>+{      # Chink sequences of VBD and IN
  """

sentence = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"),
       ("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN")]
cp = nltk.RegexpParser(grammar)
print(cp.parse(sentence))
```

    (S
      (NP the/DT little/JJ yellow/JJ dog/NN)
      barked/VBD
      at/IN
      (NP the/DT cat/NN))


## 7.4 Named Entity Recognition

NLTK provides a classifier that has already been trained to recognize named entities, accessed with the function nltk.ne_chunk(). If we set the parameter binary=True, then named entities are just tagged as NE; **otherwise, the classifier adds category labels such as PERSON, ORGANIZATION, and GPE.**

### NE Type and Examples
ORGANIZATION - Georgia-Pacific Corp., WHO <br/>
PERSON - Eddy Bonte, President Obama <br/>
LOCATION - Murray River, Mount Everest <br/>
DATE - June, 2008-06-29 <br/>
TIME - two fifty a m, 1:30 p.m. <br/>
MONEY - 175 million Canadian Dollars, GBP 10.40 <br/>
PERCENT - twenty pct, 18.75 % <br/>
FACILITY - Washington Monument, Stonehenge <br/>
GPE - South East Asia, Midlothian <br/>


```python
sent = nltk.corpus.treebank.tagged_sents()[22]
print(nltk.ne_chunk(sent, binary=False))
```

    (S
      The/DT
      (GPE U.S./NNP)
      is/VBZ
      one/CD
      of/IN
      the/DT
      few/JJ
      industrialized/VBN
      nations/NNS
      that/WDT
      *T*-7/-NONE-
      does/VBZ
      n't/RB
      have/VB
      a/DT
      higher/JJR
      standard/NN
      of/IN
      regulation/NN
      for/IN
      the/DT
      smooth/JJ
      ,/,
      needle-like/JJ
      fibers/NNS
      such/JJ
      as/IN
      crocidolite/NN
      that/WDT
      *T*-1/-NONE-
      are/VBP
      classified/VBN
      *-5/-NONE-
      as/IN
      amphobiles/NNS
      ,/,
      according/VBG
      to/TO
      (PERSON Brooke/NNP T./NNP Mossman/NNP)
      ,/,
      a/DT
      professor/NN
      of/IN
      pathlogy/NN
      at/IN
      the/DT
      (ORGANIZATION University/NNP)
      of/IN
      (PERSON Vermont/NNP College/NNP)
      of/IN
      (GPE Medicine/NNP)
      ./.)


# The Other Issues in NLTK
* Analyzing Sentence Structure
* Building Feature Based Grammars
* Analyzing the Meaning of Sentences (minor fixes still required)
* Managing Linguistic Data (minor fixes still required)

**A Simple Grammar**

Let's start off by looking at a simple context-free grammar. By convention, the left-hand-side of the first production is the start-symbol of the grammar, typically S, and all well-formed trees must have this symbol as their root label. In NLTK, context-free grammars are defined in the nltk.grammar module.


```python
grammar1 = nltk.CFG.fromstring("""
  S -> NP VP
  VP -> V NP | V NP PP
  PP -> P NP
  V -> "saw" | "ate" | "walked"
  NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
  Det -> "a" | "an" | "the" | "my"
  N -> "man" | "dog" | "cat" | "telescope" | "park"
  P -> "in" | "on" | "by" | "with"
  """)

sent = "Mary saw Bob".split()
rd_parser = nltk.RecursiveDescentParser(grammar1)
for tree in rd_parser.parse(sent):
    print(tree)
```

    (S (NP Mary) (VP (V saw) (NP Bob)))


# 8. Scikit-Learn Sklearn with NLTK

The best module for Python to do classification with is the Scikit-learn (sklearn) module, a free machine learning library features various classification, regression and clustering algorithms.

### Installing Scikit-Learn Module

    pip install -U scikit-learn
    
Luckily for us, the people behind NLTK forsaw the value of incorporating the sklearn module into the NLTK classifier methodology. As such, they created the SklearnClassifier API of sorts. To use that, you just need to import it like:


```python
from nltk.classify.scikitlearn import SklearnClassifier
```

From here, you can use just about any of the sklearn classifiers.


```python
from sklearn.naive_bayes import MultinomialNB,BernoulliNB # more variations of the Naive Bayes algorithm
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

# MNB_classifier = SklearnClassifier(MultinomialNB())
# BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
# LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
# SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
# SVC_classifier = SklearnClassifier(SVC())
# LinearSVC_classifier = SklearnClassifier(LinearSVC())
# NuSVC_classifier = SklearnClassifier(NuSVC())
```

# 9. Sentiment Analysis with NLTK
## 9.1 Text Classification


```python
import codecs
import string

with codecs.open('short_reviews/positive.txt', 'r', 'utf-8', errors='ignore') as f:
    short_pos = f.read()
    
with codecs.open('short_reviews/negative.txt', 'r', 'utf-8', errors='ignore') as f:
    short_neg = f.read()

documents = []

for r in short_pos.split('\n'):
    documents.append( (r, "pos") )

for r in short_neg.split('\n'):
    documents.append( (r, "neg") )


all_words = []

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

for w in short_pos_words:
    all_words.append(w.lower())

for w in short_neg_words:
    all_words.append(w.lower())
    
# remove stop words
stops_punc = set(stopwords.words("english")) | set(string.punctuation)
all_words = [word for word in all_words if word not in stops_punc]

all_words = nltk.FreqDist(all_words)

# take the 5000 most common words 
most5000 = all_words.most_common()[:5000]
word_features = [most5000[key][0] for key in range(5000)]
```


```python
print(all_words.most_common(15))
```

    [("'s", 3537), ('film', 1589), ('movie', 1336), ("n't", 940), ('one', 739), ('like', 720), ('--', 670), ('``', 655), ('story', 493), ('much', 386), ('even', 382), ('good', 377), ('comedy', 356), ('time', 341), ('characters', 330)]



```python
print(all_words["stupid"])
```

    30


### 9.2 Converting words to Features


```python
def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

# a tuple contains feature list and category 
featuresets = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featuresets)
```


```python
print(str(featuresets[0])[:1000], ', ...})')
```

    ({"'s": False, 'film': False, 'movie': False, "n't": False, 'one': False, 'like': False, '--': False, '``': False, 'story': False, 'much': False, 'even': False, 'good': False, 'comedy': True, 'time': False, 'characters': False, 'little': False, 'way': False, 'funny': False, 'make': False, 'enough': False, 'never': False, 'director': False, 'makes': False, 'would': False, 'may': False, 'us': False, 'work': False, 'best': False, 'bad': False, 'life': False, 'love': False, 'could': False, 'movies': False, 'new': False, 'well': False, 'something': False, 'really': False, 'made': False, 'performances': False, 'plot': False, 'many': False, 'drama': False, 'films': False, 'still': False, 'see': False, 'look': False, 'every': False, 'two': False, 'people': False, 'nothing': False, "'re": False, 'better': False, 'long': False, 'without': False, 'fun': False, 'get': False, 'action': False, 'great': False, 'though': False, 'might': False, 'big': False, 'also': False, 'character': False, 'audience , ...})



```python
len(featuresets)
```




    10664




```python
training_set = featuresets[:10000]
testing_set =  featuresets[10000:]
```

## 9.3 Creating classifiers
NOTE: Training classifiers and machine learning algorithms can take a very long time!


```python
classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)

# Sklearn Classifiers
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MultinomialNB accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)
```

    Original Naive Bayes Algo accuracy percent: 77.10843373493977
    MultinomialNB accuracy percent: 76.6566265060241
    BernoulliNB accuracy percent: 77.2590361445783
    LogisticRegression_classifier accuracy percent: 74.84939759036145
    SGDClassifier_classifier accuracy percent: 72.43975903614458
    SVC_classifier accuracy percent: 48.94578313253012
    LinearSVC_classifier accuracy percent: 71.98795180722891
    NuSVC_classifier accuracy percent: 73.79518072289156


## 9.4 Combining Algorithms with NLTK
We may find it difficult to choose just one classifier. The good news is, you don't have to! Combining classifier algorithms is is a common technique, done by creating a sort of voting system, where each algorithm gets one vote, and the classification that has the votes votes is the chosen one.


```python
from nltk.classify import ClassifierI

# for choosing the most popular vote.
from statistics import mode
```

we want our new classifier to act like a typical NLTK classifier, with all of the methods. Simple enough, using object oriented programming, we can just be sure to inherit from the NLTK classifier class.


```python
# class inheriting from NLTK's ClassifierI
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    # algorithms voting
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        # returning the most popular vote
        return mode(votes)
    
    # tally the votes for and against the winning vote
    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
```

For example, 3/5 votes for positive is weaker than 5/5 votes. As such, we can literally return the ratio of votes as a sort of confidence indicator.


```python
voted_classifier = VoteClassifier(classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier,
                                  SGDClassifier_classifier,
#                                   SVC_classifier,
                                  LinearSVC_classifier,
                                  NuSVC_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)

print("Classification:", voted_classifier.classify(testing_set[0][0]), "Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
print("Classification:", voted_classifier.classify(testing_set[1][0]), "Confidence %:",voted_classifier.confidence(testing_set[1][0])*100)
print("Classification:", voted_classifier.classify(testing_set[2][0]), "Confidence %:",voted_classifier.confidence(testing_set[2][0])*100)
print("Classification:", voted_classifier.classify(testing_set[3][0]), "Confidence %:",voted_classifier.confidence(testing_set[3][0])*100)
print("Classification:", voted_classifier.classify(testing_set[4][0]), "Confidence %:",voted_classifier.confidence(testing_set[4][0])*100)
print("Classification:", voted_classifier.classify(testing_set[5][0]), "Confidence %:",voted_classifier.confidence(testing_set[5][0])*100)
```

    voted_classifier accuracy percent: 75.75301204819277
    Classification: neg Confidence %: 100.0
    Classification: neg Confidence %: 100.0
    Classification: neg Confidence %: 100.0
    Classification: neg Confidence %: 100.0
    Classification: neg Confidence %: 100.0
    Classification: neg Confidence %: 100.0


# 10. Saving Classifiers with NLTK (Python object serialization)
The pickle module implements binary protocols for serializing and de-serializing a Python object structure. “Pickling” is the process whereby a Python object hierarchy is converted into a byte stream, and “unpickling” is the inverse operation, whereby a byte stream (from a binary file or bytes-like object) is converted back into an object hierarchy. Pickling (and unpickling) is alternatively known as “serialization”, “marshalling,” or “flattening”; however, to avoid confusion, the terms used here are “pickling” and “unpickling”.

### Pickling classifier


```python
import pickle

save_classifier = open("pickled_algos/originalnaivebayes5k.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

save_classifier = open("pickled_algos/MNB_classifier5k.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

save_classifier = open("pickled_algos/BernoulliNB_classifier5k.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

save_classifier = open("pickled_algos/LogisticRegression_classifier5k.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

save_classifier = open("pickled_algos/LinearSVC_classifier5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

save_classifier = open("pickled_algos/SGDC_classifier5k.pickle","wb")
pickle.dump(SGDClassifier_classifier, save_classifier)
save_classifier.close()
```

### Pickling other data


```python
save_documents = open("pickled_algos/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

save_word_features = open("pickled_algos/word_features5k.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

save_word_features = open("pickled_algos/featuresets.pickle","wb")
pickle.dump(featuresets, save_word_features)
save_word_features.close()
```

### Unpickling .pickle files


```python
documents_f = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()

word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

featuresets_f = open("pickled_algos/featuresets.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()

open_file = open("pickled_algos/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/BernoulliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/LogisticRegression_classifier5k.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/LinearSVC_classifier5k.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/SGDC_classifier5k.pickle", "rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()
```

# References
NLTK 3.2.4 documentation <br />
http://www.nltk.org/

PythonProgramming.net > Data Analysis > Natural Language Processing <br />
https://pythonprogramming.net/tokenizing-words-sentences-nltk-tutorial/
 
How To Work with Language Data in Python 3 using the Natural Language Toolkit (NLTK) <br />
https://www.digitalocean.com/community/tutorials/how-to-work-with-language-data-in-python-3-using-the-natural-language-toolkit-nltk

Use of PunktSentenceTokenizer in NLTK <br />
https://stackoverflow.com/questions/35275001/use-of-punktsentencetokenizer-in-nltk

## Free Books
##### 《Python 3 Text Processing with NLTK 3 Cookbook》
http://pdf.th7.cn/down/files/1502/Python%203%20Text%20Processing%20with%20NLTK%203%20Cookbook.pdf

##### 《Natural Language Processing with Python》- The first edition
http://victoria.lviv.ua/html/fl5/NaturalLanguageProcessingWithPython.pdf <br />
(Written by the creators of NLTK, it guides the reader through the fundamentals of writing Python programs, working with corpora, categorizing text, analyzing linguistic structure, and more.) <br />
* for Python 3 and NLTK 3: http://www.nltk.org/book/


## Other Related Issuse
Graphing Live Twitter Sentiment Analysis with NLTK with NLTK <br />
https://youtu.be/ojDHK1SmCHA?t=5m48s

结巴分词和NLTK----一套中文文本分析的组合拳 <br />
http://www.jianshu.com/p/aea87adee163
