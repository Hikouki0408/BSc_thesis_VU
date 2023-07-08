import urllib.request
from html.parser import HTMLParser
import re
import spacy

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_body_tag = False
        self.skip_tag = False
        self.tag_stack = []
        self.data_by_label = {}
        self.nlp = spacy.load("en_core_web_sm") # loads a pre-trained English language model 
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.url_pattern = re.compile(r'^(?:https?://|www\.)\S+\.[a-zA-Z]{2,}(?:[/?#]\S*)?$')
        self.date_patterns = ["\d{1,2}\/\d{1,2}\/\d{4}", "\d{1,2}-\d{1,2}-d{4}"]
        self.count = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.inside_body_tag = True
        self.tag_stack.append(tag)
        if tag in ["script", "style", "image", "iframe", "br", "button", "title", "label"]:
            self.skip_tag = True

    def handle_endtag(self, tag):
        if tag == "body":
            self.inside_body_tag = False
        if tag in ["script", "style", "image", "iframe", "br", "button", "title", "label"]:
            self.skip_tag = False
        self.tag_stack.pop()

    def handle_data(self, data):
        message = ''
        label = "Puretext"
        if self.inside_body_tag:
            if not self.skip_tag and data.strip():
                # returns the last tag in the list
                tag = self.tag_stack[-1] if self.tag_stack else None 
                if re.search(self.email_pattern, data) and not any(char.isspace() for char in data.strip()):
                    label = "Email"
                    if label not in self.data_by_label:
                        self.data_by_label[label] = []
                    self.data_by_label[label].append(data.strip())
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                elif re.search(self.url_pattern, data) and not any(char.isspace() for char in data.strip()):
                    label = "Website"
                    if label not in self.data_by_label:
                        self.data_by_label[label] = []
                    self.data_by_label[label].append(data.strip())
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                elif not re.search(r'[a-zA-Z0-9]', data):
                    label = "Non-contextual"
                    if label not in self.data_by_label:
                        self.data_by_label[label] = []
                    self.data_by_label[label].append(data.strip())
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                else:
                    doc = self.nlp(data.strip())
                    named_entities = []
                    for ent in doc.ents:
                        if ent.label_ in ["PERSON", "GPE", "LANGUAGE", "TIME", "PERCENT", "ORG", "PRODUCT", "EVENT"]:
                            named_entities.append(ent.text)
                        elif ent.label_ == "DATE" and any(char.isdigit() for char in ent.text) and len(ent.text) < 20:
                            named_entities.append(ent.text)    
                    if named_entities:
                        if label not in self.data_by_label:
                            self.data_by_label[label] = []
                        self.data_by_label[label].append(data.strip())
                        message = f"{label}: [{data.strip()}], Labels:[{', '.join([ent.label_ for ent in doc.ents if ent.text in named_entities])}] {', '.join(named_entities)} (tag: {tag})"
                        self.count += 1
                        for ent in doc.ents:
                            if ent.text in named_entities:
                                if ent.label_ not in self.data_by_label:
                                    self.data_by_label[ent.label_] = []
                                self.data_by_label[ent.label_].append(ent.text)
                    else:
                        if label not in self.data_by_label:
                            self.data_by_label[label] = []
                        self.data_by_label[label].append(data.strip())
                        message = f"{label}: [{data.strip()}] (tag: {tag})"
                        self.count += 1
        if message:
            print(message)


    def print_data_by_label(self):
        for label, data in self.data_by_label.items():
            if label != "Puretext":
                print(f"Data for label '{label}': ", end="")
                for i, datum in enumerate(data):
                    if i == len(data) - 1:
                        print(datum)
                    else:
                        print(datum, end=", ") 

response = urllib.request.urlopen('https://www.gutenberg.org/cache/epub/32498/pg32498-images.html')
parser = MyHTMLParser()
print("[Parsing HTML file...]")
print()
parser.feed(response.read().decode('utf-8'))
print("[Done parsing HTML file.]")
print()
parser.print_data_by_label()
print("[Done printing data by label.]")


"""
potential unrelated tags so far: if tag in ["script", "style", "label", "option", "button", "textarea"]:
https://hikouki0408.github.io/portfolio
https://www.cntraveller.com/gallery/beautiful-places-amsterdam
add more....
"""