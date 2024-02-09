import os
import json
import urllib.request
from dotenv import load_dotenv
from politicalindex import isPolitical

load_dotenv()

# =============================================

key = os.environ.get("GNEWS_KEY")
only_contain = "qwertyuiopasdfghjklzxcvbnmm1234567890% "

def getTopHeadlines():
    category = "world"
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max=10&apikey={key}"

    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))

    # for article in data["articles"]:
    #     print(article["title"])

    return data

def getRelatedHeadlines(original_title, original_source_name):
    filtered_title = ""

    for char in original_title.lower():
        if char in only_contain: # If one of valid characters
            filtered_title += char
    
    # Remove source name from article since it affects search of similar articles
    filtered_title = filtered_title.replace(original_source_name.lower(), "")
    filtered_title = filtered_title.replace(" ", "%20") # Urlify title

    print(f"FILTERED TITLE: {filtered_title}")

    url = f"https://gnews.io/api/v4/search?q=\"{filtered_title}\"&lang=en&country=us&max=10&apikey={key}"

    print(f"URL: {url}")

    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    count = data["totalArticles"]


    if count > 0:
        for article in data["articles"]:
            print(article["title"])
    else:
        print("NO ARTICLES FOUND LOL")

    return data

# POSSIBLE METHODS:
#  * Chinese child labor :)
#  * Check most frequently occurring non-proper nouns
#    * Proper nouns change with changing "big scoops" (eg. Niger famine and BLM riots is not very much covered now, but Israel-Hamas conflict is very much covered now)
#    * Avoid picking outdated content
#    * For example: war, polit..., gov..., conflict, etc.
#  * Ask chatgpt because fuck it

getRelatedHeadlines("Chile’s wildfires kill at least 112, as Boric warns death toll to rise - Al Jazeera English", "Al Jazeera English")