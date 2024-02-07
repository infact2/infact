import spacy
import os

# python -m spacy download en_core_web_sm
nlp = None
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

for chunk in nlp("i love the senate").noun_chunks:
    print(f"{chunk.root.text} {chunk.root.pos_}")

def processData():
    filename = "political_news_titles.txt"
    document = nlp(open(filename, "r").read())

    political_terms = {}

    for chunk in document.noun_chunks:
        pos = chunk.root.pos_
        term = chunk.root.text.lower()
        #if pos != "NOUN": continue # We don't count proper nouns, those change over time

        if term in political_terms:
            political_terms[term] += 1
        else:
            political_terms[term] = 1

        # print(f"=================\nT: {chunk.text}\nRT: {chunk.root.text}\nHT: {chunk.root.head.text}")
        # print(f"RTD: {chunk.root.text.dep_}")
    
    political_terms = dict(sorted(political_terms.items(), key=lambda item: item[1], reverse=True))
    filtered_political_terms = {"total": 0, "terms": {}}

    for term in political_terms:
        if political_terms[term] <= 3: break
        
        filtered_political_terms["terms"][term] = political_terms[term]
        filtered_political_terms["total"] += political_terms[term]

    return filtered_political_terms

political_terms = processData()
print(political_terms)

def politicalIndex(original_title):
    document = nlp(original_title)

    index = 0

    for chunk in document.noun_chunks:
        pos = chunk.root.pos_
        term = chunk.root.text.lower()

        #if pos != "NOUN": continue # We don't count proper nouns, those change over time

        if term in political_terms["terms"]:
            index += political_terms["terms"][term]

    index /= political_terms["total"]

    return index

print(politicalIndex("Jay Thapar was arrested for smuggling cocaine off the Mexican-American border"))
print(politicalIndex("McDonald’s says Israel boycotts are hurting its business - The Hill"))
print(politicalIndex("Senegal on the brink after elections postponed - BBC.com"))
print(politicalIndex("Bipartisan border deal on brink of defeat ahead of key Senate vote - CNN"))
print(politicalIndex("Taylor Swift Shares Tracklist for ‘The Tortured Poets Department’ With Features From Post Malone and Florence + Machine - Variety"))
print(politicalIndex("Top 10 reasons why Taylor Swift is fucking overrated and should not have won the grammies idk"))
print(politicalIndex("The government claims the earth is flat"))
