import spacy
from pattern.text.en import singularize
import os

# python -m spacy download en_core_web_sm
nlp = None
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

allowed_tags = {"NN", "NNP", "NNS", "NNPS"} # "in" in sets is O(1)

def processData():
    filename = "political_news_titles.txt"
    document = nlp(open(filename, "r").read())

    political_terms = {}

    for chunk in document.noun_chunks:
        pos = chunk.root.pos_
        term = chunk.root.text.lower()

        if chunk.root.tag_ == "NNS" or chunk.root.tag_ == "NNPS": # If token is plural
            term = singularize(term)

        if term in political_terms:
            political_terms[term] += 1
        else:
            political_terms[term] = 1

        # print(f"=================\nT: {chunk.text}\nRT: {chunk.root.text}\nHT: {chunk.root.head.text}")
        # print(f"RTD: {chunk.root.text.dep_}")
    
    political_terms = dict(sorted(political_terms.items(), key=lambda item: item[1], reverse=True))
    filtered_political_terms = set([])

    for term in political_terms:
        if political_terms[term] <= 3: break
        
        filtered_political_terms.add(term)

    return filtered_political_terms

political_terms = processData()
# print(political_terms)

def politicalIndex(original_title):
    document = nlp(original_title)

    index = 0

    for chunk in document.noun_chunks:
        pos = chunk.root.pos_
        term = chunk.root.text.lower()

        if chunk.root.tag_ == "NNS" or chunk.root.tag_ == "NNPS": # If token is plural
            term = singularize(term)

        #print(term + " ", end="")

        if term in political_terms:
            index += 1

    #print()

    return index

def isPolitical(original_title):
    return politicalIndex(original_title) > 0

test_headlines = [
    "Jay Thapar was arrested for smuggling cocaine off the Mexican-American border",
    "McDonald’s says Israel boycotts are hurting its business - The Hill",
    "Senegal on the brink after elections postponed - BBC.com",
    "Bipartisan border deal on brink of defeat ahead of key Senate vote - CNN", # should be marked political but isn't
    "Taylor Swift Shares Tracklist for ‘The Tortured Poets Department’ With Features From Post Malone and Florence + Machine - Variety",
    "Top 10 reasons why Taylor Swift is fucking overrated and should not have won the grammies idk",
    "Gaza ceasefire: Israel's PM Benjamin Netanyahu rejects Hamas's proposed terms - BBC.com",
    "Snoop Dogg and Master P sue Walmart over cereal sabotage claim - BBC.com",
    "AG says special counsel has finished probe into Biden's handling of classified docs - ABC News",
    "Tracking all the NBA trades leading up to Thursday's deadline - Yahoo Sports",
    "Parents seek justice for baby who died after his neck was broken during delivery at a Georgia hospital - CNN",
    "Broken Congress: It can't fix the border, fund allies or impeach Mayorkas as GOP revolts. - The Associated Press",
    "Nevada: Nikki Haley got trapped by Donald Trump supporters. What now? - USA TODAY", # should be marked political but isn't
    "Albania conducts a crackdown on idiots or something",
    "Jay Thapar caught listening to Taylor Swift",
    "Jay Thapar is caught doing drugs",
    "Donald Trump finds out he is 0.7% black, claims it gives him an N-word pass", # should be marked political but isn't
    "The United Nations commends North Korea after they destroy Asia",
    "Snoop Dogg gets boycotted after he accidentally slipped on a banan",
    "Racism expert warns everyone 'racism is bad'",
    "'Everyone makes mistakes,' says Biden after accidentally leaking nuclear codes", # should be marked political but isn't
    "Spongebob Squarepants found on Epstein island list", # should be marked political but isn't
    "The US invades Washington DC after oil was discovered there", # should be marked political but isn't
    "Florida man climbs atop playground equipment at Clearwater park, tells kids where babies come from",
    "Senator accidentally sleeps with 93 men" # should be marked political but isn't
]

# for headline in test_headlines:
#     if isPolitical(headline):
#         print(headline)