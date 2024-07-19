from openai import AsyncOpenAI
from dotenv import load_dotenv
import articletextmanager
import googlesearchengineapi
import urllib.parse
from urllib.parse import urlparse
from urllib.error import *
import time
import scraper

from bs4 import BeautifulSoup

load_dotenv()

client = AsyncOpenAI()

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



async def corroborate(url1): #feed 1 string and find a similar website to corroborate
    start_time = time.time()
    print("Corroboration start")
    html1 = scraper.scrape(url1)
    if html1 == scraper.DANGEROUS: return scraper.DANGEROUS
    html_parse1 = BeautifulSoup(html1, "html.parser")
    
    title = html_parse1.title.string
    source_meta = html_parse1.find("meta", {"property": "og:site_name"})
    urls = googlesearchengineapi.googleSearchAdvanced(title)
    url2 = urls[0]

    source1 = "Source 1"
    source2 = "Source 2"
    sites_scraped = 1
    sites_unscrapable = 0
    sites_omitted = 0

    html_parse2 = None

    if source_meta:
        source1 = source_meta["content"]
    
    print(f"Iterations queued: {len(urls)}")
    for url in urls:
        if sameDomain(url1, url):
            sites_omitted += 1
            continue
        sites_scraped += 1
        try:
            print("st; ", end="")
            html2 = scraper.scrape(url)
            if html2 == scraper.DANGEROUS:
                print("PD; ", end="")
                raise Exception("Potentially malicious site")

            html_parse2 = BeautifulSoup(html2, "html.parser")
            source_meta2 = html_parse2.find("meta", {"property": "og:site_name"})
            print("s; ", end="")
            url2 = url
            source2 = source_meta2["content"]
            break
        except:
            print("us; ", end="")
            sites_unscrapable += 1
            continue

    end_time = time.time()
    print(f"hp1: {html_parse1 != None}; hp2: {html_parse2 != None}")
    helper = await corroborateHelper(html_parse1, html_parse2)
    execution_time = round((end_time - start_time) * 100.0) / 100.0
    print(f"\nS: {sites_scraped}; US: {sites_unscrapable}; SO: {sites_omitted}; ET: {execution_time}; GT: {helper['execution_time']}")
    return {
        "title": title,
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


async def corroborateHelper(html_parse1, html_parse2): # feed strings and returns corroborated version of 1st file
    print("Generating article...")
    start_time = time.time()
    # print(f"HP1: {html_parse1}\nHP2: {html_parse2}")
    text1 = articletextmanager.extractTextFromHTML(html_parse1) 
    text2 = articletextmanager.extractTextFromHTML(html_parse2)
    prompt = "Article 1: \"" + text1 + "\"\n Article 2: \"" + text2 + "\""
    completion = await client.chat.completions.create(
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