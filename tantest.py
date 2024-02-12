import requests

def getDaLinks(prompt):
       print("Given Promt: " + prompt + "\n")
       
       
       prompt += "&"
       apiKey = AIzaSyDqabrP5CbkUciLP9nr4o_9XKDtNiwp5hs 
       searchEngineID = d6c2539d1fec44866 #cx
       page = 1 # using the first page
       start = (page - 1) * 10 + 1 # calculating start, (page=2) => (start=11), (page=3) => (start=21)


       url = 'https://www.googleapis.com/customsearch/v1?key={apiKey}&cx={searchEngineID}&q={prompt}&start={start}'

       parameters = {
              'cx': "d6c2539d1fec44866",
              'q': prompt,
              'sortBy': 'popularity&',
              'language': 'en',
              'from': '2023-01-01&',
              'pageSize': 5,
              'apiKey': 'AIzaSyDqabrP5CbkUciLP9nr4o_9XKDtNiwp5hs'
       }

       response = requests.get(url).json()

       # get the result items
       search_items = data.get("items")
       # iterate over 10 results found
       for i, search_item in enumerate(search_items, start=1):
              try:
                     long_description = search_item["pagemap"]["metatags"][0]["og:description"]
              except KeyError:
                     long_description = "N/A"
              # get the page title
              title = search_item.get("title")
              # page snippet
              snippet = search_item.get("snippet")
              # alternatively, you can get the HTML snippet (bolded keywords)
              html_snippet = search_item.get("htmlSnippet")
              # extract the page url
              link = search_item.get("link")
              # print the results
              print("="*10, f"Result #{i+start-1}", "="*10)
              print("Title:", title)
              print("Description:", snippet)
              print("Long description:", long_description)
              print("URL:", link, "\n")

getDaLinks("poopoo")

#getLinks(["San", "Diego", "homeless"])
#test push 3