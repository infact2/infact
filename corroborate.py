from openai import OpenAI
from dotenv import load_dotenv
import articletextmanager
import googlesearchengineapi
import urllib.parse
from urllib.parse import urlparse
from urllib.error import *
import time

from bs4 import BeautifulSoup

load_dotenv()

client = OpenAI()

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

article1 = articletextmanager.extractText("https://www.aljazeera.com/news/liveblog/2024/2/7/russia-ukraine-war-live-news-at-least-3-dead-as-russia-attacks-ukraine")
article2 = articletextmanager.extractText("https://www.aljazeera.com/news/2024/2/7/ukraines-zaluzhny-touts-drones-as-path-to-victory-russia-suffers-strikes")
text = "Article 1: " + article1 + " Article 2:" + article2
#print(text)
#text = "poopy monkey fart"

def sameDomain(url1, url2): #checks if urls are the same
    # Parse the URLs
    parsed_url1 = urlparse(url1)
    parsed_url2 = urlparse(url2)
    
    # Extract the domain parts
    domain1 = parsed_url1.netloc
    domain2 = parsed_url2.netloc

    return domain1 == domain2



def corroborate(url1): #feed 1 string and find a similar website to corroborate
    start_time = time.time()
    print("sigma balls")
    html = urllib.request.urlopen(urllib.request.Request(url1, headers=hdr))
    html_parse = BeautifulSoup(html, "html.parser")
    title = html_parse.title.string
    source_meta = html_parse.find("meta", {"property": "og:site_name"})
    urls = googlesearchengineapi.googleSearchAdvanced(title)
    url2 = urls[0]
    i = 1

    source1 = "Source 1"
    source2 = "Source 2"
    sites_scraped = 1
    sites_unscrapable = 0
    sites_omitted = 0

    if source_meta:
        source1 = source_meta["content"]
    
    for url in urls:
        if sameDomain(url1, url):
            sites_omitted += 1
            continue
        sites_scraped += 1
        try:
            print("st; ", end="")
            html = urllib.request.urlopen(url, headers=hdr)
            html_parse = BeautifulSoup(html, "html.parse")
            source_meta2 = html_parse.find("meta", {"property": "og:site_name"})
            print("s; ", end="")
            url2 = url
            source2 = source_meta2["content"]
            break
        except:
            print("us; ", end="")
            sites_unscrapable += 1
            continue

    end_time = time.time()
    helper = corroborateHelper(url1, url2)
    execution_time = round((end_time - start_time) * 100.0) / 100.0
    print()
    print(f"S: {sites_scraped}; US: {sites_unscrapable}; SO: {sites_omitted}; ET: {execution_time}; GT: {helper['execution_time']}")
    return {
        "source1": source1,
        "url2": url2, "source2": source2,
        "content": helper["content"],

        # stats (for debug)
        "total_sites": len(urls),
        "sites_scraped": sites_scraped,
        "sites_unscrapable": sites_unscrapable,
        "sites_omitted": sites_omitted,
        "execution_time": execution_time,
        "helper_time": helper["execution_time"]
    }

# prompt sections

main_instructions = "Corroborate the news articles provided. Present an unbiased version of the information in the two articles, avoiding extreme opinions. Structure your response in multiple paragraphs. Cite examples of biased keywords or inaccurate information. Stick to the source material and avoid creating new content. If the two sources are identical, mention this after the corroboration."

language = "Ensure the new article is at least paragraphs long, each using information from both sources. Avoid repetitive phrasing and construct concise, coherent sentences in the style of an Associated Press journalist. Begin each paragraph with proper transitions if there is a previous paragraph"

formatting = "Note that every paragraph has to be started with \"[p]\" without the quotes and end with \"[/p]\" without the quotes."


def corroborateHelper(url1, url2): # feed strings and returns corroborated version of 1st file
    start_time = time.time()
    text1 = articletextmanager.extractText(url1) 
    text2 = articletextmanager.extractText(url2)
    prompt = "Article 1: \"" + text1 + "\"\n Article 2: \"" + text2 + "\""
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": main_instructions + language + formatting},
            {"role": "user", "content": prompt}
        ],
        temperature = 0,
    )
    end_time = time.time()
    return {
        "content": completion.choices[0].message.content,
        "execution_time": round((end_time - start_time) * 100.0) / 100.0
    }

#corroborate("https://www.aljazeera.com/news/liveblog/2024/2/7/russia-ukraine-war-live-news-at-least-3-dead-as-russia-attacks-ukraine")

#print(completion.choices[0].message.content)