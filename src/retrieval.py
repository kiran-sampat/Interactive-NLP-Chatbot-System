import json
import requests

from bs4 import BeautifulSoup as bs
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer

from process import pre_process
from process import similarity_find


# function for information retrieval from the qa dataset
def question_answering(query, threshold):
    # give the path for the qa dataset
    json_file_path = "output/Dataset.json"

    # set a path for the serialized files
    tfidf_vectorizer_path = "output/tfidf_vectorizer.joblib"
    tfidf_matrix_path = "output/tfidf_matrix.joblib"

    # pre process the input query, passing true to also remove stopwords
    lemmatized_string = pre_process(query, True)

    # create the test set to be vectorized as the testing data
    test_set = (lemmatized_string, "")

    # use serialized post-tokenized training data
    try:
        tfidf_vectorizer = load(tfidf_vectorizer_path)
        tfidf_matrix_dataset = load(tfidf_matrix_path)

    # vectorize training data
    except:
        with open(json_file_path) as sentences_file:
            lemmatized_train_set = []
            data = json.load(sentences_file)

            # tokenize training data    
            for row in data:
                # pre process the questions in the QA dataseet file, also removing stopwords
                patterns_lemmatized_string = pre_process(row['Question'], True)

                # append the lemmatized string to the overall list
                lemmatized_train_set.append(patterns_lemmatized_string)

        # call fit_transform() on training data and transform() on test data

        # learns vocabulary and idf, then gives document-term matrix
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_dataset = tfidf_vectorizer.fit_transform(lemmatized_train_set)

        # serialize the vectorizer and the training data matrix
        dump(tfidf_vectorizer, tfidf_vectorizer_path)
        dump(tfidf_matrix_dataset, tfidf_matrix_path)

    # vectorize the query (testing data) with TF-IDF
    tfidf_matrix_query = tfidf_vectorizer.transform(test_set)

    # find cosine similarity by calling the similarity function, passing both matricies
    cosine = similarity_find(tfidf_matrix_query, tfidf_matrix_dataset)

    #### FOR BENCHMARK TESTING ####
    #with open(json_file_path, "r") as sentences_file:
    #    data = json.load(sentences_file)
    #    for index, row in enumerate(data):
    #        if cosine['similarity_max'] != 0 and index in cosine['index_list_max']:
    #            print(row['Question'])
    #
    #print(cosine['similarity_max'])

    # threshold
    if(cosine['similarity_max'] <= threshold):
        # search google if threshold is below a certain value
        google_result = google_search(query)
        
        if(google_result):
            return google_result
        else:
            not_understood = "Sorry, I am not able to answer that right now."
            return not_understood
    else:
        with open(json_file_path, "r") as sentences_file:
            data = json.load(sentences_file)
            # use list comprehension to store all relevant answers into a list
            answers_list = [row['Answer'] for index, row in enumerate(data) if index in cosine['index_list_max']]

        # converts the response list into one string
        answer = " ".join(answers_list)

        return answer


# funtion to find an answer based on web scraping information from a google search
def google_search(query):
    # define headers for safer web crawling
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    # search query for url
    s_query = query.replace(" ", "+")
    # url to get search information
    URL = f"https://www.google.com/search?q={s_query}"
    req = requests.get(URL, headers=headers)
    soup = bs(req.text, 'html.parser')

    result = soup.select_one('div.kno-rdesc > span')

    if(result):
        processed_result = result.text.replace("\n", " ")
        answer = f"{processed_result} (Information from Google)."
        return answer
    else:
        return None

