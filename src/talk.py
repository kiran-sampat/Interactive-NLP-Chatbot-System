import time
import requests

from bs4 import BeautifulSoup as bs


# function for small talk, has set responses, chosen from random based on intent
def small_talk(intent):
    ##print(intent)
    answer = intent[1]

    # st means small talk
    if ('st_time' in intent):
        # unix epoch timestamp
        t = time.time()
        answer = intent[1] + time.strftime('%r on %A, %B %d, %Y.', time.localtime(t))
    elif ('st_weather' in intent):
        # get data using bs4 and bing weather
        weather = get_weather()
        answer = intent[1] + weather

    return answer


# funtion to find the weather based on web scraping information from bing weather
def get_weather():
    # define headers for safer web crawling
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    # search query for url
    s_query = "weather"
    # url to get weather data
    URL = f"https://www.bing.com/search?q={s_query}"
    req = requests.get(URL, headers=headers)
    soup = bs(req.text, 'html.parser')

    # create dictionary to store information
    result = {}

    # store the relevant information under the corresponding key
    result['region'] = soup.select_one('span.wtr_foreGround').text
    result['time'] = soup.select_one('div.wtr_dayTime').text
    result['caption'] = soup.select_one('div.wtr_caption').text
    result['temp'] = soup.select_one('div.wtr_currTemp').text
    result['rain'] = soup.select_one('div.wtr_currPerci').text
    result['wind'] = soup.select_one('div.wtr_currWind').text
    result['temp-high'] = soup.select_one('div.wtr_high').text
    result['temp-low'] = soup.select_one('div.wtr_low').text
    result['humidity'] = soup.select_one('div.wtr_currHumi').text

    # create random string responses with the information
    response = f"{result['caption']} with a temperature of {result['temp']}°C. The highs are {result['temp-high']}C, and the Lows are {result['temp-low']}C. {result['wind']} with {result['rain']} and {result['humidity']}. As of {result['time']} in {result['region']}. (Information from Bing)."
    
    ##responses
    ##random.choice(response)

    return response

