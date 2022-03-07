import json
import pandas as pd

from process import pre_process
from intent import match_intent
from talk import small_talk
from retrieval import question_answering
from transaction import transaction_hotel


def main():
    print("-----------\n")

    initialize_data()

    bot_name = 'Bot'
    user_name = identity_init(bot_name)
    
    intent_threshold = 0.85
    qa_threshold = 0.55

    while (True):

        query = input(f"{user_name}: ")

        intent = match_intent(query.lower(), intent_threshold)

        # intent debugging
        ##bot_name = f"Bot-{intent[0]}"

        # if no intention is set then go to QA dataset
        if (not None in intent):

            if ('leave_bot' in intent):
                leave = exit_bot(bot_name, user_name)
                if (leave):
                    break
                else:
                    continue
                    
            elif ('name' in intent[0]):
                # identity manage returns tuple of (answer, user_name)
                name_tuple = identity_manage(query, intent, user_name, bot_name)
                answer = name_tuple[0]
                
                # set new user_name only if that was the intent
                if (name_tuple[1] != None):
                    user_name = name_tuple[1]
                print(f"{bot_name}: {answer}")
                
            elif ('transaction' in intent[0]):
                # run hotel transaction
                transaction_hotel(bot_name, user_name)
                
            elif ('game' in intent[0]):
                # run game code (either hangman or an text based rpg)
                print(f"game")
                
            else:
                print(f"{bot_name}: {small_talk(intent)}")
                
        else:
            info_retrieval = question_answering(query, qa_threshold)
            print(f"{bot_name}: {info_retrieval}")

    print("\n-----------")


# function to convert the dataset csv file into json file
def initialize_data():
    # convert the csv into pandas dataframes
    Dataset = pd.read_csv('datasets/QuestionAnswerPairs.csv')
    # remove unnecessary columns
    Dataset.drop(['QuestionID', 'Document'], axis=1)
    # covert dataframes to JSON, records is {column -> value}
    Dataset_JSON = json.loads(Dataset.to_json(orient='records'))
    # export the data as JSON
    with open('output/Dataset.json', 'w') as file_out:
        json.dump(Dataset_JSON, file_out)


# function to deal with exiting the chatbot
def exit_bot(bot_name, user_name):
    print(f"{bot_name}: Are you sure you want to leave?")
    sentence_in = input(f"{user_name}: (yes/no): ")

    # make input lowercase to parse it more efficiently
    selection = sentence_in.lower()

    if ('yes' in selection or selection == 'y'):
        print(f"{bot_name}: Bye! I hope you found the conversation useful!")
        return True
    elif ('no' in selection or selection == 'n'):
        print(f"{bot_name}: Welcome back! How can I help you?")
        return False
    else:
        print(f"{bot_name}: This is not a valid selection. How can I help you?")
        return None


# function to initialize the user name when bot starts
def identity_init(bot_name):
    print(f"{bot_name}: To get started, please enter your name at the prompt.")
    sentence_in = input(f"{bot_name}: ")

    # checking empty name
    if (sentence_in.strip()):
        user_name = name_change(sentence_in)
        print(f"{bot_name}: Hello {user_name}, my name is {bot_name}, to exit please wave goodbye. :)")
    else:
        user_name = 'User'
        print(f"{bot_name}: You cannot leave your name blank")
        print(f"{bot_name}: A default name has been set as {user_name}. You may change this at any time.")

    return user_name


# function to manage identities, which returns a tuple, values based on intent
def identity_manage(query, intent, user_name, bot_name):
    ##print(intent)
    new_user_name = None

    if ('name_change_user' in intent):
        new_user_name = name_change(query)
        answer = intent[1] + new_user_name
    elif ('name_ask_user' in intent):
        answer = intent[1] + user_name
    elif ('name_ask_bot' in intent):
        answer = intent[1] + bot_name
    else:
        answer = None

    return (answer, new_user_name)


# function to change the user name, returns string
def name_change(query):
    # initialize new user name as an empty string
    new_user_name = ''
    # remove punctuation, tokenize and lemmatize query
    tokens = pre_process(query, True).split(" ")
    # capitalize all values in list
    tokens = list(map(str.capitalize, tokens))

    # could try to implement name detection using pos tags with Proper Nouns (NNP)
    # though name detection and parsing is very difficult to do properly
    """
    names = []
    
    for token, tag in pos_tag(tokens):
        if 'NNP' in tag:
            names.append(token)
    print(names)
    
    if(names):
        new_user_name = names[-1]
    else:
        new_user_name = 'User'
    """

    # assign new user name, -1 gives last value in the list of tokens
    new_user_name = tokens[-1]
    
    return new_user_name


# call main function
if __name__ == "__main__":
    main()
