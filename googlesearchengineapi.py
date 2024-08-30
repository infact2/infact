import requests
import json
from dotenv import load_dotenv
from urllib.parse import urlparse
from collections import deque
from politicalindex import isPolitical
import os
import spacy

nlp = spacy.load("en_core_web_sm")

load_dotenv()

media_bias_data = {}
bias_keys = []
# NOTE: -6 is far left, vice versa
with open("media_bias.json", "r") as file:
    media_bias_data = json.load(file)
    bias_keys = [float(i) for i in media_bias_data.keys()]
    bias_keys.sort()

def websiteLeaning(url): # note: should return as an actual number, instead of a string to use as a key
    # we want to make sure that (for example) if the article is a part of "https://apnews.com/hub/" it doesn't get recognized as a part of "https://apnews.com/." idk if i worded that well but yeah
    largest_base = ""
    leaning_to_use = 0
    for key in media_bias_data:
        for source in media_bias_data[key]:
            filtered_url = url.replace("http://", "").replace("https://", "")
            filtered_source_url = source["url"].replace("http://", "").replace("https://", "")
            if filtered_url.startswith(filtered_source_url) and len(filtered_source_url) > len(largest_base):

                largest_base = filtered_source_url
                leaning_to_use = float(key)
    return leaning_to_use

def leaningKeyToString(number):
    ret_value = str(number)
    negative = ret_value[0] == "-"
    while (not negative and len(ret_value) < 4) or (negative and len(ret_value) < 5):
        ret_value += "0"
    return ret_value
def negatingLeaning(article_leaning): # finds the leaning that can be used to search for a second article, preferrably one that has the opposite leaning as the current article
    leaning_to_use = 0
    best_difference = 100
    for i in range(1, len(bias_keys)):
        previous, cur = bias_keys[i - 1], bias_keys[i]
        previous_distance, cur_distance = abs(previous + article_leaning), abs(cur + article_leaning)
        if previous_distance < best_difference:
            leaning_to_use = previous
            best_difference = previous_distance
        elif cur_distance < best_difference:
            leaning_to_use = cur
            best_difference = cur_distance

    
    return leaningKeyToString(leaning_to_use)

def generateQuery(article_leaning):
    key = negatingLeaning(article_leaning)
    # print(bias_keys)
    # print(f"KEYUYYYY {key}")
    sources = media_bias_data[key]
    query = " "
    for source in sources:
        if source == sources[-1]: # if last link, don't include "OR"
            query += f"site:{source["url"]}"
        else:
            query += f"site:{source["url"]} OR "
    return query

def appendToStart(original, item):
    resultant = deque(original)
    resultant.appendleft(item)
    return list(resultant)

def getDaLinks(original_url, raw_prompt, as_array = True, restrict_political = False):
    #print("Given Prompt: " + prompt + "\n")
    article_leaning = websiteLeaning(original_url)
    query = generateQuery(article_leaning)

    # encoded_prompt = str(raw_prompt.encode('utf-8'))
    encoded_prompt = str(raw_prompt)
    print(f"EP: {encoded_prompt}")
    doc = nlp(encoded_prompt)

    prompt = ""
    for keyword in doc.ents:
        if "news" in keyword.text.lower(): continue
        prompt += f"{keyword} "
    print(f"QLP: {prompt}")
    prompt += query
    print(f"GEN INFO\nLEAN1: {article_leaning}\nQUERY: {query}")
    # prompt += " article"

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
def googleSearchBasic(original_url, prompt):
    return getDaLinks(original_url, prompt, True, True)
def googleSearchAdvanced(original_url, prompt):
    return getDaLinks(original_url, prompt)
#getDaLinks("ivf")

# googleSearchBasic("https://apnews.com/peepeepoopoo", "Israel Gaza")
#getLinks(["San", "Diego", "homeless"])
#test push 3
