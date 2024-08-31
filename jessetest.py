import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def isNewsOrganization(text):
    # Create a dummy text with the token
    doc = nlp(text)
    
    # Iterate through the recognized entities
    for ent in doc.ents:
        # Check if the entity is recognized as an ORG (organization)
        if ent.label_ == "ORG" and ent.text == text:
            return True
    
    return False

samples = [
    "CNN", "Peter Griffin News", "Breitbart News", "Bread", "FOX News", "Tucker Carlson", "Microsoft"
]
for i in samples:
    print(f"{i} -> {isNewsOrganization(i)}")