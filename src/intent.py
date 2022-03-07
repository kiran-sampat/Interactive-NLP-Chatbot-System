import json
import random

from sklearn.feature_extraction.text import TfidfVectorizer

from process import pre_process
from process import similarity_find


# function for selecting the intent
# do not filter stop words for intent matching
def match_intent(query, threshold):
    # give the path for the Intents Dataset
    json_file_path = 'datasets/Intents.json'

    # pre process the input query, passing false to keep stopwords
    lemmatized_string = pre_process(query, False)

    # create the test set to be vectorized as the testing data
    test_set = (lemmatized_string, "")

    with open(json_file_path) as sentences_file:
        lemmatized_train_set = []
        indexed_json_list = []
        data = json.load(sentences_file)

        # traverse the entire json file
        for row in data['intents']:
            # traverse only the pattern elements of the json file
            for i, pattern in enumerate(row['patterns']):
                # add intent tag with a randomly selected response to indexed json list
                # this makes finding the response for corresponding tag easier for small talk
                # since with json i cannot reverse search the corresponding response based on the tag or index later on
                tuple_of_values = (row['tag'], random.choice(row['responses']))
                indexed_json_list.append(tuple_of_values)

                # pre process the patterns in the intents json file, keeping stopwords
                patterns_lemmatized_string = pre_process(row['patterns'][i], False)

                # append the lemmatized string to the overall list
                lemmatized_train_set.append(patterns_lemmatized_string)

    # call fit_transform() on training data and transform() on test data
    
    # vectorize the intents patterns (training data) with TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_dataset = tfidf_vectorizer.fit_transform(lemmatized_train_set)

    # vectorize the query (testing data) with TF-IDF
    tfidf_matrix_query = tfidf_vectorizer.transform(test_set)

    # find cosine similarity by calling the similarity function, passing both matricies
    cosine = similarity_find(tfidf_matrix_query, tfidf_matrix_dataset)

    # threshold
    if (cosine['similarity_max'] <= threshold):
        return (None, None)
    else:
        for index, data_tuple in enumerate(indexed_json_list):
            if index in cosine['index_list_max']:
                return data_tuple
