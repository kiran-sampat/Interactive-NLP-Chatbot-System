import requests

from bs4 import BeautifulSoup as bs


# function to deal with a short hotel booking transaction
# web scrapes Expedia based on user inputs
def transaction_hotel(bot_name, user_name):

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    
    yes_response = ['y', 'ye', 'yea', 'yes', 'yeah', 'okay', 'ok', 'correct', 'sure']
    cancel_response = ['c', 'cancel', 'bye', 'terminate', 'end', 'close', 'conclude', 'finish', 'scratch', 'leave']

    print(f"{bot_name}: Would you like to book a hotel?")
    confirm_book = input(f"{user_name}: ")
    
    if confirm_book in yes_response:
        transaction_complete = False
        
        while(not transaction_complete):
            
            # questions to get data to query Expedia with
            print(f"{bot_name}: Which city will you be travelling to?")
            city = input(f"{user_name}: ")
            print(f"{bot_name}: What will your check in date be? (yyyy-mm-dd)")
            date_in = input(f"{user_name}: ").replace("/", "-")
            print(f"{bot_name}: What about your check out date? (yyyy-mm-dd)")
            date_out = input(f"{user_name}: ").replace("/", "-")
            print(f"{bot_name}: How many adults will be staying?")
            adults = input(f"{user_name}: ")
            print(f"{bot_name}: How many children will be staying?")
            children = input(f"{user_name}: ")
            
            print(f"{bot_name}: Search for Hotels in {city} between {date_in} and {date_out} for {adults} adults and {children} children?")
            confirm_search = input(f"{user_name}: ")
            
            # error checking for search confirmation
            ##if confirm_search not in yes_response:
            ##    break
            
            print(f"{bot_name}: Searching for Hotels on Expedia. One moment please...")
            
            # query Expedia with beautiful soup
            expedia_params = f"&destination={city}&startDate={date_in}&endDate={date_out}&adults={adults}&children={children}"
            URL = f"https://www.expedia.co.uk/Hotel-Search?{expedia_params}&sort=RECOMMENDED&partialStay=false&useRewards=false"
            req = requests.get(URL, headers=headers)
            soup = bs(req.text, "html.parser")
            
            # filter out all the required html data
            raw_hotel_names = soup.find_all('h3', attrs={'class':'uitk-heading-5 is-visually-hidden'})
            raw_hotel_prices = soup.find_all('span', attrs={'data-stid':'price-lockup-text'})
            raw_hotel_times = soup.find_all('div', attrs={'class':'pwa-theme--grey-700 uitk-type-100 uitk-type-regular'})
            
            # define 3 empty lists to store hotel info
            hotel_names, hotel_prices, hotel_times = ([] for i in range(3))
            
            # loop to fill the lists with the filtered information
            # zip allows to iterate over multiple lists/tuples simultaneously 
            # based on the list with the minimum length, but all three lists are the same length in this case
            total_val = 0
            for (raw_name, raw_price, raw_time) in zip(raw_hotel_names, raw_hotel_prices, raw_hotel_times):
                hotel_names.append(raw_name.getText().strip())
                hotel_prices.append(raw_price.getText().strip())
                hotel_times.append(raw_time.getText().strip())
                total_val += 1

            # define dictionary for all hotel data
            hotels = {}
            
            # fill the dictionary with data
            hotels['names'] = hotel_names
            hotels['prices'] = hotel_prices
            hotels['times'] = hotel_times
            
            if (total_val > 8):
                total = 8
            else:
                total = total_val
                
            # loop over the lists within the dictionary
            # three params for range: start_index, end_index, increment_value
            print("------------------------")
            for i in range(0, total, 1):
                name = hotels['names'][i]
                price = hotels['prices'][i]
                time = hotels['times'][i]
                print(f"    {i + 1:02d}. \"{name}\" at a total price of {price} {time}.")
            print("------------------------")            
            
            # ask for selected index of the listed hotels            
            print(f"{bot_name}: Please select which hotel you would like to stay at, by choosing the given number: ")
            terminated = False
            
            while (True):
                chosen_index = input(f"{user_name}: ")
                if (chosen_index in cancel_response):
                    terminated = True
                    break
                if (not chosen_index.isdigit()):
                    print(f"{bot_name}: This is not a valid selection.")
                    print(f"{bot_name}: Please state if you wish to cancel, or enter your desired hotel number again. Thank you.")
                    continue
                else:
                    if (int(chosen_index) > 0 and int(chosen_index) <= 8):
                        break   
                    else:
                        print(f"{bot_name}: This is not a valid selection.")
                        print(f"{bot_name}: Please state if you wish to cancel, or enter your desired hotel number again. Thank you.")
                        continue
                        
            if (terminated == True):
                break
            
            # the index is decremented by 1, since the list of hotels start from 0, but human readability starts from 1
            index = int(chosen_index) - 1
            chosen_hotel = f"{hotels['names'][index]} {time}, at a total price of {price}"
            
            # hotel booking confirmation statement
            print(f"{bot_name}: To confirm you have selected: {chosen_hotel}? Is that correct? ")
            confirm_book = input(f"{user_name}: ")
            
            # check confirmation
            if confirm_book in yes_response:
                print(f"{bot_name}: The rooms have now been booked for you, you will recieve more information soon.")
                print(f"{bot_name}: Thank you for using this service!")
                transaction_complete = True
            else:
                # ask for booking retry if not confirmed
                print(f"{bot_name}: Would you like to retry the booking, if the details are incorrect? ")
                retry = input(f"{user_name}: ")
                if retry in yes_response:
                    transaction_complete = False
                else:
                    print(f"{bot_name}: The transaction has now been cancelled.")
                    transaction_complete = True
                    
            return

    print(f"{bot_name}: Bye! Come back when you have decided on the details!")
    return

