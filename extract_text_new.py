from urllib import request
from html.parser import HTMLParser
import re
import spacy

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.inside_body_tag = False
        self.skip_tag = False
        self.tag_stack = []
        self.nlp = spacy.load("en_core_web_sm")
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.url_pattern = re.compile(r'^(?:https?://|www\.)\S+\.[a-zA-Z]{2,}(?:[/?#]\S*)?$')
        self.date_patterns = ["\d{1,2}\/\d{1,2}\/\d{4}", "\d{1,2}-\d{1,2}-d{4}"]
        self.text = ''
        
    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.inside_body_tag = True
        self.tag_stack.append(tag)
        if tag in ["script", "style", "label", "option", "button", "textarea", "iframe"]:
            self.skip_tag = True

    def handle_endtag(self, tag):
        if tag == "body":
            self.inside_body_tag = False
        if tag in ["script", "style", "label", "option", "button", "textarea", "iframe"]:
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
        if message:
            print(message)

# Fetch the URL and pass the HTML content to the parser

url = "https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam"
response = request.urlopen(url)
html_content = response.read().decode('utf-8')

parser = MyHTMLParser()
print("[Parsing HTML content...]")
print()
parser.feed(html_content)
print("[Done parsing HTML content.]")
print()
print(parser.text)

# https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam
# https://hikouki0408.github.io/portfolio 