import requests

def getDaLinks(prompt):
       #print("Given Promt: " + prompt)
       
       
       prompt += "&"

       url = 'https://cse.google.com/cse?cx=d6c2539d1fec44866'

       parameters = {
              'cx': "d6c2539d1fec44866",
              'q': prompt,
              'sortBy': 'popularity&',
              'language': 'en',
              'from': '2023-01-01&',
              'pageSize': 5,
              'apiKey': 'AIzaSyDqabrP5CbkUciLP9nr4o_9XKDtNiwp5hs'
       }

       response = requests.get(url, params = parameters)

       response_json = response.json()
       for article in response_json['articles']:
              article_url = article["url"]
              print(f"{article_url}")

       return response_json

keywords = ["San", "Francisco", "homeless", "China"]
getDaLinks(keywords)

#getLinks(["San", "Diego", "homeless"])
#test push 3