import urllib.request
import re
import random
import spacy
from bs4 import BeautifulSoup
import google.generativeai as genai

genai.configure(api_key="AIzaSyAgJK_XqImu5ulw2raEasMllxiCSC-MsiY")

defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.7,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
    'stop_sequences': [],
    'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":"BLOCK_LOW_AND_ABOVE"},  {"category":"HARM_CATEGORY_TOXICITY","threshold":"BLOCK_LOW_AND_ABOVE"},{"category":"HARM_CATEGORY_VIOLENCE",  "threshold":"BLOCK_MEDIUM_AND_ABOVE"},{"category":"HARM_CATEGORY_SEXUAL","threshold":"BLOCK_MEDIUM_AND_ABOVE"},  {"category":"HARM_CATEGORY_MEDICAL","threshold":"BLOCK_MEDIUM_AND_ABOVE"},  {"category":"HARM_CATEGORY_DANGEROUS","threshold":"BLOCK_MEDIUM_AND_ABOVE"}],
}

# url = "https://www.foxnews.com/world/hamas-releases-more-israeli-hostages-6th-day-cease-fire"
# url = "https://www.newsmax.com/us/joe-biden-impeachment-house/2023/11/29/id/1144091/"
# url = "https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html"

omitted_paragraph_keywords = ["all rights reserved", "subscribe", "newsletter", "@", "©", "(c)", "advertis", "cookie", "newsmax", "registered trademark"]

margin = 2

def extractText(url):
    html = urllib.request.urlopen(url) 
    html_parse = BeautifulSoup(html, "html.parser")
    
    text = ""
    for para in html_parse.find_all("p"): 
        para_text = para.get_text()
        para_text_lower = para_text.lower()
        
        # Omit paragraphs with certain keywords
        omit = False
        for word in omitted_paragraph_keywords:
            if word in para_text_lower:
                omit = True
                break
        
        if omit: continue
        text += para_text + "[NEWPARA]"
    
    # Remove excess newlines
    text = text.replace("\n", "").replace("[NEWPARA]", "\n\n")
    # print(text)

    return text


def corroborate(url1, url2):
    prompt = f"summarize these two passages into a single news report:\n\"{extractText(url1)}\"\n\"{extractText(url2)}\""
    print(prompt)
    # print(f"{prompt}\n=============\n\n")
    response = genai.generate_text(
        **defaults,
        prompt=prompt
    )

    # print(response.result)


# print(extractText("https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html"))
corroborate("https://www.newsmax.com/us/joe-biden-impeachment-house/2023/11/29/id/1144091/", "https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html")