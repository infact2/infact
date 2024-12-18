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

def add_quote(quote, source_number):
    return f"[q]{quote}[/q][SOURCE {source_number}]"

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_quote",
            "description": "Call this function whenever you would like to use a quote from any of the two sources given.",
            "parameters": {
                "type": "object",
                "properties": {
                    "quote": {
                        "type": "string",
                        "description": "The quote you are using"
                    },
                    "source_number": {
                        "type": "number",
                        "description": "The number of the source",
                    },
                },
                "required": ["quote", "source_number"],
                "additionalProperties": False,
            },
        }
    }
]


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
    
    title1 = html_parse1.title.string
    source_meta = html_parse1.find("meta", {"property": "og:site_name"})

    query = title1

    url_data = googlesearchengineapi.googleSearchAdvanced(url1, query)
    urls = url_data["entries"]
    lean1 = url_data["lean1"]
    lean2 = url_data["lean2"]

    if len(urls) == 0:
        return {
            "title": "Missing Source 2",
            "source1": "Error", "title1": "",
            "url2": "", "source2": "Error", "title2": "",
            "content": "Sorry, we were unable to find a second article to corroborate. Please try again later",

            "lean1": "nf", "lean2": "nf",

            # stats (for debug)
            "total_sites": len(urls),
            "sites_scraped": 0,
            "sites_unscrapable": 0,
            "sites_omitted": 0,
            "execution_time": 0,
            "helper_time": 0,
            "query": query
        }

    url2 = urls[0]["link"]

    source1 = "Source 1"
    source2 = "Source 2"
    title2 = "you shouldnt be seeing this lol"
    sites_scraped = 1
    sites_unscrapable = 0
    sites_omitted = 0

    html_parse2 = None

    if source_meta:
        source1 = source_meta["content"]
    
    print(f"Iterations queued: {len(urls)}")
    for url_data in urls:
        url = url_data["link"]
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
            title2 = html_parse2.title.string
            if html_parse2 == None: raise Exception("NOOOOOO")

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
        "title": title1,
        "source1": source1, "title1": title1,
        "url2": url2, "source2": source2, "title2": title2,
        "content": helper["content"],

        "lean1": lean1, "lean2": lean2,

        # stats (for debug)
        "total_sites": len(urls),
        "sites_scraped": sites_scraped,
        "sites_unscrapable": sites_unscrapable,
        "sites_omitted": sites_omitted,
        "execution_time": execution_time,
        "helper_time": helper["execution_time"],
        "query": query
    }

# prompt sections

main_instructions = """
* Corroborate news articles provided in an unbiased manner; MUST USE INFORMATION FROM BOTH ARTICLES and DO NOT CREATE NEW CONTENT
* Structure your response in multiple paragraphs, which must have at least two quotes from the provided articles; wrap these quotes with "[q]" at the start and "[/q]" at the end without the quotes, and refer to these quotes with [SOURCE 1] at the end if it came from source 1, and [SOURCE 2] for source 2
"""

language = "You are an Associated Press journalist; create a 3 paragraph concise article, add proper transitions between paragraphs."

formatting = "Note that every paragraph has to be started with \"[p]\" without the quotes and end with \"[/p]\" without the quotes."


async def corroborateHelper(html_parse1, html_parse2): # feed strings and returns corroborated version of 1st file
    print("Generating article...")
    start_time = time.time()
    # print(f"HP1: {html_parse1}\nHP2: {html_parse2}")
    text1 = articletextmanager.extractTextFromHTML(html_parse1) 
    print(f"IUGUYUYGUYUIGYUGIGIUIUGY ${html_parse2 == None}")
    text2 = articletextmanager.extractTextFromHTML(html_parse2)
    prompt = "Article 1: \"" + text1 + "\"\n Article 2: \"" + text2 + "\""
    completion = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": main_instructions + language + formatting},
            {"role": "user", "content": prompt}
        ],
        temperature = 0,
        # tools=tools,
        # tool_choice="auto"
    )
    end_time = time.time()
    return {
        "content": completion.choices[0].message.content,
        "execution_time": round((end_time - start_time) * 100.0) / 100.0,
    }

#corroborate("https://www.aljazeera.com/news/liveblog/2024/2/7/russia-ukraine-war-live-news-at-least-3-dead-as-russia-attacks-ukraine")

#print(completion.choices[0].message.content)