import os
import json
import asyncio
import requests
import aiohttp
import base64
from dotenv import load_dotenv
from politicalindex import isPolitical
# from newsapi.newsapi_client import NewsApiClient
from newsapi import NewsApiClient
from bs4 import BeautifulSoup

load_dotenv()

# =============================================

# key = os.environ.get("GNEWS_KEY")
# only_contain = "qwertyuiopasdfghjklzxcvbnmm1234567890% "
_newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

class Headlines:
    cache = []
    quota = 8

    def getTopHeadlines(self):
        return self.cache

    def setTopHeadlines(self):
        print("Resetting headlines...")

        new_cache = []
        unskipped_articles = 0
        page = 1
        while unskipped_articles < self.quota:
            try:
                top_headlines = _newsapi.get_top_headlines(page=page)
            except:
                print("results limited")
                break

            # check if the request was successful
            if top_headlines["status"] == "ok":
                articles = top_headlines["articles"]
                # Print the titles and URLs of the top headlines
                cur = 0
                for article in articles:
                    if unskipped_articles >= self.quota:
                        print("quota met (f)")
                        break # if article quota met, break.
                    if isPolitical(article["title"]):
                        new_cache.append(article)
                        unskipped_articles += 1
                        print(f"LOADED: {cur}/{len(articles)} articles (t: {unskipped_articles})")
                    else: print(f"LOADED: {cur}/{len(articles)} articles (t: {unskipped_articles}) [SKIPPED]")
                    cur += 1
            else:
                print(f"Error fetching top headlines: {top_headlines['message']}")
                break # stop searching if error
            page += 1
        self.cache = new_cache

    async def interval(self):
        while True:
            await asyncio.sleep(60 * 2.5)
            setTopHeadlines(self)

    def startInterval(self):
        print("Interval started")
        asyncio.run(interval())