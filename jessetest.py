import requests
import threading
import asyncio
import aiohttp
import base64


async def hehe():
    async with aiohttp.ClientSession() as session:
        response = await session.get("https://news.google.com/rss/articles/CBMiLWh0dHBzOi8vd3d3LmJiYy5jb20vbmV3cy91ay1wb2xpdGljcy02ODYxODU3MNIBMWh0dHBzOi8vd3d3LmJiYy5jb20vbmV3cy91ay1wb2xpdGljcy02ODYxODU3MC5hbXA?oc=5&hl=en-US&gl=US&ceid=US:en", allow_redirects=True)        

#asyncio.run(hehe())

unredirected_link = "https://www.reuters.com/world/middle-east/israeli-military-says-it-killed-90-gunmen-gazas-al-shifa-hospital-2024-03-20/"
hash = unredirected_link.split("/")[5].split("?")[0] + "=="
print(hash)
print(type(hash))
print(base64.b64decode(hash).split(b"\x011")[1].decode())
#.split("")

print("test")