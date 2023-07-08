import requests
from bs4 import BeautifulSoup
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
        self.text = ''

    def extract_text_from_url(self, url):
        # Send a GET request to the URL and retrieve the HTML content
        response = requests.get(url)
        html_content = response.content

        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all the text elements in the HTML
        text_elements = soup.find_all(string=True)

        # Extract the text from the elements and remove leading/trailing whitespace
        text = ' '.join(element.strip() for element in text_elements if element.strip())
        
        return text
    
    def extract_relations_from_text(self, text, instances):
        nlp = StanfordCoreNLP('http://localhost:9000')
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
        print(FN)
        FP = count_unexpected
        Precision = TP / (TP + FP)
        Recall = TP / (TP + FN)
        F1_Score = 2 * (Precision * Recall) / (Precision + Recall)
        print("Precision is ", Precision)
        print("Recall is ", Recall)
        print("F1_score is ",F1_Score)
        """
        
        


with open('dataset_ebook.json', 'r') as file:
    json_data = json.load(file)
    
# Fetch the URL and pass the HTML content to the parser
url = "https://www.gutenberg.org/cache/epub/27137/pg27137-images.html"

parser = MyHTMLParser()

start_time = time.time()
extracted_text = parser.extract_text_from_url(url)
runtime_time_1 = time.time()
runtime_text_extraction = runtime_time_1 - start_time
parser.extract_relations_from_text(extracted_text, json_data)
runtime_time_2 = time.time()
run_time = runtime_time_2 - start_time
print("Runtime_textExtraction: ", runtime_text_extraction, "seconds")
print("Runtime_total :", run_time, "seconds")
text_size = sys.getsizeof(extracted_text)
print("Size of the text:", text_size, "bytes")
