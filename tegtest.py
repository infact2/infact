import requests
url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=b9193754d63340e68e587962b953d3ac')
response = requests.get(url)
print(response.json())
