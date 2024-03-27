from openai import OpenAI
from dotenv import load_dotenv
import articletextmanager
import googlesearchengineapi
import urllib.parse
from urllib.parse import urlparse

from bs4 import BeautifulSoup

load_dotenv()

client = OpenAI()


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
    print("sigma balls")
    html = urllib.request.urlopen(urllib.request.Request(url1))
    html_parse = BeautifulSoup(html, "html.parser")
    title = html_parse.title.string
    urls = googlesearchengineapi.googleSearchAdvanced(title)
    url2 = urls[0]
    i = 1
    if not sameDomain(url1, url2):
        return corroborateHelper(url1, url2)
    else:
        print("cycle 1 sigma balls")
        url2 = urls[i]
        print("article 1: " + url1 + " article 2: " + url2)
        i += i


    return corroborateHelper(url1, url2)

# prompt sections

main_instructions = "First, corroborate the news articles provided. You should sound like you are a news article and print out an unbiased version of the information provided in the 2 articles. You need to avoid as much bias as possible and omit extreme opinions. Please leave your response in the form of multiple indented paragraphs. If any recieve article seems to have html in it, ignore the HTML and only take in the text. Cite examples like biased key words or innacurate information. Please do not try to make up new things, and stick to the source material whenver possible."

language = "Please be sure that this new article is 3-5 paragraphs long, and each paragraph may use information from both articles. Please also be sure to avoid phrasing repetition, construct concise, yet coherent sentences, and write like you are a good journalist from the Associated Press. At the start of a paragraph, please add proper transitions from the previous paragraph (if there is a previous paragraph) to the current."

formatting = "Note that every paragraph has to be started with \"<p>\" without the quotes and end with \"</p>\" without the quotes."


def corroborateHelper(url1, url2): # feed strings and returns corroborated version of 1st file
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
    return completion.choices[0].message.content

#corroborate("https://www.aljazeera.com/news/liveblog/2024/2/7/russia-ukraine-war-live-news-at-least-3-dead-as-russia-attacks-ukraine")

#print(completion.choices[0].message.content)