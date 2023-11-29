import urllib.request  
from bs4 import BeautifulSoup 

# url = "https://www.foxnews.com/world/hamas-releases-more-israeli-hostages-6th-day-cease-fire"
# url = "https://www.newsmax.com/us/joe-biden-impeachment-house/2023/11/29/id/1144091/"
url = "https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html"
omitted_paragraph_keywords = ["all rights reserved", "subscribe", "newsletter", "@"]

html = urllib.request.urlopen(url) 
htmlParse = BeautifulSoup(html, "html.parser") 

for para in htmlParse.find_all("p"): 
    text = para.get_text()
    text_lower = text.lower()
    
    omit = False
    for word in omitted_paragraph_keywords:
        if word in text_lower:
            omit = True
            break
    
    if omit: continue

    print("    " + text)