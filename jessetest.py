import requests
import threading
import asyncio
import aiohttp
import base64
from bs4 import BeautifulSoup


async def test():
    async with aiohttp.ClientSession() as session:
        response = await session.get("https://www.aljazeera.com/news/2024/3/27/most-americans-disapprove-of-israels-actions-in-gaza-poll", allow_redirects=True)

        html = await response.text()
        html_parse = BeautifulSoup(html, "html.parser")

        # print(html_parse.find("meta", {"property": "content"}))
        print([i["content"] for i in html_parse.findAll("meta")])

asyncio.run(test())

