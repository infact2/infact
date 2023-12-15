import requests

prompt = 'q=trump impeachment&'

url = ('https://newsapi.org/v2/everything?' 
       'q=&'
       'sortBy=popularity&' 
       'apiKey=b9193754d63340e68e587962b953d3ac')

response = requests.get(url)

for article in response.json()["articles"]:
    article_url = article["url"]
    print(f"{article_url}")