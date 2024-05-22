import os
import json
import asyncio
import requests
import aiohttp
import urllib.request
import time
import base64
from dotenv import load_dotenv
from politicalindex import isPolitical
from pygooglenews import GoogleNews
from bs4 import BeautifulSoup

# =============================================

# key = os.environ.get("GNEWS_KEY")
# only_contain = "qwertyuiopasdfghjklzxcvbnmm1234567890% "

class Headlines:
    cache = {}
    gn = None

    def __init__(self):
        load_dotenv()
        self.gn = GoogleNews()

    def getTopHeadlines(self):
        return self.cache

    async def setTopHeadlines(self):
        print("Resetting headlines...")
        category = "WORLD"

        async with aiohttp.ClientSession() as session:
            new_headlines = self.gn.topic_headlines(category)
            entries = new_headlines["entries"]
            count = len(entries)

            for i in range(count):
                print(f"i: {i}; count: {count}")
                unredirected_link = entries[i]["link"]
                print("request")

                response = await session.get(unredirected_link)
                html = await response.text()
                html_parse = BeautifulSoup(html, "html.parser")
                link = html_parse.find("a")["href"]
                print("response")

                # link = redirectFromUrl(unredirected_link)

                entries[i]["link"] = link
                if "miamiherald" in link: continue
                print(f"URL {entries[i]["link"]}")

                # use redirect response
                print("request redirected")
                response = await session.get(link)
                print("respond redirected")
                
                print("scraping image")
                html = await response.text()
                html_parse = BeautifulSoup(html, "html.parser")

                img_meta = html_parse.find("meta", {"property": "og:image"})

                if img_meta:
                    entries[i]["urlToImage"] = img_meta["content"]
                else:
                    entries[i]["urlToImage"] = None
                print("image scraped")

                # img = html_parse.find("img")
                
                # if img:
                #     attrs = img.attrs

                #     if "src" in attrs: entries[i]["urlToImage"] = attrs["src"]
                #     elif "srcset" in attrs:
                #         src_set = attrs["srcset"]
                #         src_item = src_set.split(",")[0]
                #         src = src_item.split()[0]
                        
                #         entries[i]["urlToImage"] = src
                #     else:
                #         entries[i]["urlToImage"] = "https://i0.wp.com/midpenpost.org/wp-content/uploads/2023/10/DSC_5063-2.png?fit=768%2C509&ssl=1"
                # else:
                #     entries[i]["urlToImage"] = "https://i0.wp.com/midpenpost.org/wp-content/uploads/2023/10/DSC_5063-2.png?fit=768%2C509&ssl=1"

                # display progress bar
                os.system("clear")
                progress_amt = round((i + 1) / count * 25)
                print(f"Loading headlines... {int((i + 1) / count * 100)}%\n" + "▓" * progress_amt + "░" * (25 - progress_amt))
                print("Finished!")

            self.cache = new_headlines

    async def interval(self):
        while True:
            await asyncio.sleep(60 * 15)
            await setTopHeadlines(self)

    def startInterval(self):
        print("Interval started")
        asyncio.run(interval())