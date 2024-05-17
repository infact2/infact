import requests
import json
from dotenv import load_dotenv
from urllib.parse import urlparse
from collections import deque
from politicalindex import isPolitical
import os

load_dotenv()

def appendToStart(original, item):
    resultant = deque(original)
    resultant.appendleft(item)
    return list(resultant)

def getDaLinks(prompt, as_array = True, restrict_political = False):
    #print("Given Prompt: " + prompt + "\n")
    prompt += ' articles'

    #parameters
    apiKey = os.getenv("GOOGLE_API_KEY")
    searchEngineID = "d6c2539d1fec44866" #cx
    start = 1
    numPages = 1
    url = f'https://www.googleapis.com/customsearch/v1?key={apiKey}&cx={searchEngineID}&q={prompt}&time_period=last_year&max_page={numPages}'
    #print(url)

    response = requests.get(url).json()
    #print(response)

    requested_urls = None

    if as_array:
        requested_urls = []
    else:
        requested_urls = {"count": 0, "entries": []}
    
    # get the result items
    search_items = response.get("items")
    #print(search_items)

    # iterate over 10 results found
    if search_items is not None:
        for i, search_item in enumerate(search_items, start=1):
            try:
                long_description = search_item["pagemap"]["metatags"][0]["og:description"]
            except KeyError:
                long_description = "N/A"
            # get the page title
            title = search_item.get("title")
            if title.lower() == "google news": continue
            # page snippet
            snippet = search_item.get("snippet")
            # alternatively, you can get the HTML snippet (bolded keywords)
            html_snippet = search_item.get("htmlSnippet")
            # extract the page url
            unredirected_link = search_item.get("link")
            link = requests.get(unredirected_link).url 
            # print the results
            #print("="*10, f"Result #{i+start-1}", "="*10)
            #print("Title:", title)
            #print("Description:", snippet)
            #print("Long description:", long_description)
            #print("URL:", unredirected_link, "\n")
            # og_url = search_item["pagemap"]["metatags"][0]["og:url"]
            # print(og_url, "\n")
            #search_item_formatted = json.dumps(search_item, indent = 2)
            #print(search_item_formatted, "\n")

            if restrict_political and not isPolitical(title): continue
            
            if as_array:
                requested_urls = appendToStart(requested_urls, link)
            else:
                parsed_url = urlparse(link)
                requested_urls["entries"] = appendToStart(requested_urls["entries"], {
                    "title": title, 
                    "link": link,
                    "source": {
                        "title": parsed_url.hostname.split(".")[1].upper(), # eg. FOX NEWS
                        "link": f"{parsed_url.scheme}://{parsed_url.hostname}" # source homepage
                    }
                })
                requested_urls["count"] += 1
        
        return requested_urls
    else:  
        print("provide a different prompt, this had no results")
        if as_array: return []
        return {"count": 0, "entries": []}

def getTopHeadlines(category = "world"):
    return getDaLinks(category, False, True)
def googleSearchBasic(prompt):
    return getDaLinks(prompt, True, True)
def googleSearchAdvanced(prompt):
    return getDaLinks(prompt)
#getDaLinks("ivf")

#googleSearchBasic("The new TikTok ban bill, explained: When it could take effect, why lawmakers want to pass it and more")
#getLinks(["San", "Diego", "homeless"])
#test push 3
