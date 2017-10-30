from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import nltk
import string ,re
def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None

def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None

def sentence_similarity ( sentence1 , sentence2 ):
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = 0
        for ss in synsets2:
            if synset.path_similarity ( ss ) is not None :
                if synset.path_similarity ( ss ) > best_score :
                    best_score = synset.path_similarity ( ss )
        # Check that the similarity could have been computed
        if best_score > 0 :
            score += best_score
            count += 1

    # Average the values
    if count > 1 :
       score /= count
    return score

def symmetric_sentence_similarity(sentence1, sentence2):
    """ compute the symmetric sentence similarity using Wordnet """
    return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) / 2
def return_answer ( data , question ) :

    MAX = 0
    MAX1 = 0
    st = ''
    str1 = ''
    for sentence in data :
        if symmetric_sentence_similarity ( sentence , question ) >= 0.55  :
           if symmetric_sentence_similarity ( sentence , question ) > MAX :
               MAX = symmetric_sentence_similarity ( sentence , question )
               st = sentence
           elif symmetric_sentence_similarity ( sentence , question ) > MAX1 :
               MAX1 = symmetric_sentence_similarity ( sentence , question )
               str1 = sentence
    st = st + '\n' + str1
    st = re.sub (r'([^\s\w]|_)+', '', st )
    if MAX < 0.55 :
        st = "The answer can not be deduced from the context ! Try another question "
    return st
