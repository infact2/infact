import scraper
import urllib
from bs4 import BeautifulSoup

base = "https://www.allsides.com"
html = scraper.scrape("https://www.allsides.com/media-bias/ratings?field_featured_bias_rating_value=1&field_news_source_type_tid%5B%5D=2&field_news_source_type_tid%5B%5D=3&field_news_source_type_tid%5B%5D=4&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&title=")
html_parse = BeautifulSoup(html, "html.parser")

# with open("yo_ignore_this", "w") as file:
#     # Write the string to the file
#     BAAAAAA = scraper.scrape("https://www.allsides.com/news-source/abc-news-media-bias")
#     file.write(BAAAAAA.read().decode("utf-8"))

# print("DOING")


# search for all with "views-field-title" class
# please ignore ones with text "News Source" tho lol
elements = html_parse.find_all("td", class_="views-field-title")

to_write = {}

# Print the found elements
for element in elements:
    name = element.get_text().replace('\n', '')[0:-1]
    scrape_url = element.find("a")["href"]

    if "opinion" in name.lower(): continue # opinion urls create issues for finding articles, omit them

    # find leaning
    cur_html = scraper.scrape(base + scrape_url)
    cur_html_parse = BeautifulSoup(cur_html, "html.parser")
    leaning = cur_html_parse.find(class_="numerical-bias-rating").get_text()
    # this usually means that the rating is not agreed upon, so omit
    if leaning == "": continue
    previously_website = False
    url = ""
    for item in cur_html_parse.find("tbody").find_all("td"):
        if previously_website:
            url = item.find("a")["href"]
            break
        previously_website = item.get_text() == "Website"

    print(f"{name} : {url} : {leaning}")

    if leaning in to_write: to_write[leaning].append({"name": name, "url": url})
    else: to_write[leaning] = [{"name": name, "url": url}]

print(to_write)