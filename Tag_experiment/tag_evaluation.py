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
# 9. https://www.amazon.nl/-/en
# 10. https://www.government.nl/

# Load the website URL
url = 'https://en.wikipedia.org/wiki/Main_Page'
response = requests.get(url)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the body tag
body = soup.find('body')

# Find all the HTML tags inside the body tag, excluding the <style> and <script> tags
tags = body.find_all(lambda tag: tag.name not in ['style', 'script'])

# Count the number of tags containing text and the number of tags not containing text
text_tags = 0
non_text_tags = 0
text_tag_list = []
non_text_tag_list = []

# Count the number of each type of tag and the number of each type of tag containing text
tag_counts = {}
text_counts = {}
tag_texts = {}

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
            if tag.name in tag_texts:
                tag_texts[tag.name].append(tag.string.strip())
            else:
                tag_texts[tag.name] = [tag.string.strip()]
        else:
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
    if tag in tag_texts:
        text = ', '.join(tag_texts[tag])
    else:
        text = ''
    print(f'{tag}: {percentage:.2f}%, text: {text}')


""""
website 1.

python3 tag_evaluation.py
Total tags: 191
Tags containing text: 65
Tags not containing text: 126
Percentage of tags containing text: 34.03%
Tags containing text: ['a', 'span', 'span', 'span', 'span', 'span', 'span', 'p', 'li', 'a', 'li', 'a', 'h2', 'p', 'span', 'h3', 'span', 'p', 'p', 'p', 'span', 'h3', 'strong', 'strong', 'strong', 'p', 'a', 'span', 'h3', 'h4', 'h5', 'p', 'a', 'h5', 'p', 'a', 'h5', 'p', 'a', 'h5', 'p', 'a', 'h5', 'p', 'a', 'a', 'span', 'h3', 'div', 'p', 'a', 'div', 'p', 'a', 'div', 'p', 'a', 'div', 'p', 'a', 'span', 'h3', 'p', 'a', 'p']
Tags not containing text: ['section', 'nav', 'div', 'ul', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'footer', 'main', 'header', 'div', 'div', 'ul', 'div', 'div', 'img', 'div', 'div', 'section', 'div', 'div', 'div', 'img', 'div', 'h4', 'iframe', 'section', 'div', 'ul', 'li', 'img', 'br', 'br', 'br', 'li', 'img', 'br', 'br', 'li', 'img', 'br', 'br', 'br', 'section', 'div', 'div', 'div', 'div', 'div', 'img', 'div', 'div', 'img', 'div', 'div', 'div', 'div', 'img', 'div', 'div', 'div', 'img', 'div', 'div', 'div', 'img', 'div', 'section', 'div', 'div', 'div', 'div', 'div', 'div', 'img', 'div', 'div', 'div', 'div', 'img', 'div', 'div', 'div', 'div', 'img', 'div', 'div', 'div', 'div', 'img', 'section', 'div', 'div', 'div', 'iframe', 'div', 'p', 'div', 'ul', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i']
Percentage of each type of tag containing text:
span: 100.00%, text: Home, About, Education, Projects, Blogs, Contact, Information about me, Koki Hirose, Degree & Major, My Recent Projects, Views News, Get in Touch
h2: 100.00%, text: Web Developer & Social media content creator
h3: 100.00%, text: About Me, Education, My Portfolio, Latest News, CONTACT ME
strong: 100.00%, text: - Vrije Universiteit Amsterdam Sep 2020 - Present, - Study Group Holland ISC Sep 2019 - Aug 2020, - Tokai University, Japan Apr 2017 - March 2019
h5: 100.00%, text: Snake, Tetris, GPX manager, My Theis, Work in progress
p: 94.44%, text: © 2023 Koki Hirose, Multicultural individual from Japan, living in Amsterdam, the Netherlands. Works in web development and filmmaking, driven by tradition and innovation., Hello, I'm Koki, a web developer and social media content creator with a passion for creating beautiful and engaging digital experiences. As an entry-level developer, I have a foundational knowledge of web development, mobile application development, and programming languages such as C++, Java, and JavaScript., I'm excited about combining my technical skills with my creativity to build dynamic and engaging websites and mobile apps. I have a strong eye for design and a passion for creating content that resonates with audiences and drives engagement., Although I'm still developing my skills, I'm eager to learn and grow in my role as a web developer and social media content creator. I believe that every project presents an opportunity to improve and I am always looking for ways to refine my skills., My CV is available via LinkedIn., Object Oriented in Scala, Object Oriented in Scala, Programmed in Java, Extract text from HTML pages for advanced relation extraction, Programmed in Java, 14 April, 2023, 15 April, 2023, 17 April, 2023, 29 April, 2023, I am based in Amsterdam, Netherlands, and I'm always looking to connect with new people. Whether you're interested in collaborating on a project or just want to say hello, I'd love to hear from you., Thank you for visiting my website, and I look forward to hearing from you soon!
a: 60.00%, text: KOKI HIROSE, English, 日本語, https://www.linkedin.com/in/koki-hirose-365a9224, View Project, View Project, View Project, View Project, View Project, Add More..., Extract text from HTML pages for advanced relation extraction, How Chat-GPT is Actually Creating Jobs, Not Stealing Them, Chat-GPT's Impact on Student and Professor Learning Experience., Want to live in the EU? New rules could make it easier to move between countries, koki248vlog@gmail.com
h4: 50.00%, text: Portfolios
li: 13.33%, text: English, 日本語
div: 7.02%, text: , , , 
section: 0.00%, text: 
nav: 0.00%, text: 
ul: 0.00%, text: 
i: 0.00%, text: 
footer: 0.00%, text: 
main: 0.00%, text: 
header: 0.00%, text: 
img: 0.00%, text: 
iframe: 0.00%, text: 
br: 0.00%, text: 

website 2.https://vu.nl/nl

Total tags: 488
Tags containing text: 105
Tags not containing text: 383
Percentage of tags containing text: 21.52%
Tags containing text: ['widget-navigation', 'span', 'span', 'a', 'span', 'span', 'widget-login', 'my-studychoice-authentication', 'h1', 'widget-search-overlay', 'span', 'style', 'span', 'span', 'span', 'span', 'section', 'span', 'span', 'span', 'span', 'span', 'span', 'span', 'span', 'span', 'span', 'span', 'span', 'p', 'a', 'h2', 'p', 'a', 'p', 'div', 'p', 'div', 'h2', 'img', 'p', 'span', 'p', 'span', 'p', 'span', 'p', 'span', 'p', 'span', 'span', 'p', 'a', 'h2', 'widget-content-slider', 'h2', 'p', 'p', 'p', 'a', 'button', 'button', 'span', 'p', 'div', 'p', 'button', 'span', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'button', 'p', 'span', 'span', 'span', 'span', 'span', 'span', 'span', 'p', 'span', 'span', 'span', 'span', 'span', 'span', 'span', 'p', 'span', 'span', 'span', 'span', 'span', 'span', 'span', 'script']
Tags not containing text: ['noscript', 'iframe', 'div', 'header', 'div', 'div', 'div', 'a', 'img', 'div', 'ul', 'li', 'a', 'li', 'i', 'li', 'a', 'i', 'li', 'i', 'div', 'div', 'div', 'i', 'div', 'button', 'i', 'div', 'div', 'i', 'div', 'span', 'button', 'i', 'div', 'div', 'i', 'div', 'button', 'i', 'div', 'div', 'i', 'div', 'button', 'i', 'main', 'section', 'div', 'div', 'div', 'section', 'div', 'div', 'div', 'div', 'a', 'i', 'section', 'div', 'div', 'section', 'div', 'div', 'div', 'i', 'div', 'div', 'i', 'div', 'div', 'i', 'div', 'div', 'i', 'div', 'div', 'div', 'div', 'div', 'div', 'ul', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'div', 'div', 'ul', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'section', 'div', 'div', 'div', 'div', 'div', 'widget-content-slider', 'div', 'div', 'div', 'div', 'div', 'div', 'a', 'div', 'div', 'div', 'span', 'i', 'div', 'div', 'div', 'div', 'div', 'div', 'a', 'div', 'div', 'div', 'div', 'i', 'div', 'a', 'div', 'div', 'div', 'img', 'div', 'i', 'div', 'div', 'div', 'a', 'div', 'div', 'div', 'img', 'div', 'i', 'div', 'a', 'div', 'div', 'div', 'img', 'div', 'i', 'div', 'a', 'div', 'div', 'div', 'img', 'div', 'i', 'div', 'a', 'i', 'div', 'div', 'widget-agenda', 'section', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'a', 'div', 'span', 'i', 'div', 'a', 'div', 'span', 'i', 'div', 'div', 'div', 'div', 'div', 'p', 'div', 'div', 'div', 'div', 'div', 'a', 'i', 'div', 'div', 'div', 'div', 'a', 'i', 'form', 'div', 'div', 'div', 'label', 'input', 'i', 'div', 'div', 'div', 'label', 'input', 'span', 'div', 'div', 'div', 'label', 'input', 'span', 'div', 'div', 'div', 'label', 'input', 'span', 'div', 'div', 'div', 'label', 'input', 'span', 'div', 'footer', 'div', 'section', 'div', 'div', 'div', 'div', 'ul', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'div', 'div', 'ul', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'div', 'div', 'div', 'div', 'ul', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'div', 'ul', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'section', 'div', 'div', 'div', 'ul', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'li', 'a', 'i', 'div', 'script', 'script', 'script']
Percentage of each type of tag containing text:
widget-navigation: 100.00%, text: 
widget-login: 100.00%, text: 
my-studychoice-authentication: 100.00%, text: 
h1: 100.00%, text: Aan de VU word je niet iets, maar iemand
widget-search-overlay: 100.00%, text: 
style: 100.00%, text: .vuw-hero {
        background-image: url("https://assets.vu.nl/d8b6f1f5-816c-005b-1dc1-e363dd7ce9a5/4e8b9c68-eb73-43dd-804f-fcc68845046e/RP_61_C%26M_Homepage_2200x720%5B41%5D.jpg");
    }
h2: 100.00%, text: Impact, Nieuws, Wij zijn de VU, Bekijk ook
p: 96.67%, text: Wil jij ook je wereld veranderen?, Accepteer sociale media cookies om deze content te zien, Oekraïne, Informatie en ondersteuning, 15 mei 2023, 26 apr. 2023, 04 mei 2023, 02 mei 2023, 25 apr. 2023, Werken bij de VU?, Studeren aan de VU, VU-campustour, Deze website maakt gebruik van cookies, Cookie-voorkeuren, U kunt alle cookies accepteren of per cookie-categorie uw voorkeur instellen. U kunt uw keuze later altijd veranderen door de cookies uit uw browser te verwijderen. Meer informatie vindt u in de cookieverklaring., Persoonlijke instellingen:, Functioneel, Deze cookies worden gebruikt om onze website naar behoren te laten functioneren., Analytisch, Deze cookies worden gebruikt om het gebruik van de website te meten (analyseren). Met deze meetgegevens worden statistieken gemaakt die wij gebruiken om de website te verbeteren., Personalisatie, Deze cookies worden gebruikt om te analyseren hoe u onze website gebruikt. Op basis hiervan kunnen wij de inhoud van onze website aanpassen met informatie die aansluit op uw interesses., Sociale media, Deze cookies worden geplaatst door sociale medianetwerken zoals Facebook, Twitter en LinkedIn. Bijvoorbeeld wanneer u een bericht deelt of liket via de social media buttons op onze website. De sociale medianetwerken kunnen hiermee uw internetgedrag zien en gebruiken voor eigen doeleinden., Advertenties, Deze cookies worden geplaatst door advertentiepartners. De cookies worden gebruikt om relevante advertenties van de VU te tonen op andere websites die u bezoekt. Met deze cookies kan uw internetgedrag gevolgd worden door advertentienetwerken., VU Hoofdmenu, Veel gezocht, Uitgelicht
span: 86.21%, text: EN, Sorry! The information you are looking for is only available in Dutch., Er is iets fout gegaan bij het uitvoeren van het verzoek., Er is iets fout gegaan bij het uitvoeren van het verzoek., Over de VU, 31.761 studenten, waarvan 6610 internationaal, 459 promoties, 9 faculteiten, Onderwijs, Bacheloropleidingen, Masteropleidingen, Onderwijs voor professionals, Honoursprogramma, VU Summer School, Onderzoek, Uitgelicht onderzoek, Onze wetenschappers, Valorisatie, Prijzen en onderscheidingen, Interdisciplinaire onderzoeksinstituten, Nina Polak nieuwe Vrije Schrijver van de VU, Verhalen spelen grote rol in ontwikkeling moreel bewustzijn studenten, CvB stelt Onderwijsagenda voor 2023-2028 vast, Gabriele Chlevickaite wint Praemium Erasmianum dissertatieprijs, KNAW kiest nieuwe leden, Overzicht nieuws, Cookieverklaring, Cookieverklaring, Home, Onderwijs, Onderzoek, Over de VU, Universiteitsbibliotheek, Persvoorlichting, Alumni, Contact, Personenzoeker, Bacheloropleidingen, Masteropleidingen, Opleidingen voor professionals, Faculteiten, Werken bij de VU, Privacy Verklaring, Disclaimer, Veiligheid, Webcolofon, Cookie Settings, Webarchief, Copyright © 2023 - Vrije Universiteit Amsterdam
button: 50.00%, text: Accepteer alle cookies, Stel mijn voorkeuren in, Accepteer alle cookies, Bewaren
widget-content-slider: 50.00%, text: 
script: 25.00%, text: $(document).foundation();
img: 16.67%, text: 
section: 11.11%, text: Empty section to create overlapping blocks
a: 7.94%, text: Mijn Studiekeuze., Bezoek de VU-bachelordag, Stel je cookie voorkeuren in, Bekijk onze vacatures!, Meer informatie over de cookies die wij gebruiken
div: 1.94%, text: Informatie en ondersteuning, , U kunt alle cookies accepteren of per cookie-categorie uw voorkeur instellen. U kunt uw keuze later altijd veranderen door de cookies uit uw browser te verwijderen. Meer informatie vindt u in de cookieverklaring.
noscript: 0.00%, text: 
iframe: 0.00%, text: 
header: 0.00%, text: 
ul: 0.00%, text: 
li: 0.00%, text: 
i: 0.00%, text: 
main: 0.00%, text: 
widget-agenda: 0.00%, text: 
form: 0.00%, text: 
label: 0.00%, text: 
input: 0.00%, text: 
footer: 0.00%, text: 

website 3.

Total tags: 947
Tags containing text: 362
Tags not containing text: 585
Percentage of tags containing text: 38.23%
Tags containing text: ['noscript', 'li', 'a', 'li', 'a', 'a', 'li', 'a', 'span', 'li', 'a', 'span', 'li', 'a', 'span', 'button', 'button', 'p', 'a', 'p', 'a', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'button', 'p', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'p', 'a', 'li', 'a', 'li', 'a', 'span', 'li', 'a', 'li', 'a', 'li', 'a', 'span', 'li', 'a', 'span', 'li', 'a', 'span', 'strong', 'strong', 'strong', 'strong', 'strong', 'strong', 'strong', 'strong', 'strong', 'strong', 'strong', 'div', 'strong', 'p', 'style', 'a', 'p', 'p', 'p', 'p', 'p', 'p', 'a', 'p', 'a', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'span', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'a', 'div', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'span', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'span', 'p', 'p', 'p', 'p', 'p', 'span', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'link', 'dt', 'li', 'a', 'li', 'a', 'dt', 'li', 'a', 'li', 'a', 'p', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'p', 'a', 'address', 'p', 'a', 'span', 'p', 'a', 'span', 'p', 'a', 'span', 'p', 'a', 'span', 'div', 'a', 'span', 'p', 'a', 'span', 'p', 'a', 'span', 'div', 'a', 'span', 'p', 'a', 'span', 'p', 'a', 'span', 'div', 'a', 'span', 'p', 'a', 'span', 'p', 'a', 'span', 'div', 'a', 'span', 'script']
Tags not containing text: ['noscript', 'iframe', 'div', 'header', 'div', 'h1', 'a', 'img', 'ul', 'div', 'span', 'a', 'img', 'div', 'ul', 'div', 'form', 'div', 'input', 'div', 'div', 'div', 'a', 'img', 'nav', 'div', 'ul', 'li', 'div', 'div', 'div', 'div', 'ul', 'div', 'ul', 'div', 'figure', 'img', 'li', 'div', 'div', 'div', 'div', 'ul', 'div', 'ul', 'div', 'figure', 'img', 'li', 'div', 'div', 'div', 'div', 'ul', 'div', 'ul', 'div', 'figure', 'img', 'li', 'div', 'div', 'div', 'div', 'ul', 'div', 'ul', 'div', 'figure', 'img', 'li', 'div', 'div', 'div', 'div', 'ul', 'div', 'ul', 'div', 'figure', 'img', 'li', 'div', 'div', 'div', 'div', 'ul', 'div', 'ul', 'div', 'figure', 'img', 'li', 'div', 'div', 'div', 'div', 'ul', 'div', 'ul', 'div', 'figure', 'img', 'p', 'div', 'div', 'div', 'div', 'form', 'input', 'nav', 'ul', 'ul', 'p', 'a', 'ul', 'li', 'a', 'img', 'div', 'ul', 'main', 'div', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'a', 'img', 'div', 'a', 'img', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'a', 'img', 'div', 'div', 'a', 'img', 'div', 'div', 'div', 'div', 'div', 'ul', 'li', 'span', 'img', 'div', 'div', 'div', 'div', 'div', 'div', 'ul', 'li', 'a', 'li', 'a', 'div', 'div', 'div', 'div', 'div', 'div', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'p', 'div', 'div', 'div', 'a', 'span', 'img', 'div', 'div', 'div', 'div', 'a', 'span', 'img', 'div', 'div', 'div', 'div', 'a', 'span', 'img', 'div', 'div', 'div', 'div', 'a', 'span', 'img', 'div', 'div', 'div', 'div', 'a', 'span', 'img', 'div', 'div', 'div', 'div', 'a', 'span', 'img', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'div', 'p', 'div', 'div', 'a', 'div', 'figure', 'img', 'div', 'div', 'div', 'div', 'div', 'figure', 'a', 'img', 'div', 'div', 'figure', 'a', 'img', 'div', 'div', 'figure', 'a', 'img', 'div', 'div', 'figure', 'a', 'img', 'div', 'div', 'div', 'p', 'div', 'div', 'div', 'a', 'p', 'img', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'p', 'br', 'figure', 'img', 'div', 'div', 'a', 'p', 'img', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'p', 'img', 'figure', 'img', 'div', 'div', 'a', 'p', 'br', 'img', 'figure', 'img', 'div', 'div', 'a', 'p', 'img', 'figure', 'img', 'div', 'div', 'a', 'figure', 'img', 'div', 'div', 'a', 'p', 'img', 'figure', 'img', 'div', 'div', 'a', 'p', 'img', 'figure', 'img', 'div', 'div', 'a', 'p', 'img', 'figure', 'img', 'div', 'div', 'a', 'p', 'img', 'div', 'div', 'a', 'div', 'div', 'div', 'div', 'p', 'ul', 'li', 'a', 'li', 'a', 'li', 'a', 'li', 'a', 'div', 'div', 'div', 'div', 'dl', 'dd', 'ul', 'li', 'a', 'img', 'li', 'a', 'img', 'li', 'a', 'img', 'div', 'dl', 'dd', 'ul', 'li', 'a', 'img', 'footer', 'div', 'div', 'ul', 'li', 'a', 'img', 'li', 'a', 'img', 'li', 'a', 'img', 'li', 'a', 'img', 'p', 'a', 'img', 'div', 'div', 'a', 'img', 'ul', 'li', 'a', 'img', 'li', 'a', 'img', 'p', 'br', 'div', 'div', 'img', 'div', 'div', 'img', 'div', 'div', 'img', 'div', 'div', 'img', 'script', 'script', 'script', 'script', 'script', 'script']
Percentage of each type of tag containing text:
button: 100.00%, text: Search, People, Search
strong: 100.00%, text: UTokyo Entrepreneurs Series, UTokyo President’s Log, UTokyo WAY 2022-2023, Center for Global Education, Insight and analysis, UTokyo Compass, UTokyo Entrepreneurs Series, UTokyo President’s Log, UTokyo WAY 2022-2023, Center for Global Education, Insight and analysis, UTokyo Compass
style: 100.00%, text: <!--

ul.c-list__none-dot{
margin-bottom: 0px;
}

ul.c-list__none-dot li{
margin-bottom: 0px;
}

ul.c-list__none-dot li a{
border-bottom: 1px dashed #0d3d63;
color: #0d3d63;
}

ul.c-list__none-dot li a:hover{
text-decoration: none;
border-bottom: none;
}

-->
link: 100.00%, text: 
dt: 100.00%, text: University Facilities, Compliance
address: 100.00%, text: © The University of Tokyo
p: 84.62%, text: HOME, Education, People, Education, COVID-19 Response, NOTICES, May 8, 2023, Task Force Message: “Message for UTokyo students: Lowering of the activity restriction guideline level at the University of Tokyo”, May 8, 2023, Task Force Message: “Message for UTokyo staff: Lowering of the activity restriction guideline level at the University of Tokyo”, UTokyo FOCUS, Alerts, Twin sisters deliver “more fun!” experiences to entertainment, May 17, 2023, UTokyo Research, The evolution of honey bee brains, May 8, 2023, Science and Technology, Dark clouds on the horizon, May 3, 2023, Science and Technology, LincRNA paints a target on diseased tissues, April 27, 2023, Medicine and Health, Better social drinkers don’t earn more, April 25, 2023, Social Sciences, Education and outreach to create a sustainable society, April 21, 2023, International, Making AI convenient, but also safe, ethical, April 20, 2023, Science and Technology, May 22, 2023, Google-UChicago-UTokyo Quantum Workshop, Online, June 17, 2023, Building Your Future in Information Science and Technology —Explore Career Development and..., Hongo Area Campus, In-person and online, May 22, 2023, A dialogue with Secretary General Ou Boqian, Trilateral Cooperation Secretariat: “Shared f..., Hongo Area Campus, May 27, 2023, GO GLOBAL UTokyo Study Abroad Fair 2023, Komaba Area Campus, June 5, 2023, World Environment Day “The Lives, Deaths and Afterlives of Plastic: Global Perspectives”, Online, April 29, 2023—September 3, 2023, Special Exhibition “Tokyo Ephemera”, Other campuses/off-campus, Event calendar, HIGHLIGHTS, UTokyo Compass, UTokyo FSI, Message from the President, Tokyo College, Explore Our Campuses, Learn, Diversity & Inclusion, Green Transformation, UTokyo WAY, Tansei, UTokyo Outline, Term Dates and University Calendar, Featured Book, Gendaigo Bunpou Gai..., IJIMA Masahiro (author and editor), In recent years, rather than providing an all-encompassing theory of Japanese grammar, studies of Japanese grammar in modern language have become increasingly fragmented into different research fields...[Read more], Introducing UTokyo Compass, Message from President Fujii, UTokyo FSI video, Participation in "Race to Zero", UTokyo FSI, Undergraduate Programs in English, Graduate Degree Programs in English, List of Overseas Offices, Earthquake Response, May 10, 2023, Statements from President Fujii, May 10, 2023, Congratulatory Addresses at Matriculation Ceremonies and Commencements, May 10, 2023, Address by the President of the University of Tokyo for the 2022 Spring Semester Diploma Presentation Ceremony [Translated Version], May 8, 2023, Message for UTokyo students: Reduction of the UTokyo Activity Restrictions Index Level to Level S, Disseminating information for UTokyo during disasters, Access and campus maps, Kashiwa Campus, Hongo Campus, Komaba Campus, Access and Campus Maps, Back, Access and Campus Maps, Back, Access and Campus Maps, Back, Access and Campus Maps
li: 78.07%, text: Skip to content, Contact, 日本語, 中文, 한국어, Office of the President, Mission and Vision, History, Facts and Figures, Offices & Administration, Publications & PR, Visit UTokyo, Access and Campus Maps, Facilities, Rules and Regulations, Job Information, Faculties, Graduate Schools, Institutes and Other University Organizations, Special Educational Activities, Research Activities, International Activities, Explore Our Campuses, Learn, Discover Our People, In Depth, Why Tokyo?, Why Japan?, UTokyo FOCUS, Research from Graduate Schools, Institutes and Other Organizations, University-wide Research Activities, Research Cooperation with Industries, Research at UTokyo, News & Topics, UTokyo Alumni Association, Connect, Learn, Support for Students, Contribute, Publications Including Online Media, Bulletin Board, Services and Benefits, Obtaining Certificates of Student Status, Certificates of Graduation, and Transcripts, Term Dates and University Calendar, Why UTokyo?, Undergraduate Students, Graduate Students, Student Exchange Programs, Special and Short-term Programs, Housing, Tuition and Scholarships, Student Support, Guide for International Students UTokyo, News/Notices & Events, Procedures for Entering and Residing in Japan, Housing, Health and Safety, Tuition and Scholarships, Career Support for Students, Studying Japanese, Studying Abroad, On-campus Services for International Students and Researchers, University-wide Student Exchange Program (USTEP) Type U, Support for Family Members in Japan, Rules and Regulations, Term Dates and University Calendar, Ceremonies, HOME, About UTokyo, Academics, Why UTokyo?, Research, Alumni, Prospective Students, Current Students, Access and Campus Maps, Contact, 日本語, 中文, 한국어, Museums, The University of Tokyo Archives (Japanese), Information on Compliance, Social media directory, Site map, Site policy, Privacy policy, Jobs, Frequently asked questions
span: 75.76%, text: 日本語, 中文, 한국어, FOCUS, 日本語, 中文, 한국어, EVENTS, MEDIA, INITIATIVES, UPDATES, Kashiwa Campus, Hongo Campus, Komaba Campus, Access and Campus Maps, Close, Back, Access and Campus Maps, Close, Back, Access and Campus Maps, Close, Back, Access and Campus Maps, Close
a: 59.61%, text: Skip to content, Contact, Language, 日本語, 中文, 한국어, HOME, Education, About UTokyo, Office of the President, Mission and Vision, History, Facts and Figures, Offices & Administration, Publications & PR, Visit UTokyo, Access and Campus Maps, Facilities, Rules and Regulations, Job Information, Academics, Faculties, Graduate Schools, Institutes and Other University Organizations, Special Educational Activities, Research Activities, International Activities, Why UTokyo?, Explore Our Campuses, Learn, Discover Our People, In Depth, Why Tokyo?, Why Japan?, Research, UTokyo FOCUS, Research from Graduate Schools, Institutes and Other Organizations, University-wide Research Activities, Research Cooperation with Industries, Research at UTokyo, Alumni, News & Topics, UTokyo Alumni Association, Connect, Learn, Support for Students, Contribute, Publications Including Online Media, Bulletin Board, Services and Benefits, Obtaining Certificates of Student Status, Certificates of Graduation, and Transcripts, Term Dates and University Calendar, Prospective Students, Why UTokyo?, Undergraduate Students, Graduate Students, Student Exchange Programs, Special and Short-term Programs, Housing, Tuition and Scholarships, Student Support, Guide for International Students UTokyo, Current Students, News/Notices & Events, Procedures for Entering and Residing in Japan, Housing, Health and Safety, Tuition and Scholarships, Career Support for Students, Studying Japanese, Studying Abroad, On-campus Services for International Students and Researchers, University-wide Student Exchange Program (USTEP) Type U, Support for Family Members in Japan, Rules and Regulations, Term Dates and University Calendar, Ceremonies, People, HOME, About UTokyo, Academics, Why UTokyo?, Research, Alumni, Education, Prospective Students, Current Students, Access and Campus Maps, Contact, 日本語, 中文, 한국어, University Response to Coronavirus Disease 2019 (COVID-19), UTokyo FOCUS, Alerts, Event calendar, Museums, The University of Tokyo Archives (Japanese), Information on Compliance, Social media directory, Disseminating information for UTokyo during disasters, Site map, Site policy, Privacy policy, Jobs, Frequently asked questions, Access and campus maps, Kashiwa Campus, Hongo Campus, Komaba Campus, Access and Campus Maps, Close, Back, Access and Campus Maps, Close, Back, Access and Campus Maps, Close, Back, Access and Campus Maps, Close
noscript: 50.00%, text: JavaScript is required to display the University of Tokyo website correctly. Please enable JavaScript in your browser settings and refresh the page.
script: 14.29%, text: $(window).load(function() {
                $('.imgList01').equalize('width');
                $('.imgList01').equalize();
        });
div: 2.26%, text: The University of Tokyo celebrates the 150th anniversary of its founding in 2027, HIGHLIGHTS, Close, Close, Close, Close
iframe: 0.00%, text: 
header: 0.00%, text: 
h1: 0.00%, text: 
img: 0.00%, text: 
ul: 0.00%, text: 
form: 0.00%, text: 
input: 0.00%, text: 
nav: 0.00%, text: 
figure: 0.00%, text: 
main: 0.00%, text: 
br: 0.00%, text: 
dl: 0.00%, text: 
dd: 0.00%, text: 
footer: 0.00%, text:

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
title: 100.00%, text: The Weather Channel, Search, Globe, Arrow down, Arrow Down, Arrow Down, Arrow Down, Arrow Down, Arrow Down, External Link, External Link, External Link, External Link, External Link, External Link, Arrow Left, Arrow Right, Air Quality, Arrow down, External Link, Video, Video, Video, Video, Video, Video, Video, Video, Video, Video, Video, Video, Video, Video, Video, Video, Video, Video, The Weather Company, The Weather Channel, Weather Underground, Ad Choices, Georgia, eSSENTIAL Accessibility, IBM Cloud, Hidden Weather Icon Masks, Hidden Weather Icon Symbols
legend: 100.00%, text: Type at least three characters to start auto complete. Recently searched locations will be displayed if there is no search query. The first option will be automatically selected. Use up and down arrows to change selection. Use escape to clear.
label: 100.00%, text: Search City or Zip Code
h2: 100.00%, text: recents, WHEN WILL THE SMOKE CLEAR?, What Else Is Happening?, Weather Today Across the Country, Fighting Your Allergies, It's Official, El Niño Is Here, Stay Safe, Protecting Yourself From Smoke
h3: 100.00%, text: Specialty Forecasts, Code Red Alerts
p: 100.00%, text: We recognize our responsibility to use data and technology for good. Take control of your data., © Copyright TWC Product and Technology LLC 2014, 2023
tspan: 100.00%, text: IBM, Cloud
li: 93.75%, text: °F, °C, Hybrid, Feedback, Careers, Press Room, Advertise With Us, TV, Newsletter Sign Up, Terms of Use, Privacy Policy, Accessibility Statement, Data Vendors, Privacy Settings, Data Rights
span: 92.16%, text: US, °F, Weather, radar, Severe, Video & Photos, Health & Activities, TV & Weather, Weather Products, Privacy, Today, Hourly, 10 Day, Weekend, Monthly, Radar, Smoke, More Forecasts, More, Allergy Tracker, Fishing, Cold & Flu, Air Quality Forecast, Extremely Poor Air Quality Continues; Fears Of Health Damage, Time-Lapse Shows How Quickly New York City Turned Orange, Watch NYC Skyline Go From Gray To Shocking Scarlet, What's Behind Canada's Devastating Wildfires?, Air Quality Concerns: NY Schools Go Remote, Special Olympics Cancelled In PA, What Is This Smoke Doing To Your Body?, NYC Haze Before-And-After Shows Smoke's Incredible Scale, Can You Escape The Smoke Here?, Here's How It Feels To Be In NYC Right Now, Make Your Own Home Air Purifier, Severe Storms With Large Hail Possible To Start Weekend, Rare Lunar Rainbows Spotted At Yosemite Waterfalls, Astounding Images Of Latest Kīlauea Eruption, K-9 Dies In Hot Car During Training Exercise, Spring Cleaning: How To Remove Winter’s Leftover Mold, Is It Allergies, A Cold Or COVID?, 6 Easy Ways To Allergy-Proof Your Home, 5 Reasons Your Allergies Could Be Worse At Night, What It Means For Your Forecast, Experts Say This Is The Best Mask, AdChoices, Privacy Settings, © Copyright TWC Product and Technology LLC 2014, 2023, Powered by the
a: 87.71%, text: Skip to Main Content, Accessibility Help, Antigua and Barbuda | English, Argentina | Español, Bahamas | English, Barbados | English, Belize | English, Bolivia | Español, Brazil | Português, Canada | English, Canada | Français, Chile | Español, Colombia | Español, Costa Rica | Español, Dominica | English, Dominican Republic | Español, Ecuador | Español, El Salvador | Español, Grenada | English, Guatemala | Español, Guyana | English, Haiti | Français, Honduras | Español, Jamaica | English, Mexico | Español, Nicaragua | Español, Panama | Español, Panama | English, Paraguay | Español, Peru | Español, St. Kitts and Nevis | English, St. Lucia | English, St. Vincent and the Grenadines | English, Suriname | Nederlands, Trinidad and Tobago | English, Uruguay | Español, United States | English, United States | Español, Venezuela | Español, Algeria | العربية, Algeria | Français, Angola | Português, Benin | Français, Burkina Faso | Français, Burundi | Français, Cameroon | Français, Cameroon | English, Cape Verde | Português, Central African Republic | Français, Chad | Français, Chad | العربية, Comoros | Français, Comoros | العربية, Democratic Republic of the Congo | Français, Republic of Congo | Français, Côte d'Ivoire | Français, Djibouti | Français, Djibouti | العربية, Egypt | العربية, Equatorial Guinea | Español, Eritrea | العربية, Gabon | Français, Gambia | English, Ghana | English, Guinea | Français, Guinea-Bissau | Português, Kenya | English, Lesotho | English, Liberia | English, Libya | العربية, Madagascar | Français, Mali | Français, Mauritania | العربية, Mauritius | English, Mauritius | Français, Morocco | العربية, Morocco | Français, Mozambique | Português, Namibia | English, Niger | Français, Nigeria | English, Rwanda | Français, Rwanda | English, Sao Tome and Principe | Português, Senegal | Français, Sierra Leone | English, Somalia | العربية, South Africa | English, South Sudan | English, Sudan | العربية, Swaziland | English, Tanzania | English, Togo | Français, Tunisia | العربية, Uganda | English, Australia | English, Bangladesh | বাংলা, Brunei | Bahasa Melayu, China | 中文, Hong Kong SAR | 中文, East Timor | Português, Fiji | English, India (English) | English, India (Hindi) | हिन्दी, Indonesia | Bahasa Indonesia, Japan | 日本語, Kiribati | English, South Korea | 한국어, Kyrgyzstan | Русский, Malaysia | Bahasa Melayu, Marshall Islands | English, Micronesia | English, New Zealand | English, Palau | English, Philippines | English, Philippines | Tagalog, Samoa | English, Singapore | English, Singapore | 中文, Solomon Islands | English, Taiwan | 中文, Thailand | ไทย, Tonga | English, Tuvalu | English, Vanuatu | English, Vanuatu | Français, Vietnam | Tiếng Việt, Andorra | Català, Andorra | Français, Austria | Deutsch, Belarus | Русский, Belgium | Dutch, Belgium | Français, Bosnia and Herzegovina | Hrvatski, Croatia | Hrvatski, Cyprus | Ελληνικά, Czech Republic | Čeština, Denmark | Dansk, Estonia | Русский, Estonia | Eesti, Finland | Suomi, France | Français, Germany | Deutsch, Greece | Ελληνικά, Hungary | Magyar, Ireland | English, Italy | Italiano, Liechtenstein | Deutsch, Luxembourg | Français, Malta | English, Monaco | Français, Netherlands | Nederlands, Norway | Norsk, Poland | Polski, Portugal | Português, Romania | Română, Russia | Русский, San Marino | Italiano, Slovakia | Slovenčina, Spain | Español, Spain | Català, Sweden | Svenska, Switzerland | Deutsch, Turkey | Turkçe, Ukraine | Українська, United Kingdom | English, State of Vatican City (Holy See) | Italiano, Bahrain | العربية, Iran |  فارسى, Iraq | العربية, Israel | עִבְרִית, Jordan | العربية, Kuwait | العربية, Lebanon | العربية, Oman | العربية, Pakistan |  اردو, Pakistan | English, Qatar | العربية, Saudi Arabia | العربية, Syria | العربية, United Arab Emirates | العربية, Today, Hourly, 10 Day, Weekend, Monthly, Radar, Allergy Tracker, Fishing, Cold & Flu, Air Quality Forecast, WHEN WILL THE SMOKE CLEAR?, See More, More News, Read More, See More, Feedback, Careers, Press Room, Advertise With Us, TV, Newsletter Sign Up, Terms of Use, Privacy Policy, Accessibility Statement, Data Vendors, Data Rights
header: 75.00%, text: What Else Is Happening?, Weather Today Across the Country, Fighting Your Allergies, It's Official, El Niño Is Here, Stay Safe, Protecting Yourself From Smoke
button: 71.88%, text: Today's Forecast, Hourly Forecast, Weekend Forecast, Monthly Forecast, National Forecast, National News, Almanac, Weather in Motion®, Radar Maps, Classic Weather Maps, Regional Satellite, Severe Alerts, Safety & Preparedness, Hurricane Central, Top Stories, Video, Photos, Allergy Tracker, Cold & Flu, Air Quality Forecast, Seasonal Deals, Data Rights, Privacy Policy
footer: 57.14%, text: See More, More News, Read More, See More
div: 18.34%, text: Advertisement, recents, You have no recent locations, Imperial - F / mph / miles / inches, Imperial - F / mph / miles / inches, Advertisement, Advertisement, Extremely Poor Air Quality Continues; Fears Of Health Damage, Extremely Poor Air Quality Continues; Fears Of Health Damage, Time-Lapse Shows How Quickly New York City Turned Orange, Time-Lapse Shows How Quickly New York City Turned Orange, Watch NYC Skyline Go From Gray To Shocking Scarlet, Watch NYC Skyline Go From Gray To Shocking Scarlet, What's Behind Canada's Devastating Wildfires?, What's Behind Canada's Devastating Wildfires?, Air Quality Concerns: NY Schools Go Remote, Special Olympics Cancelled In PA, Air Quality Concerns: NY Schools Go Remote, Special Olympics Cancelled In PA, See More, Severe Weather, Severe Storms With Large Hail Possible To Start Weekend, Severe Storms With Large Hail Possible To Start Weekend, Nature, Rare Lunar Rainbows Spotted At Yosemite Waterfalls, Rare Lunar Rainbows Spotted At Yosemite Waterfalls, Photos, Astounding Images Of Latest Kīlauea Eruption, Astounding Images Of Latest Kīlauea Eruption, Pets, K-9 Dies In Hot Car During Training Exercise, K-9 Dies In Hot Car During Training Exercise, More News, Advertisement, Read More, Advertisement, Advertisement, Spring Cleaning: How To Remove Winter’s Leftover Mold, Spring Cleaning: How To Remove Winter’s Leftover Mold, Is It Allergies, A Cold Or COVID?, Is It Allergies, A Cold Or COVID?, 6 Easy Ways To Allergy-Proof Your Home, 6 Easy Ways To Allergy-Proof Your Home, 5 Reasons Your Allergies Could Be Worse At Night, 5 Reasons Your Allergies Could Be Worse At Night, See More, Advertisement, What It Means For Your Forecast, What It Means For Your Forecast, Advertisement, Advertisement, Experts Say This Is The Best Mask, Experts Say This Is The Best Mask, Advertisement, Advertisement
svg: 0.00%, text: 
path: 0.00%, text: 
img: 0.00%, text: 
form: 0.00%, text: 
fieldset: 0.00%, text: 
input: 0.00%, text: 
nav: 0.00%, text: 
section: 0.00%, text: 
ul: 0.00%, text: 
details: 0.00%, text: 
summary: 0.00%, text: 
g: 0.00%, text: 
circle: 0.00%, text: 
main: 0.00%, text: 
noscript: 0.00%, text: 
rect: 0.00%, text: 
aside: 0.00%, text: 
defs: 0.00%, text: 
lineargradient: 0.00%, text: 
stop: 0.00%, text: 
text: 0.00%, text: 
image: 0.00%, text: 
mask: 0.00%, text: 
use: 0.00%, text: 
symbol: 0.00%, text: 

website 10.

Total tags: 247
Tags containing text: 92
Tags not containing text: 155
Percentage of tags containing text: 37.25%
Tags containing text: ['script', 'a', 'span', 'span', 'a', 'a', 'a', 'a', 'a', 'a', 'label', 'button', 'a', 'a', 'a', 'h2', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h1', 'div', 'h2', 'h3', 'img', 'p', 'h3', 'span', 'p', 'h3', 'small', 'p', 'h2', 'h3', 'span', 'p', 'h3', 'span', 'p', 'h3', 'span', 'p', 'h3', 'span', 'p', 'h3', 'span', 'p', 'h3', 'span', 'p', 'a', 'text', 'text', 'text', 'h2', 'a', 'a', 'a', 'a', 'a', 'h2', 'a', 'a', 'a', 'a', 'a', 'p', 'li', 'a', 'a', 'a']
Tags not containing text: ['noscript', 'iframe', 'div', 'header', 'div', 'div', 'div', 'figure', 'img', 'figcaption', 'div', 'div', 'nav', 'nav', 'ul', 'li', 'li', 'li', 'li', 'li', 'div', 'form', 'input', 'main', 'div', 'div', 'div', 'ul', 'li', 'li', 'li', 'div', 'figure', 'picture', 'source', 'source', 'img', 'div', 'div', 'nav', 'div', 'ul', 'li', 'a', 'div', 'li', 'a', 'div', 'li', 'a', 'div', 'li', 'a', 'div', 'li', 'a', 'div', 'li', 'a', 'div', 'li', 'a', 'div', 'li', 'a', 'div', 'li', 'a', 'div', 'li', 'a', 'div', 'li', 'a', 'div', 'li', 'a', 'div', 'div', 'div', 'section', 'div', 'a', 'div', 'figure', 'div', 'div', 'a', 'div', 'figure', 'img', 'footer', 'small', 'div', 'div', 'a', 'div', 'figure', 'img', 'footer', 'div', 'section', 'div', 'a', 'div', 'p', 'div', 'a', 'div', 'p', 'div', 'a', 'div', 'p', 'div', 'a', 'div', 'p', 'div', 'a', 'div', 'p', 'div', 'a', 'div', 'p', 'aside', 'div', 'a', 'svg', 'rect', 'footer', 'div', 'div', 'ul', 'li', 'li', 'li', 'li', 'li', 'div', 'ul', 'li', 'li', 'li', 'li', 'li', 'nav', 'div', 'ul', 'li', 'li', 'li', 'script', 'script']
Percentage of each type of tag containing text:
span: 100.00%, text: Government of the Netherlands, You are here:, Image: ©, 05-06-2023 | 16:10, 31-05-2023 | 16:23, 31-05-2023 | 13:00, 31-05-2023 | 11:26, 30-05-2023 | 16:00, 30-05-2023 | 10:30
label: 100.00%, text: Search within English part of Government.nl
button: 100.00%, text: Search
h2: 100.00%, text: Main menu, Spotlight, News, Service, About this site
h3: 100.00%, text: Building and housing, Economy, Education, Family, health and care, Government and democracy, International cooperation, Justice, security and defence, Migration and travel, Nature and the environment, Taxes, benefits and allowances, Transport, Work, Requirements for photos, Travelling with minors, How to become a Dutch citizen, Expo 2025 Osaka: design of the Netherlands Pavilion unveiled, Netherlands leads the way in Europe with bill for the Minimum Tax Rate Act 2024 (implementing ‘Pillar Two’), Measures in women’s prisons after inspection report Nieuwersluis PI, Africa Strategy: government presents integrated approach to cooperation with Africa, Threat assessment NCTV: terrorist threat to the Netherlands increased, Highlights of a year of feminist foreign policy
h1: 100.00%, text: Information from the Government of the Netherlands
text: 100.00%, text: Questions?, Contact the Public, Information Service
p: 78.57%, text: Housing, Infrastructure, Population decline..., Enterprise and innovation, Brexit, Biotechnology, Intellectual property ..., School holidays, Higher education ..., Coronavirus Covid-19, Drugs, Health insurance, Abortion, Mental health care, Family law ..., Public administration, Personal data, Police , Democracy ..., European Union, Human rights, Treaties ..., War in Ukraine, Identification documents, Emergency number 112, Counterterrorism and national security, Child abuse ..., Reception of refugees from Ukraine, Visas, Dutch nationality, Immigration, Embassies, consulates and other representations ..., Climate change, Environment, Water management ..., Taxation and businesses, Income tax, Grant programmes ..., Driving licence, Mobility, Vehicles, Drones ..., Minimum wage, Legalising documents, Working conditions, Migrant workers ..., Photos for passports, identity cards and driving licences must meet certain requirements., Do you intend to travel outside the Netherlands with a child over whom you do not have parental authority? Please use this consent letter., Find out more about how to become a Dutch citizen., The Netherlands has announced its participation in Expo 2025 Osaka, Kansai, Japan. The Netherlands Pavilion is unique in that it ..., The bill for the proposed Minimum Tax Rate Act 2024 was presented today to the House of Representatives of the Dutch parliament. ..., Minister for Legal Protection Franc Weerwind and the Custodial Institutions Agency (DJI) are taking measures to tackle ..., The Netherlands is sharpening the focus of its collaboration with Africa by investing more, more specifically, and more ..., The terrorist threat for the Netherlands has increased over the past half year. There are increasingly more signals that jihadist ..., The Netherlands seeks to reduce inequality, and it is committed to promoting the equality of men, women and LGBTIQ+ people all ..., This website in other languages:
a: 52.17%, text: Go to content, Home, Latest, Topics, Ministries, Government, Documents, Travelling to the Netherlands, Public holidays in the Netherlands, Amount of the minimum wage, More news, Contact, RSS, Sitemap, Help, Archive, Copyright, Privacy, Cookies, Accessibility, Report vulnerability, Nederlands, Papiamento, Papiamentu
small: 50.00%, text: Image: Henriette Guest
script: 33.33%, text: (function(window, document, dataLayerName, id) {
            window[dataLayerName]=window[dataLayerName]||[],window[dataLayerName].push({start:(new Date).getTime(),event:"stg.start"});var scripts=document.getElementsByTagName('script')[0],tags=document.createElement('script');
            function stgCreateCookie(a,b,c){var d="";if(c){var e=new Date;e.setTime(e.getTime()+24*c*60*60*1e3),d="; expires="+e.toUTCString()}document.cookie=a+"="+b+d+"; path=/"}
            var isStgDebug=(window.location.href.match("stg_debug")||document.cookie.match("stg_debug"))&&!window.location.href.match("stg_disable_debug");stgCreateCookie("stg_debug",isStgDebug?1:"",isStgDebug?14:-1);
            var qP=[];dataLayerName!=="dataLayer"&&qP.push("data_layer_name="+dataLayerName),isStgDebug&&qP.push("stg_debug");var qPString=qP.length>0?("?"+qP.join("&")):"";
            tags.async=!0,tags.src="//statistiek.rijksoverheid.nl/containers/"+id+".js"+qPString,scripts.parentNode.insertBefore(tags,scripts);
            !function(a,n,i){a[n]=a[n]||{};for(var c=0;c<i.length;c++)!function(i){a[n][i]=a[n][i]||{},a[n][i].api=a[n][i].api||function(){var a=[].slice.call(arguments,0);"string"==typeof a[0]&&window[dataLayerName].push({event:n+"."+i+":"+a[0],parameters:[].slice.call(arguments,1)})}}(i[c])}(window,"ppms",["tm","cm"]);
          })(window, document, 'dataLayer', '17953060-0014-4821-b579-e7b24c408376');
img: 20.00%, text: 
li: 2.94%, text: English
div: 1.82%, text: 
noscript: 0.00%, text: 
iframe: 0.00%, text: 
header: 0.00%, text: 
figure: 0.00%, text: 
figcaption: 0.00%, text: 
nav: 0.00%, text: 
ul: 0.00%, text: 
form: 0.00%, text: 
input: 0.00%, text: 
main: 0.00%, text: 
picture: 0.00%, text: 
source: 0.00%, text: 
section: 0.00%, text: 
footer: 0.00%, text: 
aside: 0.00%, text: 
svg: 0.00%, text: 
rect: 0.00%, text: 
"""