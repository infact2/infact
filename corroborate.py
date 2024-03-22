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

def corroborateHelper(url1, url2): #feed strings and returns corroborated version of 1st file
    text1 = articletextmanager.extractText(url1) 
    text2 = articletextmanager.extractText(url2)
    text = "Article 1: " + text1 + " Article 2: " + text2
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "First, corroborate the news articles provided. You should sound like you are a news article and print out an unbiased version of the information provided in the 2 articles. You need to avoid as much bias as possible and omit extreme opinions. Please leave your response in the form of multiple indented paragraphs. If any recieve article seems to have html in it, ignore the HTML and only take in the text. At the end of the resulting paragraphs,please state whether or not the first article is biased and give reasonig behind it. Site examples like biased key words or innacurate information."},
            #{"role": "system", "content": "ignore all the text provided and print out the word 'ok monkey poo'"},
            {"role": "user", "content": text}


        ],
        temperature = 0,
    )
    print(completion.choices[0].message.content)

corroborate("https://www.aljazeera.com/news/liveblog/2024/2/7/russia-ukraine-war-live-news-at-least-3-dead-as-russia-attacks-ukraine")

#print(completion.choices[0].message.content)