import scraper
import urllib
from bs4 import BeautifulSoup
from sourcenamehandler import handleSourceName
import json
import csv

base = "https://www.allsides.com"
# html = scraper.scrape("https://raw.githubusercontent.com/favstats/AllSideR/master/data/allsides_data.csv")
# html_parse = BeautifulSoup(html, "html.parser")

# with open("yo_ignore_this", "w") as file:
#     # Write the string to the file
#     BAAAAAA = scraper.scrape("https://www.allsides.com/news-source/abc-news-media-bias")
#     file.write(BAAAAAA.read().decode("utf-8"))

# print("DOING")


# search for all with "views-field-title" class
# please ignore ones with text "News Source" tho lol
# elements = html_parse.find_all("td", class_="views-field-title")
generalized_bias = {
    "1": "-4.50",
    "2": "-2.00",
    "3": "0.00",
    "4": "2.00",
    "5": "4.50"
}

# print(html.read())

to_write = {}
banned_site_names = ["Prager University", "Google News", "InfoWars", "Yahoo! News", "Wall Street Journal - Editorial"]

with open("allsides_data.csv", mode="r") as file:
    elements = csv.reader(file)

    # Print the found elements
    for element in elements:
        name = element[0]
        url = element[7]
        confidence = element[12]
        if name in banned_site_names: continue
        if confidence != "High" and confidence != "Medium": continue
        raw_rating = str(element[2])
        if raw_rating == "NA": continue
        
        leaning = generalized_bias[raw_rating]

        if "opinion" in name.lower(): continue # opinion urls create issues for finding articles, omit them

        # find leaning
        cur_html = scraper.scrape(url)
        cur_html_parse = BeautifulSoup(cur_html, "html.parser")
        # leaning = cur_html_parse.find(class_="numerical-bias-rating").get_text()
        # # this usually means that the rating is not agreed upon, so omit
        # if leaning == "": continue

        previously_website = False
        url = ""
        for item in cur_html_parse.find("tbody").find_all("td"):
            if previously_website:
                url = item.find("a")["href"]
                break
            previously_website = item.get_text() == "Website"

        if url == "": continue
        if "linkedin" in url: continue

        print(f"{name} : {url} : {leaning}")

        if leaning in to_write:
            to_write[leaning].append({"name": name, "url": url, "newsapi": handleSourceName(name)})
        else:
            to_write[leaning] = [{"name": name, "url": url, "newsapi": handleSourceName(name)}]

    # print(to_write)
    print("writing...")
    with open("media_bias.json", "w") as file:
        file.write(json.dumps(to_write, indent=4))

    print("written!")