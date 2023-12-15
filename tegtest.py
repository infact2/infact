import requests

prompt = "hamas" + "&"

url = 'https://newsapi.org/v2/everything?' 

parameters = {
       'q': prompt,
       'sortBy': 'popularity&',
       'pageSize': 20,
       'apiKey': 'b9193754d63340e68e587962b953d3ac'
}

response = requests.get(url, params = parameters)

response_json = response.json()
for article in response_json['articles']:
    article_url = article["url"]
    print(f"{article_url}")