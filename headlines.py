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

    def getTopHeadlines(self):
        return self.cache

    def setTopHeadlines(self):
        print("Resetting headlines...")
        category = "WORLD"

        top_headlines = _newsapi.get_top_headlines()
        new_cache = []

        # check if the request was successful
        if top_headlines["status"] == "ok":
            articles = top_headlines["articles"]
            # Print the titles and URLs of the top headlines
            cur = 0
            for article in articles:
                if isPolitical(article["title"]):
                    new_cache.append(article)
                    print(f"LOADED: {cur}/{len(articles)} articles")
                else: print(f"LOADED: {cur}/{len(articles)} articles SKIPPED")
                cur += 1
        else:
            print(f"Error fetching top headlines: {top_headlines['message']}")
        self.cache = new_cache

    async def interval(self):
        while True:
            await asyncio.sleep(60 * 2.5)
            setTopHeadlines(self)

    def startInterval(self):
        print("Interval started")
        asyncio.run(interval())