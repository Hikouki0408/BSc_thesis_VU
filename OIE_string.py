from pycorenlp import StanfordCoreNLP

# Create a connection to the Stanford CoreNLP server
nlp = StanfordCoreNLP('http://localhost:9000')

# run this code: java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

# John works at a company in New York.
#"The Vrije Universiteit Amsterdam is being founded in 1880. The VU Amsterdam is one of two large, publicly funded research universities in the city."

text = "Ruth de Vries +31 648 51 11 22 Sign up for the Campus Community newsletter. Sign up Jochen Meischke 2023-06-08T11:47:32+02:00 June 6th, 2023 Share This Story, Choose Your Platform! Facebook Twitter Reddit LinkedIn WhatsApp Tumblr Pinterest Vk Email Related Posts How STIL helps people with a tremor lead a normal life again June 29th, 2023 Delft tops charts in 2023 Entrepreneurial Ecosystem Index June 19th, 2023 TU Delft continues collaboration with AMS Institute June 19th, 2023 - TU Delft Campus Privacy Statement LinkedIn Twitter YouTube Page load link We use cookies to ensure the best possible experience on our website. If you would like to know more about the settings of the cookies click on the 'Preferences' button. On this pop-up, you can set the cookies to your preferences. When you click on the button 'Agree and continue' you will agree on all the cookies that we described in the privacy policy Cookie settings Accept Privacy & Cookies Policy Privacy Overview This website uses cookies to improve your experience while you navigate through the website. Out of these, the cookies that are categorized as necessary are stored on your browser as they are essential for the working of basic functionalities of the website. We also use third-party cookies that help us analyze and understand how you use this website. These cookies will be stored in your browser only with your consent. You also have the option to opt-out of these cookies. But opting out of some of these cookies may affect your browsing experience. Necessary Always Enabled Necessary cookies are automatically placed on your device when you access tudelftcampus.nl or take certain actions on our website. Non-necessary Non-necessary cookies are only placed on your device if you have specifically consented to us doing so. SAVE & ACCEPT"


# Use the 'openie' annotator to extract relations
output = nlp.annotate(text, properties={
    'annotators': 'openie',
    'outputFormat': 'json',
    'openie.triple.strict': 'true',
    'openie.max_entailments_per_clause': '1'
})


counter = 61

# Extract and print the relations
for sentence in output['sentences']:
    for triple in sentence['openie']:
        subject = triple['subject']
        relation = triple['relation']
        obj = triple['object']
        print(f'{counter}. Subject: {subject}, Relation: {relation}, Object: {obj}')
        counter += 1
