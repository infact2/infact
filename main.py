import urllib.request
from flask import Flask, request, send_file, render_template, jsonify
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI
import asyncio
import base64
import json
from scraper import DANGEROUS

from corroborate import corroborate

import users
from headlines import Headlines

print("Starting...")

load_dotenv()
client = OpenAI()
_headlines = Headlines()
hdr = {'User-Agent': 'Mozilla/5.0'}

# defaults = {
#     'model': 'models/text-bison-001',
#     'temperature': 0.7,
#     'candidate_count': 1,
#     'top_k': 40,
#     'top_p': 0.95,
#     'max_output_tokens': 1024,
#     'stop_sequences': [],
#     'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":"BLOCK_LOW_AND_ABOVE"},  {"category":"HARM_CATEGORY_TOXICITY","threshold":"BLOCK_LOW_AND_ABOVE"},{"category":"HARM_CATEGORY_VIOLENCE",  "threshold":"BLOCK_MEDIUM_AND_ABOVE"},{"category":"HARM_CATEGORY_SEXUAL","threshold":"BLOCK_MEDIUM_AND_ABOVE"},  {"category":"HARM_CATEGORY_MEDICAL","threshold":"BLOCK_MEDIUM_AND_ABOVE"},  {"category":"HARM_CATEGORY_DANGEROUS","threshold":"BLOCK_MEDIUM_AND_ABOVE"}],
# }

# url = "https://www.foxnews.com/world/hamas-releases-more-israeli-hostages-6th-day-cease-fire"
# url = "https://www.newsmax.com/us/joe-biden-impeachment-house/2023/11/29/id/1144091/"
# url = "https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html"

omitted_paragraph_keywords = ["all rights reserved", "subscribe", "newsletter", "@", "©", "(c)", "advertis", "cookie", "newsmax", "registered trademark"]

margin = 2

# def extractText(url):
#     html = urllib.request.urlopen(urllib.request.Request(url, headers=hdr))
#     html_parse = BeautifulSoup(html, "html.parser")
    
#     text = ""
#     for para in html_parse.find_all("p"): 
#         para_text = para.get_text()
#         para_text_lower = para_text.lower()
        
#         # Omit paragraphs with certain keywords
#         omit = False
#         for word in omitted_paragraph_keywords:
#             if word in para_text_lower:
#                 omit = True
#                 break
        
#         if omit: continue
#         text += para_text + "[NEWPARA]"
    
#     # Remove excess newlines
#     text = text.replace("\n", "").replace("[NEWPARA]", "\n\n")
#     # print(text)

#     return text

def textToHTML(text):
    return text.replace("\n", "<br/>")

def decode(encoded):
    return base64.b64decode(encoded.encode("ascii")).decode("ascii")


#print(extractText("https://abcnews.go.com/US/fbi-investigating-south-carolina-couple-accused-harassing-neighbors/story?id=105825286"))
# corroborate("https://www.newsmax.com/us/joe-biden-impeachment-house/2023/11/29/id/1144091/", "https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html")




# ==========================================================

# ROUTING SHENANIGANS

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
async def index():
    return send_file("static/index.html")

@app.route("/signup/<redirect>")
async def signup(redirect):
    return render_template("signup.html", redirect=decode(redirect), redirect_raw=redirect)

@app.route("/login/<redirect>")
async def login(redirect):
    return render_template("login.html", redirect=decode(redirect), redirect_raw=redirect)

@app.route("/dashboard")
async def dashboard():
    return send_file("static/dashboard.html")

@app.route("/information")
async def information():
    return send_file("static/information.html")

@app.route("/corroborate/<url_encoded>/<settings_json_encoded>")
async def _corroborate(url_encoded, settings_json_encoded):
    print("Corroborating...")
    url1 = decode(url_encoded)
    settings = json.loads(decode(settings_json_encoded))
    
    raw_content = await corroborate(url1)
    if raw_content == DANGEROUS:
        print(f"NUH UH ({url1})")
        return send_file("static/stop.html")
        
    print("Done corroborating.")

    # remove ALL html
    raw_content["content"] = raw_content["content"].replace("<", "").replace(">", "")
    # readd paragraph elements
    raw_content["content"] = raw_content["content"].replace("[p]", "<p>").replace("[/p]", "</p>")
    raw_content["content"] = raw_content["content"].replace("[q]", "<span class='quote'>").replace("[/q]", "</span>")
    # add source links lol
    raw_content["content"] = raw_content["content"].replace("[SOURCE 1]", f"<a class='source-note' href='{url1}'>[1]</a>").replace("[SOURCE 2]", f"<a class='source-note' href='{raw_content["url2"]}'>[2]</a>")

    return render_template("corroborate.html",
        title=raw_content["title"], url1=url1, url2=raw_content["url2"], source1=raw_content["source1"], source2=raw_content["source2"], content=raw_content["content"],
        
        total_sites=raw_content["total_sites"], sites_scraped=raw_content["sites_scraped"], sites_unscrapable=raw_content["sites_unscrapable"], sites_omitted=raw_content["sites_omitted"], execution_time=raw_content["execution_time"], helper_time=raw_content["helper_time"])

@app.route("/isitdown")
async def ping():
    return "<h1>No.</h1>"

@app.route("/gimme", methods=["POST", "GET"])
async def gimme():
    data = _headlines.getTopHeadlines()
    print(type(data))
    # print(data)

    # print(data)

    # print("==============\n\n\n")
    # print(response.json())
    # print("==============\n\n\n")

    return jsonify(data)

@app.route("/getuserdata/<username_encoded>/<password_encoded>", methods=["POST", "GET"])
async def getUserData(username_encoded, password_encoded):
    data = users.authenticate(decode(username_encoded), decode(password_encoded))
    print(data)
    return jsonify(data)

@app.route("/createaccount/<username_encoded>/<password_encoded>", methods=["POST", "GET"])
async def createAccount(username_encoded, password_encoded):
    data = users.createAccount(decode(username_encoded), decode(password_encoded))
    print(data)
    return jsonify(data)

@app.route("/savearticle/<username_encoded>/<password_encoded>/<id>/<title_encoded>", methods=["POST", "GET"])
async def saveArticle(username_encoded, password_encoded, id, title_encoded):
    data = users.saveArticle(decode(username_encoded), decode(password_encoded), id, decode(title_encoded))
    print("ARTIFCLE SAVED")
    print(data)
    return jsonify(data)

@app.route("/<path>")
async def _path(path):
    try:
        return send_file(f"static/{path}")
    except:
        pass
    return send_file(f"static/404.html")

@app.errorhandler(404)
async def error404(event):
    return send_file("static/404.html")

@app.errorhandler(500)
async def error500(event):
    return send_file("static/500.html")

if __name__ == '__main__':
#    app.run(debug = True)
    async def load():
        from waitress import serve
        _headlines.setTopHeadlines()
        print("Running...")
        serve(app, host="0.0.0.0", port=8000)
    asyncio.run(load())
    _headlines.startInterval()
