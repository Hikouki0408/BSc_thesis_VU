import urllib.request
from html.parser import HTMLParser
import re
import spacy
from selenium import webdriver


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_head_tag = False
        self.inside_body_tag = False
        self.skip_tag_body = False
        self.select_tag_head = False
        self.extract_script = False
        self.tag_stack = []
        self.data_by_label = {}
        self.nlp = spacy.load("en_core_web_sm") # loads a pre-trained English language model 
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.url_pattern = re.compile(r'^(?:https?://|www\.)\S+\.[a-zA-Z]{2,}(?:[/?#]\S*)?$')
        self.date_patterns = ["\d{1,2}\/\d{1,2}\/\d{4}", "\d{1,2}-\d{1,2}-d{4}"]
        self.count = 0
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
            # If there's an error, print the error message and return an empty string
            return ''

    def handle_data(self, data):
        #message = ''
        label = "undefined"
        if self.inside_head_tag:
            if self.select_tag_head and data.strip():
                self.text += data.strip() + " "
            elif self.extract_script:
                script_code = data.strip()
                extracted_content = self.execute_javascript_code(script_code)
                if extracted_content:
                    self.text += extracted_content + " "
        if self.inside_body_tag:
            if not self.skip_tag_body and data.strip():
                # returns the last tag in the list
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
                    label = "Puretext"
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
                        self.text += data.strip() + " "
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
                        self.text += data.strip() + " "
                        message = f"{label}: [{data.strip()}] (tag: {tag})"
                        self.count += 1
        #if message:
            #print(message)


    def print_data_by_label(self):
        for label, data in self.data_by_label.items():
            if label != "Puretext":
                print(f"Data for label '{label}': ", end="")
                for i, datum in enumerate(data):
                    if i == len(data) - 1:
                        print(datum)
                    else:
                        print(datum, end=", ") 
    
# https://hikouki0408.github.io/portfolio/                        
# 1. https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam
# 2. https://stackoverflow.blog/2023/05/31/ceo-update-paving-the-road-forward-with-ai-and-community-at-the-center
# 3. https://www.euronews.com/travel/2023/02/27/long-queues-and-scams-will-the-new-eu-entry-system-cause-border-chaos
# 4. https://www.tudelftcampus.nl/time-to-shake-up-the-pile-driving-industry
# 5. https://hackr.io/blog/what-is-programming
# 6. https://www.amsterdamfoodie.nl/amsterdam-food-guide/indonesian-restaurants-in-amsterdam-rijsttafel
# 7. https://www.engadget.com/best-android-phone-130030805.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAMJRC35y42RkEpGFN410RsxpbKvMCO1YlLmbtdzQ8pV8l3LRZ5sWPGJQYf-yEwX7vimbG2qzSJYMbpZ545Hz3cup5XB1qlkb203T1mVAKhmOteZxYDxKoohpFTWRvo-M8MzqByHFRBN4-odKGhQEche2Zb-GXjopL6cIZsxeIuLl
# 8. https://www.hotcars.com/upcoming-cars-worth-waiting-for/#2023-fisker-ocean
# 9. https://research.ibm.com/blog/utility-toward-useful-quantum
# 10. https://theluxurytravelexpert.com/2020/12/14/best-hotels-in-the-world

response = urllib.request.urlopen('https://stackoverflow.blog/2023/05/31/ceo-update-paving-the-road-forward-with-ai-and-community-at-the-center')
parser = MyHTMLParser()
print("[Parsing HTML file...]")
print()
parser.feed(response.read().decode('utf-8'))
print("[Done parsing HTML file.]")
print()
#parser.print_data_by_label()
print("[Done printing data by label.]")
print(parser.text)


"""
with open('text.txt', 'w') as file:
    file.write(parser.text)
"""