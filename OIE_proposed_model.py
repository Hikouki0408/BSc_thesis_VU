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
# then run: python3 OIE_proposed_model.py on another terminal

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
        if tag == "head":                         # Check if the current tag is the opening <head> tag
            self.inside_head_tag = True           # Set the flag to indicate being inside the <head> tag
        if tag == "body":                         # Check if the current tag is the opening <body> tag
            self.inside_body_tag = True           # Set the flag to indicate being inside the <body> tag
        self.tag_stack.append(tag)               # Add the tag to the tag stack for tracking nested tags

        if tag in ["title"]:                     # Check if the current tag is one of the specified tags (e.g., <title>)
            self.select_tag_head = True          # Set the flag to indicate selecting content from the <head> tag (e.g., <title> content)
        if tag in ["script"]:                    # Check if the current tag is one of the specified tags (e.g., <script>)
            self.extract_script = True           # Set the flag to indicate extracting content from the <script> tag

        if tag in ["style", "iframe", "svg", "form", "button", "footer", "nav"]:
            # Check if the current tag is one of the specified tags to filter out in the <body> section
            self.skip_tag_body = True            # Set the flag to skip processing content from this tag in the <body>

    def handle_endtag(self, tag):
        if tag == "head":                           # Check if the end tag is for the <head> element
            self.inside_head_tag = False            # Set 'inside_head_tag' to False since the <head> section ends
        if tag == "body":                           # Check if the end tag is for the <body> element
            self.inside_body_tag = False            # Set 'inside_body_tag' to False since the <body> section ends
        if tag in ["title"]:                        # Check if the end tag is for the <title> element
            self.select_tag_head = False            # Set 'select_tag_head' to False since the <title> section ends
        if tag in ["script"]:                       # Check if the end tag is for the <script> element
            self.extract_script = False             # Set 'extract_script' to False since the <script> section ends
        if tag in ["style", "iframe", "svg", "form", "button", "footer", "nav"]:
            # Check if the end tag is for any of the elements listed (style, iframe, svg, form, button, footer, nav)
            self.skip_tag_body = False              # Set 'skip_tag_body' to False since the corresponding section ends
        self.tag_stack.pop()                        # Remove the last tag from 'tag_stack' since it's the ending tag


    def execute_javascript_code(self, script_code):
        # Set Chrome options for running the browser in a headless mode (without UI)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        # Create a new instance of the Chrome browser with the defined options
        driver = webdriver.Chrome(options=options)

        # Load a blank page in the browser to execute the provided JavaScript code
        driver.get('data:text/html;charset=utf-8,<!DOCTYPE html><html><head></head><body></body></html>')

        try:
            # Execute the provided JavaScript code in the browser
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

            # Close the browser after extracting the text
            driver.quit()

            return extracted_text   # Return the extracted text from the dynamically generated content

        except Exception as e:
            # If there's an error during JavaScript execution, print the error message or return an empty string
            return ''

    def handle_data(self, data):
        message = ''                              
        label = "undefined"                       

        if self.inside_head_tag:                  # Check if currently inside the <head> tag
            if self.select_tag_head and data.strip():     # If 'select_tag_head' is True and data is not empty, append the stripped data to 'self.text'
                self.text += data.strip() + ". "
            elif self.extract_script:             # If 'extract_script' is True, execute JavaScript code and add the extracted content to 'self.text'
                script_code = data.strip()
                extracted_content = self.execute_javascript_code(script_code)
                if extracted_content:
                    self.text += extracted_content + " "

        if self.inside_body_tag:                  # Check if currently inside the <body> tag
            if not self.skip_tag_body and data.strip():   # If 'skip_tag_body' is False and data is not empty, proceed with data handling
                tag = self.tag_stack[-1] if self.tag_stack else None   # Get the last tag in the list or None if the list is empty

                if self.extract_script:           # If 'extract_script' is True, execute JavaScript code and update 'data' with the extracted content
                    script_code = data.strip()
                    extracted_content = self.execute_javascript_code(script_code)
                    if extracted_content:
                        data = extracted_content
                    else:
                        data = ''

                # Check data for specific patterns (email, URL, non-contextual, or Puretext) using regex
                if re.search(self.email_pattern, data) and not any(char.isspace() for char in data.strip()):
                    label = "Email"
                    message = f"{label}: [{data.strip()}] (tag: {tag})"  # Construct a message string with the label and data

                elif re.search(self.url_pattern, data) and not any(char.isspace() for char in data.strip()):
                    label = "Website"
                    message = f"{label}: [{data.strip()}] (tag: {tag})"

                elif not re.search(r'[a-zA-Z0-9]', data):   # Check if data contains no letters or digits (non-contextual data)
                    label = "Non-contextual"                # ex) 1.1% contains digit number so does not apply, but if the extraced text is only '%' or '.' or '日本語' then defined as "Non-contextual".
                    message = f"{label}: [{data.strip()}] (tag: {tag})"

                else:   # If none of the above patterns match, consider the data as pure text
                    label = "Puretext"
                    message = f"{label}: [{data.strip()}] (tag: {tag})"
                    self.text += data.strip() + " "   # Append the data to 'self.text'


                #if message:
                    #print(message)   


    def extract_relations_from_text(self, instances):
        # Initialize StanfordCoreNLP for natural language processing
        nlp = StanfordCoreNLP('http://localhost:9000')

        text = self.text                             # Get the extracted text from the class attribute 'self.text'
        total_instances = len(instances)             # Get the total number of instances (triples) to extract relations for
        unique_sets = set()                          # Initialize a set to store unique triples from the provided 'instances'
        matched_triples = set()                      # Initialize a set to store matched triples found in the text
        count_unexpected = 0                         # Initialize a counter for unexpected (incorrect) triples found
        output = nlp.annotate(text, properties={
            'annotators': 'openie',                  # Use OpenIE for extracting relations
            'outputFormat': 'json',                 # Specify output format as JSON
            'openie.triple.strict': 'true',         # Set strict mode to only consider confident extractions
            'openie.max_entailments_per_clause': '1' # Limit the number of entailments per clause to 1
        })

        # Extract unique triples (Subject, Relation, Object) from the provided 'instances'
        for instance in instances:
            unique_sets.add((instance['Subject'], instance['Relation'], instance['Object']))

        # Iterate through the sentences and their extracted triples from the text
        for sentence in output['sentences']:
            for triple in sentence['openie']:
                subject = triple['subject']          # Extracted subject from the triple
                relation = triple['relation']        # Extracted relation from the triple
                obj = triple['object']               # Extracted object from the triple
                print(f"Subject: {subject}, Relation: {relation}, Object: {obj}")

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
print("Runtime_OpenIE: ", runtime_OpenIE, "seconds")
text_size = sys.getsizeof(parser.text)
print("Size of the text:", text_size, "bytes")


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



