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
        if tag in ["script", "style", "image", "iframe", "button", "title", "label", "nav", "footer"]:
            self.skip_tag = True

    def handle_endtag(self, tag):
        if tag == "body":
            self.inside_body_tag = False
        if tag in ["script", "style", "image", "iframe", "button", "title", "label", "nav", "footer"]:
            self.skip_tag = False
        self.tag_stack.pop()

    def handle_data(self, data):
        message = ''
        label = "undefined"
        if data.strip():
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

    def extract_relations_from_text(self, instances):
        nlp = StanfordCoreNLP('http://localhost:9000')
        text = self.text
        total_instances = len(instances)
        count_matched = 0
        count_unexpected = 0
        output = nlp.annotate(text, properties={
            'annotators': 'openie',
            'outputFormat': 'json',
            'openie.triple.strict': 'true',
            'openie.max_entailments_per_clause': '1'
        })
        
        # Extract and print the relations
        for sentence in output['sentences']:
            for triple in sentence['openie']:
                subject = triple['subject']
                relation = triple['relation']
                obj = triple['object']
                #print(f"Subject: {subject}, Relation: {relation}, Object: {obj}")
        """  
                
                match_found = False
                for instance in instances:
                    if subject == instance['Subject'] and relation == instance['Relation'] and obj == instance['Object']:
                        print("Match found in JSON file!")
                        count_matched += 1
                        match_found = True
                        break

                if not match_found:
                    count_unexpected += 1
        
        print(len(instances))
        print(count_matched)
        print(count_unexpected)
        TP = count_matched
        FN = total_instances - TP
        FP = count_unexpected
        print(FN)
        Precision = TP / (TP + FP)
        Recall = TP / (TP + FN)
        F1_Score = 2 * (Precision * Recall) / (Precision + Recall)
        print("Precision is ", Precision)
        print("Recall is ", Recall)
        print("F1_score is ",F1_Score)
        """
           
                
with open('Datasets/dataset_ebook.json', 'r') as file:
    json_data = json.load(file)
    
# Fetch the URL and pass the HTML content to the parser
url = "https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam"
response = request.urlopen(url)
html_content = response.read().decode('utf-8')
parser = MyHTMLParser()

start_time = time.time()
parser.feed(html_content)
runtime_time_1 = time.time()
runtime_text_extraction = runtime_time_1 - start_time
parser.extract_relations_from_text(json_data)
runtime_time_2 = time.time()
run_time = runtime_time_2 - start_time
print("Runtime_textExtraction: ", runtime_text_extraction, "seconds")
print("Runtime_total :", run_time, "seconds")
text_size = sys.getsizeof(parser.text)
print("Size of the text:", text_size, "bytes")




# 1. https://hikouki0408.github.io/portfolio 
# 2. https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam
# 3. https://www.nytimes.com



