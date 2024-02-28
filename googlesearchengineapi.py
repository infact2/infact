import requests
import json

def getDaLinks(prompt):
       #print("Given Prompt: " + prompt + "\n")
       prompt += ' news articles'

       #parameters
       apiKey = 'AIzaSyDqabrP5CbkUciLP9nr4o_9XKDtNiwp5hs'
       searchEngineID = "d6c2539d1fec44866" #cx
       start = 1
       numPages = 1
       url = f'https://www.googleapis.com/customsearch/v1?key={apiKey}&cx={searchEngineID}&q={prompt}&siteSearch=news.google.com&time_period=last_year&max_page={numPages}'
       #print(url)
       
       requestedUrls = [0] * numPages * 10

       response = requests.get(url).json()
       #print(response)
       
       # get the result items
       search_items = response.get("items")
       # iterate over 10 results found
       if search_items is not None:
              for i, search_item in enumerate(search_items, start=1):
                     try:
                            long_description = search_item["pagemap"]["metatags"][0]["og:description"]
                     except KeyError:
                            long_description = "N/A"
                     # get the page title
                     title = search_item.get("title")
                     # page snippet
                     snippet = search_item.get("snippet")
                     # alternatively, you can get the HTML snippet (bolded keywords)
                     html_snippet = search_item.get("htmlSnippet")
                     # extract the page url
                     link = search_item.get("link")
                     # print the results
                     #print("="*10, f"Result #{i+start-1}", "="*10)
                     #print("Title:", title)
                     #print("Description:", snippet)
                     #print("Long description:", long_description)
                     #print("URL:", link, "\n")
                     #og_url = search_item["pagemap"]["metatags"][0]["og:url"]
                     #print(og_url, "\n")
                     #search_item_formatted = json.dumps(search_item, indent = 2)
                     #print(search_item_formatted, "\n")
                     requestedUrls[i-1] = link
              return requestedUrls

       else:  
              print("provide a different prompt, this had no results")


def googleSearchBasic(prompt):
       getDaLinks(prompt)
def googleSearchAdvanced(prompt):
       getDaLinks(prompt)
getDaLinks("ivf")

#getLinks(["San", "Diego", "homeless"])
#test push 3