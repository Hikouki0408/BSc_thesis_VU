import requests
from bs4 import BeautifulSoup
from urllib import request
from html.parser import HTMLParser
import re
from pycorenlp import StanfordCoreNLP
import time
import json
import sys

# run this code: java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
# then run: python3 OIE_extracted_text.py on another terminal

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
        unique_sets = set()
        count_matched = 0
        count_unexpected = 0
        output = nlp.annotate(text, properties={
            'annotators': 'openie',
            'outputFormat': 'json',
            'openie.triple.strict': 'true',
            'openie.max_entailments_per_clause': '1'
        })
        for instance in instances:
            unique_sets.add((instance['Subject'], instance['Relation'], instance['Object']))

        # Loop through the 'output' JSON data
        for sentence in output['sentences']:
            for triple in sentence['openie']:
                subject = triple['subject']
                relation = triple['relation']
                obj = triple['object']
                print(f"Subject: {subject}, Relation: {relation}, Object: {obj}")
                
                # Check if the set is in the unique_sets set
                if (subject, relation, obj) in unique_sets:
                    print("Match found in Dataset!")
                    count_matched += 1
                else:
                    print("Not found in Dataset!")
                    count_unexpected += 1
        
        print()
        print("Total_triples: ", len(instances))
        print("Total_correct: ",count_matched)
        print("Total_wrong: ", count_unexpected)
        TP = count_matched
        FN = total_instances - TP
        FP = count_unexpected
        print("Total_failed: ", FN)
        Precision = TP / (TP + FP)
        Recall = TP / (TP + FN)
        F1_Score = 2 * (Precision * Recall) / (Precision + Recall)
        print("Precision is ", Precision)
        print("Recall is ", Recall)
        print("F1_score is ",F1_Score)
        
        


with open('Datasets/dataset_tudelft.json', 'r') as file:
    json_data = json.load(file)
    
# Fetch the URL and pass the HTML content to the parser
url = "https://www.tudelftcampus.nl/time-to-shake-up-the-pile-driving-industry"

# 1. https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam
# 2. https://www.gutenberg.org/cache/epub/27137/pg27137-images.html
# 3. https://stackoverflow.blog/2023/05/31/ceo-update-paving-the-road-forward-with-ai-and-community-at-the-center
# 4. https://www.euronews.com/travel/2023/02/27/long-queues-and-scams-will-the-new-eu-entry-system-cause-border-chaos
# 5. https://www.tudelftcampus.nl/time-to-shake-up-the-pile-driving-industry

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
