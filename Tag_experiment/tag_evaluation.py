import requests
from bs4 import BeautifulSoup

# https://hikouki0408.github.io/portfolio 
# https://www.amazon.nl/-/en

def remove_css_scripts(tag):
    # Remove <style> and <script> tags from the given tag
    for css_script_tag in tag.find_all(['style', 'script']):
        css_script_tag.decompose()

def get_tag_text(tag):
    if isinstance(tag, str):
        return tag.strip()
    if tag.name in ['style', 'script']:
        return ''
    if tag.string:
        return tag.string.strip()
    else:
        return ''.join(get_tag_text(child) for child in tag.contents if isinstance(child, str) or child.name not in ['style', 'script'])
    
# 1. https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam
# 2. https://stackoverflow.blog/2023/05/31/ceo-update-paving-the-road-forward-with-ai-and-community-at-the-center
# 3. https://www.euronews.com/travel/2023/02/27/long-queues-and-scams-will-the-new-eu-entry-system-cause-border-chaos
# 4. https://www.tudelftcampus.nl/time-to-shake-up-the-pile-driving-industry
# 5  https://vu.nl/nl
# 6  https://www.u-tokyo.ac.jp/en/
# 7  https://weather.com/?Goto=Redirected
# 8  https://www.billboard.com/
# 9  https://www.government.nl/
# 10 https://www.cntraveller.com/gallery/beautiful-places-amsterdam

url = 'https://www.cntraveller.com/gallery/beautiful-places-amsterdam'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
body = soup.find('body') # for <head>  body = soup.find('head')
tags = body.find_all(lambda tag: tag.name not in ['style', 'script'])

text_tags = 0
non_text_tags = 0
text_tag_list = []
non_text_tag_list = []
tag_counts = {}
text_counts = {}
tag_texts = {}

for tag in tags:
    if tag.name[0] != '/':  # Only count opening tags
        remove_css_scripts(tag)  # Call the function to remove CSS and script tags
        tag_text = get_tag_text(tag)
        if tag_text:
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
                tag_texts[tag.name].append(tag_text)
            else:
                tag_texts[tag.name] = [tag_text]
        else:
            non_text_tags += 1
            non_text_tag_list.append(tag.name)
            if tag.name in tag_counts:
                tag_counts[tag.name] += 1
            else:
                tag_counts[tag.name] = 1

total_tags = text_tags + non_text_tags
text_percentage = (text_tags / total_tags) * 100

text_percentages = {}
for tag, count in tag_counts.items():
    if tag in text_counts:
        text_percentages[tag] = (text_counts[tag] / count) * 100
    else:
        text_percentages[tag] = 0

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
    
    if tag == 'form' or tag == 'input' or tag == 'button' or tag == 'footer' or tag == 'nav' or tag == 'svg' or tag == 'figure' or tag == 'figcaption':
        print(f'{tag}: {percentage:.2f}% [TAG! HERE], text: {text}')
    else:
        #print(f'{tag}: {percentage:.2f}%')
        print(f'{tag}: {percentage:.2f}% [TAG! HERE], text: {text}')
    

"""
website_1:
Percentage of each type of tag containing text:
header: 100.00%
button: 100.00% [TAG! HERE], text: move to sidebar, hide, Search, move to sidebar, hide, Toggle History subsection, Toggle Campus and academic life subsection, Toggle Academic profile subsection, move to sidebar, hide, Toggle limited content width
form: 100.00% [TAG! HERE], text: Search
h2: 100.00%
main: 100.00%
h1: 100.00%
table: 100.00%
caption: 100.00%
i: 100.00%
tbody: 100.00%
sup: 100.00%
p: 100.00%
b: 100.00%
meta: 100.00%
figure: 100.00%
figcaption: 100.00%
h3: 100.00%
ol: 100.00%
cite: 100.00%
abbr: 100.00%
footer: 100.00% [TAG! HERE], text: This page was last edited on 21 July 2023, at 19:07(UTC).Text is available under theCreative Commons Attribution-ShareAlike License 4.0;
additional terms may apply.  By using this site, you agree to theTerms of UseandPrivacy Policy. Wikipedia® is a registered trademark of theWikimedia Foundation, Inc., a non-profit organization.Privacy policyAbout WikipediaDisclaimersContact WikipediaCode of ConductMobile viewDevelopersStatisticsCookie statement
li: 99.44%
th: 97.37%
td: 97.22%
a: 96.91%
tr: 95.24%
div: 89.31%
span: 84.95%
nav: 77.78% [TAG! HERE], text: Main menuMain menumove to sidebarhideNavigationMain pageContentsCurrent eventsRandom articleAbout WikipediaContact usDonateContributeHelpLearn to editCommunity portalRecent changesUpload fileLanguagesLanguage links are at the top of the page across from the title., Create accountLog inPersonal toolsCreate accountLog inPages for logged out editorslearn moreContributionsTalk, Contentsmove to sidebarhide(Top)1HistoryToggle History subsection1.1Origins (1880)1.2Expansion (1900s–1960s)1.3Change (1970s-2000s)1.4Expansion and reform (2000s–present)2Campus and academic lifeToggle Campus and academic life subsection2.1Buitenveldert2.2Uilenstede3Organizational structure4Academic profileToggle Academic profile subsection4.1University rankings5Research6University newspaper7Notable faculty8Notable past faculty9Notable alumni10See also11Notes12References13External links, Toggle the table of contents, ArticleTalkEnglish, ReadEditView history, ToolsToolsmove to sidebarhideActionsReadEditView historyGeneralWhat links hereRelated changesUpload fileSpecial pagesPermanent linkPage informationCite this pageWikidata itemPrint/exportDownload as PDFPrintable versionIn other projectsWikimedia Commons
ul: 68.33%
input: 33.33% [TAG! HERE], text: Personal toolsCreate accountLog inPages for logged out editorslearn moreContributionsTalk, Toggle the table of contents, 35 languagesAfrikaansالعربيةБеларускаяCatalàDeutschEestiEspañolEsperantoفارسیFøroysktFrançaisFrysk한국어ՀայերենBahasa IndonesiaItalianoעבריתLatinaمصرىNederlands日本語Norsk bokmålOʻzbekcha / ўзбекчаپنجابیPolskiPortuguêsРусскийSimple EnglishSuomiSvenskaTagalogไทยУкраїнськаاردو中文Edit links
label: 14.29%
img: 0.00%
br: 0.00%
link: 0.00%
noscript: 0.00%

Webiste_2:
Percentage of each type of tag containing text:
header: 100.00%
nav: 100.00% [TAG! HERE], text: Search for:, LatestNewsletterPodcastCompany
form: 100.00% [TAG! HERE], text: Search for:, Your email address will not be published.Required fields are marked*Comment*Name*Email*WebsiteSave my name, email, and website in this browser for the next time I comment.Δ
label: 100.00%
span: 100.00%
section: 100.00%
article: 100.00%
h1: 100.00%
h2: 100.00%
blockquote: 100.00%
strong: 100.00%
em: 100.00%
figcaption: 100.00%
h3: 100.00%
small: 100.00%
footer: 100.00% [TAG! HERE], text: © 2023 All Rights Reserved.Proudly powered byWordPressStack OverflowAboutPressWork HereContact UsQuestionsProductsTeamsAdvertisingCollectivesTalentPoliciesLegalPrivacy PolicyTerms of ServiceCookie SettingsCookie PolicyChannelsBlogPodcastNewsletterTwitterLinkedInInstagram
p: 92.68%
a: 83.82%
div: 77.05%
figure: 25.00%
noscript: 0.00%
iframe: 0.00%
img: 0.00%
svg: 0.00% [TAG! HERE], text: 
path: 0.00%
input: 0.00% [TAG! HERE], text: 
button: 0.00% [TAG! HERE], text: 
textarea: 0.00%
br: 0.00%

Website_3
Percentage of each type of tag containing text:
template: 100.00%
b: 100.00%
header: 100.00%
nav: 100.00% [TAG! HERE], text: NewsDestinationsExperiencesStaysPeopleOpinionSeriesSeriesSoul of the SouthexploreCity ScenesWomen Beyond BordersConscious Travel, TravelTravel News, NewsDestinationsExperiencesStaysPeopleOpinionSeries, NewsDestinationsExperiencesStaysPeopleOpinionSeriesSeriesSoul of the SouthexploreCity ScenesWomen Beyond BordersConscious Travel
main: 100.00%
article: 100.00%
h1: 100.00%
i: 100.00%
time: 100.00%
h2: 100.00%
strong: 100.00%
figcaption: 100.00%
h3: 100.00%
aside: 100.00%
footer: 100.00% [TAG! HERE], text: SearchNewsDestinationsExperiencesStaysPeopleOpinionSeriesTerms and ConditionsCookie Policy-EnglishEnglishFrançaisDeutschItalianoEspañolPortuguêsРусскийTürkçeΕλληνικάMagyarفارسیالعربيةShqipRomânăქართულიбългарскиSrpskiVisit Euronews
form: 100.00% [TAG! HERE], text: Search
title: 100.00%
select: 100.00%
option: 100.00%
p: 96.08%
a: 83.85%
li: 81.82%
ul: 76.92%
span: 76.71%
label: 66.67%
div: 61.90%
button: 57.14% [TAG! HERE], text: OPEN, MoreHide, Search, English
input: 25.00% [TAG! HERE], text: Search
figure: 25.00%
svg: 4.00% [TAG! HERE], text: Search
path: 0.00%
img: 0.00%
link: 0.00%
circle: 0.00%
rect: 0.00%
noscript: 0.00%


Website_4
Percentage of each type of tag containing text:
header: 100.00%
ul: 100.00%
li: 100.00%
form: 100.00% [TAG! HERE], text: Search for:
label: 100.00%
h1: 100.00%
main: 100.00%
article: 100.00%
p: 100.00%
strong: 100.00%
h3: 100.00%
h2: 100.00%
h4: 100.00%
footer: 100.00% [TAG! HERE], text: Get SocialContact CampusTU Delft CampusBuilding 26CVan der Burghweg 12628 CS Delftinfo@tudelftcampus.nlContact CRE-FMCampus Real Estate& Facility Management (CREFM)Landbergstraat 82628 CE DelftSecr-CREFM@tudelft.nl+31 (0)15 278 8000Stay connectedSign up for the TU DelftCampus Community newsletterand/or thePioneering Tech newsletterVISIT USAccessibility & ParkingCampus mapfusion-columnsfusion-row, © Copyright- TU Delft CampusPrivacy StatementLinkedInTwitterYouTubefusion-fusion-copyright-contentfusion-row
section: 88.89%
a: 82.35%
div: 68.42%
span: 67.29%
nav: 50.00% [TAG! HERE], text: NewsNewsNewsStoriesPioneering for changeActivitiesEventsStart-up SupportEntrepreneurshipStudentsTU Delft Startup vouchersApplication Aerospace Startup VoucherDE Startup VoucherBK-Launch Startup VoucherEnergy Startup VoucherSettleTU Delft CampusSettleAccessibility & parkingFacilitiesFieldlabs and innovation clustersDelft on Internet of ThingsFloodproof HollandMobility Innovation Centre DelftRoboHouseThe Green VillageAll field labs and innovation clustersThe CampusCampus developmentCampus developmentProjectsDevelopment areasHistoryAboutCollaborateInnovate togetherFieldlabsAboutFacts & FiguresCampus mapFood and beverage on campusENNLSearch for:
button: 33.33% [TAG! HERE], text: Close
svg: 0.00% [TAG! HERE], text: 
defs: 0.00%
filter: 0.00%
fecolormatrix: 0.00%
fecomponenttransfer: 0.00%
fefuncr: 0.00%
fefuncg: 0.00%
fefuncb: 0.00%
fefunca: 0.00%
fecomposite: 0.00%
img: 0.00%
noscript: 0.00%
i: 0.00%
input: 0.00% [TAG! HERE], text: 
iframe: 0.00%
br: 0.00%
b: 0.00%
path: 0.00%
link: 0.00%

Website_5
Percentage of each type of tag containing text:
header: 100.00%
main: 100.00%
h1: 100.00%
p: 100.00%
h2: 100.00%
form: 100.00% [TAG! HERE], text: FunctioneelDeze cookies worden gebruikt om onze website naar behoren te laten functioneren.AnalytischDeze cookies worden gebruikt om het gebruik van de website te meten (analyseren). Met deze meetgegevens worden statistieken gemaakt die wij gebruiken om de website te verbeteren.PersonalisatieDeze cookies worden gebruikt om te analyseren hoe u onze website gebruikt. Op basis hiervan kunnen wij de inhoud van onze website aanpassen met informatie die aansluit op uw interesses.Sociale mediaDeze cookies worden geplaatst door sociale medianetwerken zoals Facebook, Twitter en LinkedIn. Bijvoorbeeld wanneer u een bericht deelt of liket via de social media buttons op onze website. De sociale medianetwerken kunnen hiermee uw internetgedrag zien en gebruiken voor eigen doeleinden.AdvertentiesDeze cookies worden geplaatst door advertentiepartners. De cookies worden gebruikt om relevante advertenties van de VU te tonen op andere websites die u bezoekt. Met deze cookies kan uw internetgedrag gevolgd worden door advertentienetwerken.Bewaren
footer: 100.00% [TAG! HERE], text: VU HoofdmenuHomeOnderwijsOnderzoekOver de VUUniversiteitsbibliotheekPersvoorlichtingAlumniVeel gezochtContactPersonenzoekerBacheloropleidingenMasteropleidingenOpleidingen voor professionalsFaculteitenWerken bij de VUUitgelichtCampus tourDoneer aan het VUfondsStudiegidsVU Studie InspiratorAd ValvasVU MagazinePrivacy VerklaringDisclaimerVeiligheidWebcolofonCookie SettingsWebarchiefCopyright © 2023 - Vrije Universiteit Amsterdam
a: 88.89%
section: 88.89%
span: 87.93%
ul: 87.50%
li: 82.98%
div: 79.73%
button: 50.00% [TAG! HERE], text: Accepteer alle cookies, Stel mijn voorkeuren in, Accepteer alle cookies, Bewaren
widget-content-slider: 50.00%
noscript: 0.00%
iframe: 0.00%
widget-navigation: 0.00%
img: 0.00%
i: 0.00%
widget-login: 0.00%
my-studychoice-authentication: 0.00%
widget-search-overlay: 0.00%
widget-agenda: 0.00%
label: 0.00%
input: 0.00% [TAG! HERE], text: 
"""