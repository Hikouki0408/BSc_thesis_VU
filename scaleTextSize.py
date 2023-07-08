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
    
    
# Fetch the URL and pass the HTML content to the parser
url = "https://www.gutenberg.org/cache/epub/32498/pg32498-images.html"

parser = MyHTMLParser()
start_time = time.time()
extracted_text = parser.extract_text_from_url(url)
text_size = sys.getsizeof(extracted_text)
print("Size of the text:", text_size, "bytes")
