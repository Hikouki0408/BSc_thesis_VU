import requests
from bs4 import BeautifulSoup

# 1. https://hikouki0408.github.io/portfolio 
# 2. https://vu.nl/nl
# 3. https://www.u-tokyo.ac.jp/en/
# 4. https://www.cntraveller.com/gallery/beautiful-places-amsterdam
# 5. https://weather.com/?Goto=Redirected
# 6. https://nl.wikipedia.org/wiki/Wikipedia
# 7. https://stackoverflow.co
# 8. https://www.billboard.com/
# 9. https://www.amazon.nl/-/en/
# 10. https://www.government.nl/

# Load the website URL
url = 'https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam'
response = requests.get(url)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the body tag
body = soup.find('body')

# Find all the HTML tags inside the body tag
tags = body.find_all()

# Count the number of tags containing text and the number of tags not containing text
text_tags = 0
non_text_tags = 0
text_tag_list = []
non_text_tag_list = []

# Count the number of each type of tag and the number of each type of tag containing text
tag_counts = {}
text_counts = {}

for tag in tags:
    if tag.name[0] != '/':  # Only count opening tags
        if tag.string:
            text_tags += 1
            text_tag_list.append(tag.name)
            if tag.name in text_counts:
                text_counts[tag.name] += 1
            else:
                text_counts[tag.name] = 1
            if tag.name in tag_counts:
                tag_counts[tag.name] += 1
            else:
                tag_counts[tag.name] = 1
        else:
            if tag.name != 'p' or not tag.find_all('a'):  # Exclude p tag containing a tags
                non_text_tags += 1
                non_text_tag_list.append(tag.name)
                if tag.name in tag_counts:
                    tag_counts[tag.name] += 1
                else:
                    tag_counts[tag.name] = 1

# Calculate the percentage of tags containing text
total_tags = text_tags + non_text_tags
text_percentage = (text_tags / total_tags) * 100

# Calculate the percentage of each type of tag containing text
text_percentages = {}

for tag, count in tag_counts.items():
    if tag in text_counts:
        text_percentages[tag] = (text_counts[tag] / count) * 100
    else:
        text_percentages[tag] = 0

# Print the results
print(f'Total tags: {total_tags}')
print(f'Tags containing text: {text_tags}')
print(f'Tags not containing text: {non_text_tags}')
print(f'Percentage of tags containing text: {text_percentage:.2f}%')
print(f'Tags containing text: {text_tag_list}')
print(f'Tags not containing text: {non_text_tag_list}')
print('Percentage of each type of tag containing text:')
for tag, percentage in sorted(text_percentages.items(), key=lambda x: x[1], reverse=True):
    print(f'{tag}: {percentage:.2f}%')





""""
website 1.

Percentage of each type of tag containing text:
span: 100.00%
p: 100.00%
h2: 100.00%
h3: 100.00%
strong: 100.00%
h5: 100.00%
a: 60.00%
h4: 50.00%
li: 13.33%
div: 7.02%
section: 0.00%
nav: 0.00%
ul: 0.00%
i: 0.00%
footer: 0.00%
main: 0.00%
header: 0.00%
img: 0.00%
iframe: 0.00%
br: 0.00%

website 2.https://vu.nl/nl

Percentage of each type of tag containing text:
widget-navigation: 100.00%
widget-login: 100.00%
my-studychoice-authentication: 100.00%
h1: 100.00%
widget-search-overlay: 100.00%
style: 100.00%
p: 100.00%
h2: 100.00%
span: 86.21%
button: 50.00%
widget-content-slider: 50.00%
script: 25.00%
img: 16.67%
section: 11.11%
a: 7.94%
div: 1.94%
noscript: 0.00%
iframe: 0.00%
header: 0.00%
ul: 0.00%
li: 0.00%
i: 0.00%
main: 0.00%
widget-agenda: 0.00%
form: 0.00%
label: 0.00%
input: 0.00%
footer: 0.00%

website 3.

Percentage of each type of tag containing text:
button: 100.00%
strong: 100.00%
style: 100.00%
link: 100.00%
dt: 100.00%
address: 100.00%
p: 86.09%
li: 78.07%
span: 75.76%
a: 59.61%
noscript: 50.00%
script: 14.29%
div: 2.26%
iframe: 0.00%
header: 0.00%
h1: 0.00%
img: 0.00%
ul: 0.00%
form: 0.00%
input: 0.00%
nav: 0.00%
figure: 0.00%
main: 0.00%
br: 0.00%
dl: 0.00%
dd: 0.00%
footer: 0.00%

website 4.

Percentage of each type of tag containing text:
title: 100.00%
h1: 100.00%
time: 100.00%
h2: 100.00%
em: 100.00%
strong: 100.00%
p: 84.31%
span: 58.85%
a: 56.64%
header: 33.33%
script: 29.17%
li: 29.01%
div: 24.85%
button: 16.67%
noscript: 0.00%
iframe: 0.00%
aside: 0.00%
svg: 0.00%
path: 0.00%
picture: 0.00%
img: 0.00%
nav: 0.00%
ul: 0.00%
i: 0.00%
section: 0.00%
main: 0.00%
article: 0.00%
figure: 0.00%
source: 0.00%
figcaption: 0.00%
footer: 0.00%
g: 0.00%
defs: 0.00%
clippath: 0.00%
rect: 0.00%

website 5. 

Percentage of each type of tag containing text:
title: 100.00%
legend: 100.00%
label: 100.00%
h2: 100.00%
h3: 100.00%
p: 100.00%
tspan: 100.00%
script: 100.00%
li: 93.75%
span: 92.16%
a: 87.71%
header: 75.00%
button: 71.88%
footer: 57.14%
div: 18.66%
svg: 0.00%
path: 0.00%
img: 0.00%
form: 0.00%
fieldset: 0.00%
input: 0.00%
nav: 0.00%
section: 0.00%
ul: 0.00%
details: 0.00%
summary: 0.00%
main: 0.00%
noscript: 0.00%
g: 0.00%
rect: 0.00%
aside: 0.00%
defs: 0.00%
lineargradient: 0.00%
stop: 0.00%
text: 0.00%
image: 0.00%
mask: 0.00%
use: 0.00%
symbol: 0.00%
circle: 0.00%


"""

