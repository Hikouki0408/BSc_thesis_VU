import requests
from bs4 import BeautifulSoup
from urllib import request
from html.parser import HTMLParser
from pycorenlp import StanfordCoreNLP
import time
import json
import sys

# make sure to have openie-assembly-5.0-SNAPSHOT.jar in the same folder
# run this code: java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
# then run: python3 OIE_basemodel.py on another terminal

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
        # Initialize StanfordCoreNLP for natural language processing
        nlp = StanfordCoreNLP('http://localhost:9000')

        total_instances = len(instances)         # Get the total number of instances (triples) to extract relations for
        unique_sets = set()                      # Initialize a set to store unique triples from the provided 'instances'
        matched_triples = set()                  # Initialize a set to store matched triples found in the text
        count_unexpected = 0                     # Initialize a counter for unexpected (incorrect) triples found
        output = nlp.annotate(text, properties={
            'annotators': 'openie',              # Use OpenIE for extracting relations
            'outputFormat': 'json',             # Specify output format as JSON
            'openie.triple.strict': 'true',     # Set strict mode to only consider confident extractions
            'openie.max_entailments_per_clause': '1' # Limit the number of entailments per clause to 1
        })

        # Extract unique triples (Subject, Relation, Object) from the provided 'instances'
        for instance in instances:
            unique_sets.add((instance['Subject'], instance['Relation'], instance['Object']))

        # Loop through the 'output' JSON data
        for sentence in output['sentences']:
            for triple in sentence['openie']:
                subject = triple['subject']          # Extracted subject from the triple
                relation = triple['relation']        # Extracted relation from the triple
                obj = triple['object']               # Extracted object from the triple
                    
                # Check if the triple (Subject, Relation, Object) is in the 'unique_sets' set
                if (subject, relation, obj) in unique_sets and (subject, relation, obj) not in matched_triples:
                    print(f"Subject: {subject}, Relation: {relation}, Object: {obj}")
                    print("Match found in Dataset!")
                    matched_triples.add((subject, relation, obj))  # Add the matched triple to 'matched_triples' set
                else:
                    count_unexpected += 1    # Increment the counter for unexpected triples

        # Print statistics and evaluation metrics
        print()
        print("Total_triples: ", len(instances))    # Print the total number of instances (triples) to extract relations for
        print("Total_correct: ", len(matched_triples))    # Print the total number of correctly matched triples
        print("Total_wrong: ", count_unexpected)    # Print the total number of unexpected (incorrect) triples found
        TP = len(matched_triples)                   # Calculate True Positives (matched triples)
        FN = total_instances - TP                   # Calculate False Negatives (triples not matched)
        FP = count_unexpected                        # Calculate False Positives (unexpected triples)
        print("Total_failed: ", FN)                 # Print the total number of triples that failed to match
        Precision = TP / (TP + FP)                  # Calculate Precision
        Recall = TP / (TP + FN)                     # Calculate Recall
        F1_Score = 2 * (Precision * Recall) / (Precision + Recall)   # Calculate F1-Score
        print("Precision is ", Precision)          
        print("Recall is ", Recall)                
        print("F1_score is ",F1_Score)             

        
        


with open('Datasets/dataset_wiki.json', 'r') as file:
    json_data = json.load(file)
    
# Fetch the URL and pass the HTML content to the parser
url = "https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam"

# 1. https://theluxurytravelexpert.com/2020/12/14/best-hotels-in-the-world 
# 2. https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam
# 3. https://research.ibm.com/blog/utility-toward-useful-quantum
# 4. https://www.hotcars.com/upcoming-cars-worth-waiting-for/#2023-fisker-ocean
# 5. https://www.tudelftcampus.nl/time-to-shake-up-the-pile-driving-industry
# 6. https://hackr.io/blog/what-is-programming
# 7. https://www.engadget.com/best-android-phone-130030805.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAMJRC35y42RkEpGFN410RsxpbKvMCO1YlLmbtdzQ8pV8l3LRZ5sWPGJQYf-yEwX7vimbG2qzSJYMbpZ545Hz3cup5XB1qlkb203T1mVAKhmOteZxYDxKoohpFTWRvo-M8MzqByHFRBN4-odKGhQEche2Zb-GXjopL6cIZsxeIuLl
# 8. https://www.amsterdamfoodie.nl/amsterdam-food-guide/indonesian-restaurants-in-amsterdam-rijsttafel
# 9. https://stackoverflow.blog/2023/05/31/ceo-update-paving-the-road-forward-with-ai-and-community-at-the-center
# 10. https://www.euronews.com/travel/2023/02/27/long-queues-and-scams-will-the-new-eu-entry-system-cause-border-chaos

parser = MyHTMLParser()
start_time = time.time()
extracted_text = parser.extract_text_from_url(url)
runtime_time_1 = time.time()
runtime_text_extraction = runtime_time_1 - start_time
parser.extract_relations_from_text(extracted_text, json_data)
runtime_time_2 = time.time()
run_time = runtime_time_2 - start_time
runtime_OpenIE = run_time - runtime_text_extraction
print("Runtime_textExtraction: ", runtime_text_extraction, "seconds")
print("Runtime_OpenIE: ", runtime_OpenIE, "seconds")
text_size = sys.getsizeof(extracted_text)
print("Size of the text:", text_size, "bytes")
