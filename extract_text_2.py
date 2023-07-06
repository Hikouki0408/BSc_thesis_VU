import urllib.request
from html.parser import HTMLParser
import re
import spacy
import json

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_body_tag = False
        self.skip_tag = False
        self.tag_stack = []
        self.nlp = spacy.load("en_core_web_sm") # loads a pre-trained English language model 
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.url_pattern = re.compile(r'^(?:https?://|www\.)\S+\.[a-zA-Z]{2,}(?:[/?#]\S*)?$')
        self.date_patterns = ["\d{1,2}\/\d{1,2}\/\d{4}", "\d{1,2}-\d{1,2}-d{4}"]
        self.puretext_list = []

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.inside_body_tag = True
        self.tag_stack.append(tag)
        if tag in ["style", "script", "img", "iframe", "br","button", "title", "label"]:
            self.skip_tag = True

    def handle_endtag(self, tag):
        if tag == "body":
            self.inside_body_tag = False
        if tag in ["style", "script", "img", "iframe", "br","button", "title", "label"]:
            self.skip_tag = False
        self.tag_stack.pop()

    def handle_data(self, data):
        message = ''
        if self.inside_body_tag:
            if not self.skip_tag and data.strip():
                tag = self.tag_stack[-1] if self.tag_stack else None 
                if re.search(self.email_pattern, data) and not any(char.isspace() for char in data.strip()):
                    label = "Email"
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                elif re.search(self.url_pattern, data) and not any(char.isspace() for char in data.strip()):
                    label = "Website"
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                elif not re.search(r'[a-zA-Z0-9]', data):
                    label = "Non-contextual"
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                else:
                    doc = self.nlp(data.strip())
                    named_entities = []
                    for ent in doc.ents:
                        if ent.label_ in ["PERSON", "GPE", "LANGUAGE", "TIME", "PERCENT", "ORG", "PRODUCT", "EVENT"]:
                            named_entities.append(ent.text)
                        elif ent.label_ == "DATE" and any(char.isdigit() for char in ent.text) and len(ent.text) < 20:
                            named_entities.append(ent.text)    
                    label = "Puretext"
                    if len(data.strip().split()) > 2:
                            self.puretext_list.append(data.strip())
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
            
    def extract_relations(self):
        puretext = self.puretext_list
        extracted_data = []
        for text in puretext:
            doc = self.nlp(text)
            relationships = []

            for token in doc:
                # NER Pattern 1: PERSON [verb] ORG
                if token.ent_type_ == 'PERSON' and token.head.pos_ == 'VERB' and token.head.ent_type_ == 'ORG':
                    entity1 = token.text
                    entity2 = token.head.text
                    relationships.append((entity1, 'verb', entity2, 'NER Pattern 1'))

                # NER Pattern 2: GPE [preposition] LANGUAGE
                if token.ent_type_ == 'GPE' and token.head.pos_ == 'ADP' and token.head.ent_type_ == 'LANGUAGE':
                    entity1 = token.text
                    entity2 = token.head.text
                    relationships.append((entity1, token.head.text, entity2, 'NER Pattern 2'))

                # Pattern 1: Entity1 [preposition] Entity2
                if token.dep_ in ('prep', 'agent'):
                    entity1 = token.head.text
                    entity2 = token.text
                    relationships.append((entity1, 'prep', entity2, 'Pattern 1'))

                # Pattern 2: Entity1 [verb] Entity2
                if token.dep_ == 'dobj' and token.head.pos_ == 'VERB':
                    entity1 = token.head.text
                    entity2 = token.text
                    relationships.append((entity1, 'verb', entity2, 'Pattern 2'))

                # Pattern 3: Entity1 [appos] Entity2
                if token.dep_ == 'appos':
                    entity1 = token.head.text
                    entity2 = token.text
                    relationships.append((entity1, 'appos', entity2, 'Pattern 3'))

                # Pattern 4: Entity1 [poss] Entity2
                if token.dep_ == 'poss':
                    entity1 = token.head.text            
                    entity2 = token.text
                    relationships.append((entity1, 'poss', entity2, 'Pattern 4'))

                # Pattern 5: Entity1 [amod] Entity2
                if token.dep_ == 'amod':
                    entity1 = token.head.text
                    entity2 = token.text
                    relationships.append((entity1, 'amod', entity2, 'Pattern 5'))
                
                # Pattern 6: Entity1 [preposition] Entity2 [preposition] Entity3
                if token.dep_ in ('prep', 'agent'):
                    entity1 = token.head.text
                    entity2 = token.text
                    entity3 = ' '.join([t.text for t in token.head.children if t.dep_ == 'pobj'])
                    if entity2 and entity3:
                        relationships.append((entity1, token.text, entity2, token.head.text, entity3, 'Pattern 6'))

                # Pattern 7: Entity1 [verb] Entity2 [preposition] Entity3
                if token.dep_ == 'dobj' and token.head.pos_ == 'VERB':
                    entity1 = token.head.text
                    entity2 = token.text
                    entity3 = ' '.join([t.text for t in token.children if t.dep_ == 'pobj'])
                    if entity2 and entity3:
                        relationships.append((entity1, token.text, entity2, token.head.text, entity3, 'Pattern 7'))

            if relationships:
                extracted_data.append({
                "Text": text,
                "Relations": [str(relation) for relation in relationships]
            })

        with open('dataset_NYT.json', 'w') as json_file:
            json.dump(extracted_data, json_file, indent=4)


# 1. https://hikouki0408.github.io/portfolio 
# 2. https://vu.nl/nl
# 3. https://en.wikipedia.org/wiki/Main_Page
# 4. https://www.nytimes.com/
# 5. https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam

response = urllib.request.urlopen('https://www.nytimes.com/')
parser = MyHTMLParser()
parser.feed(response.read().decode('utf-8'))

# Print all the texts classified as Puretext in a numbered list
for i, text in enumerate(parser.puretext_list):
    print(f"{i+1}. {text}")
print()
print("start extracting relations()")
print()
parser.extract_relations()
