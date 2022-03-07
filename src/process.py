import string

from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity


# function to find corresponding pos tag
def get_wordnet_pos(tag):
    # map nltk pos tags (default penn dataset) to the format wordnet lemmatizer accepts
    if tag.startswith('N'):
        wordnet_tag = wordnet.NOUN # value is n
    elif tag.startswith('V'):
        wordnet_tag = wordnet.VERB # value is v
    elif tag.startswith('J'):
        wordnet_tag = wordnet.ADJ # value is a not j
    elif tag.startswith('R'):
        wordnet_tag = wordnet.ADV # value is r
    else:
        # this will be a noun by default, and easier for error handling
        wordnet_tag = wordnet.NOUN

    return wordnet_tag


# function for language pre processing (tokenizing, lemmatizing etc)
# removes stopwords only for cases when needed, returns a processed string
def pre_process(query, sw):
    # convert query to lowercase and remove punctuation
    query = query.translate(str.maketrans('', '', string.punctuation)).lower()

    # tokenize query
    token_list = word_tokenize(query)

    if (sw):
        # create a stopword set from the standard stopwords available in nltk
        stop_words = set(stopwords.words('english'))
        # remove stopwords from token list
        token_list = [token for token in token_list if token not in stop_words]

    # pos tag processes a sequence of words/tokens
    # attaches a part of speech (pos) tag to each word 
    # returns a list of tuples as (token, tag)
    token_list_tagged = pos_tag(token_list)

    # initialize the Wordnet Lemmatizer
    lemmatizer = WordNetLemmatizer()
    # get wordnet pos will get the corresponding wordnet pos tag for the default pos tag
    # lemmatize list of tokens and join into a string
    lemmatized_list = [lemmatizer.lemmatize(token, get_wordnet_pos(tag)) for token, tag in token_list_tagged]
    lemmatized_string = " ".join(lemmatized_list)
    
    return lemmatized_string


# function to calculate cosine similarity and return a dictionary of max value with all the indexes they occur
def similarity_find(tfidf_matrix_query, tfidf_matrix_dataset):
    # create dictionary to store information
    cosine = {}

    # perform cosine similarity on the vectorized query and qa dataset
    cosine_matrix = cosine_similarity(tfidf_matrix_query, tfidf_matrix_dataset)[0]
    # flatten matrix to one dimensional vector
    cosine_flat = cosine_matrix.flatten()
    # find the maximum cosine value in the cosine similarity vector
    cosine['similarity_max'] = max(cosine_flat)
    # use list comprehension to iterate through the vector, finding all indexes of the max value
    # used to account for multiple maximum cosine similarity matches
    cosine['index_list_max'] = [index for index, value in enumerate(cosine_flat) if value == cosine['similarity_max']]

    ##print(cosine['similarity_max'])

    return cosine

