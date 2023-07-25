from urllib import request
from html.parser import HTMLParser
import re
from pycorenlp import StanfordCoreNLP
import time
import json
import sys
from selenium import webdriver


# make sure to have openie-assembly-5.0-SNAPSHOT.jar in the same folder
# run this code: java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
# then run: python3 OIE_extracted_text.py on another terminal

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_head_tag = False
        self.inside_body_tag = False
        self.skip_tag_body = False
        self.select_tag_head = False
        self.extract_script = False
        self.tag_stack = []
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.url_pattern = re.compile(r'^(?:https?://|www\.)\S+\.[a-zA-Z]{2,}(?:[/?#]\S*)?$')
        self.date_patterns = ["\d{1,2}\/\d{1,2}\/\d{4}", "\d{1,2}-\d{1,2}-d{4}"]
        self.text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.inside_head_tag = True
        if tag == "body":
            self.inside_body_tag = True
        self.tag_stack.append(tag)
        if tag in ["title"]:
            self.select_tag_head = True
        if tag in ["script"]:
            self.extract_script = True
        if tag in ["style", "iframe", "svg", "form", "button", "footer", "nav"]:
            self.skip_tag_body = True

    def handle_endtag(self, tag):
        if tag == "head":
            self.inside_head_tag = False
        if tag == "body":
            self.inside_body_tag = False
        #if tag in ["script", "style", "image", "iframe", "button", "label", "nav", "footer"]:
        if tag in ["title"]:
            self.select_tag_head = False
        if tag in ["script"]:
            self.extract_script = False
        if tag in ["style", "iframe", "svg", "form", "button", "footer", "nav"]:
            self.skip_tag_body = False
        self.tag_stack.pop()
    
    def execute_javascript_code(self, script_code):
            # Set Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        
        # Create a new instance of the Chrome browser
        driver = webdriver.Chrome(options=options)
        
        driver.get('data:text/html;charset=utf-8,<!DOCTYPE html><html><head></head><body></body></html>')

        try:
            driver.execute_script(script_code)
                # Extract the dynamically generated text displayed on the browser
            script_extract_text = '''
                var elements = document.querySelectorAll('body > *');
                var texts = "";
                elements.forEach(function(element) {
                    texts += element.textContent + " ";
                });
                return texts.trim();
            '''
            extracted_text = driver.execute_script(script_extract_text)
            # Close the browser
            driver.quit()

            return extracted_text

        except Exception as e:
            # If there's an error, print the error message or return an empty string
            return ''

    def handle_data(self, data):
        message = ''
        label = "undefined"
        if self.inside_head_tag:
            if self.select_tag_head and data.strip():
                self.text += data.strip() + ". "
            elif self.extract_script:
                script_code = data.strip()
                extracted_content = self.execute_javascript_code(script_code)
                if extracted_content:
                    self.text += extracted_content + " "
        if self.inside_body_tag:
            if not self.skip_tag_body and data.strip():
                tag = self.tag_stack[-1] if self.tag_stack else None
                if self.extract_script:
                    script_code = data.strip()
                    extracted_content = self.execute_javascript_code(script_code)
                    if extracted_content:
                        data = extracted_content
                    else:
                        data = ''
                if re.search(self.email_pattern, data) and not any(char.isspace() for char in data.strip()):
                    label = "Email"
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                elif re.search(self.url_pattern, data) and not any(char.isspace() for char in data.strip()):
                    label = "Website"
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                elif not re.search(r'[a-zA-Z0-9]', data): #if the extraced text does not contain any alphanumeric character or digits from 0 to 9, ex) japanese, special char
                    label = "Non-contextual"              # ex) 1.1% contains digit number so does not apply, but if the extraced text is only '%' or '.' or '日本語' then defined as "Non-contextual".
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                else:
                    label = "Puretext" # text that are examined by relation extraction model
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                    self.text += data.strip() + " "
        #if message:
            #print(message)

    def extract_relations_from_text(self, instances):
        nlp = StanfordCoreNLP('http://localhost:9000')
        text = self.text
        total_instances = len(instances)
        unique_sets = set()
        matched_triples = set()
        count_unexpected = 0
        output = nlp.annotate(text, properties={
            'annotators': 'openie',
            'outputFormat': 'json',
            'openie.triple.strict': 'true',
            'openie.max_entailments_per_clause': '1'
        })
        for instance in instances:
            unique_sets.add((instance['Subject'], instance['Relation'], instance['Object']))

        for sentence in output['sentences']:
            for triple in sentence['openie']:
                subject = triple['subject']
                relation = triple['relation']
                obj = triple['object']
                """
                print(f"Subject: {subject}, Relation: {relation}, Object: {obj}")
                
                # Check if the set is in the unique_sets set
                if (subject, relation, obj) in unique_sets and (subject, relation, obj) not in matched_triples:
                    print(f"Subject: {subject}, Relation: {relation}, Object: {obj}")
                    print("Match found in Dataset!")
                    matched_triples.add((subject, relation, obj))  # Add to the matched triples set
                else:
                    count_unexpected += 1
        
        print()
        print("Total_triples: ", len(instances))
        print("Total_correct: ", len(matched_triples))
        print("Total_wrong: ", count_unexpected)
        TP = len(matched_triples)
        FN = total_instances - TP
        FP = count_unexpected
        print("Total_failed: ", FN)
        Precision = TP / (TP + FP)
        Recall = TP / (TP + FN)
        F1_Score = 2 * (Precision * Recall) / (Precision + Recall)
        print("Precision is ", Precision)
        print("Recall is ", Recall)
        print("F1_score is ",F1_Score)
        """
 
                
with open('Datasets/dataset_engadget.json', 'r') as file:
    json_data = json.load(file)
    
# Fetch the URL and pass the HTML content to the parser
url = "https://www.engadget.com/best-android-phone-130030805.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAMJRC35y42RkEpGFN410RsxpbKvMCO1YlLmbtdzQ8pV8l3LRZ5sWPGJQYf-yEwX7vimbG2qzSJYMbpZ545Hz3cup5XB1qlkb203T1mVAKhmOteZxYDxKoohpFTWRvo-M8MzqByHFRBN4-odKGhQEche2Zb-GXjopL6cIZsxeIuLl"
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
runtime_OpenIE = run_time - runtime_text_extraction
print("Runtime_textExtraction: ", runtime_text_extraction, "seconds")
print("Runtime_total :", run_time, "seconds")
print("Runtime_OpenIE: ", runtime_OpenIE, "seconds")
text_size = sys.getsizeof(parser.text)
print("Size of the text:", text_size, "bytes")


# https://hikouki0408.github.io/portfolio/                        
# 1. https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam
# 2  https://www.tudelftcampus.nl/time-to-shake-up-the-pile-driving-industry
# 3. https://stackoverflow.blog/2023/05/31/ceo-update-paving-the-road-forward-with-ai-and-community-at-the-center
# 4. https://www.euronews.com/travel/2023/02/27/long-queues-and-scams-will-the-new-eu-entry-system-cause-border-chaos
# 5. https://theluxurytravelexpert.com/2020/12/14/best-hotels-in-the-world Size of the text: 211956 bytes
# 6. https://research.ibm.com/blog/utility-toward-useful-quantum             Size of the text: 115986 bytes
# 7. https://www.hotcars.com/upcoming-cars-worth-waiting-for/#2023-fisker-ocean Size of the text: 112716 bytes
# 8. https://hackr.io/blog/what-is-programming Size of the text: 94236 bytes
# 9. https://www.amsterdamfoodie.nl/amsterdam-food-guide/indonesian-restaurants-in-amsterdam-rijsttafel # Size of the text: 75670 bytes

# 10. https://www.engadget.com/best-android-phone-130030805.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAMJRC35y42RkEpGFN410RsxpbKvMCO1YlLmbtdzQ8pV8l3LRZ5sWPGJQYf-yEwX7vimbG2qzSJYMbpZ545Hz3cup5XB1qlkb203T1mVAKhmOteZxYDxKoohpFTWRvo-M8MzqByHFRBN4-odKGhQEche2Zb-GXjopL6cIZsxeIuLl
# 10. (above) Size of the text: 86898 bytes


