from urllib import request
from html.parser import HTMLParser
import re
from pycorenlp import StanfordCoreNLP
import time
import json
import sys

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.inside_body_tag = False
        self.skip_tag = False
        self.tag_stack = []
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.url_pattern = re.compile(r'^(?:https?://|www\.)\S+\.[a-zA-Z]{2,}(?:[/?#]\S*)?$')
        self.date_patterns = ["\d{1,2}\/\d{1,2}\/\d{4}", "\d{1,2}-\d{1,2}-d{4}"]
        self.text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.inside_body_tag = True
        self.tag_stack.append(tag)
        if tag in ["script", "style", "image", "iframe", "button", "label", "nav", "footer"]:
            self.skip_tag = True

    def handle_endtag(self, tag):
        if tag == "body":
            self.inside_body_tag = False
        if tag in ["script", "style", "image", "iframe", "button", "label", "nav", "footer"]:
            self.skip_tag = False
        self.tag_stack.pop()

    def handle_data(self, data):
        message = ''
        label = "undefined"
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
                    label = "Puretext"
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                    self.text += (data.strip() + " ")

    def extract_relations_from_text(self,text):
        nlp = StanfordCoreNLP('http://localhost:9000')
        output = nlp.annotate(text, properties={
            'annotators': 'openie',
            'outputFormat': 'json',
            'openie.triple.strict': 'true',
            'openie.max_entailments_per_clause': '1'
        })
        # Extract and print the relations
        counter = 1
        for sentence in output['sentences']:
            for triple in sentence['openie']:
                subject = triple['subject']
                relation = triple['relation']
                obj = triple['object']
                print(f"{counter}. Subject: {subject}, Relation: {relation}, Object: {obj}")
                counter += 1
           


    
# Fetch the URL and pass the HTML content to the parser
url = "https://stackoverflow.blog/2023/05/31/ceo-update-paving-the-road-forward-with-ai-and-community-at-the-center"
response = request.urlopen(url)
html_content = response.read().decode('utf-8')
parser = MyHTMLParser()
parser.feed(html_content)
parser.extract_relations_from_text(parser.text)




# 1. https://hikouki0408.github.io/portfolio 
# 2. https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam
# 3. https://www.bbc.com/news/world-europe-66122743
# 4. https://stackoverflow.blog/2023/05/31/ceo-update-paving-the-road-forward-with-ai-and-community-at-the-center/
# 5. 



