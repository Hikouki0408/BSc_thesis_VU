from pycorenlp import StanfordCoreNLP

# Create a connection to the Stanford CoreNLP server
nlp = StanfordCoreNLP('http://localhost:9000')

# run this code: java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

# John works at a company in New York.
#"The Vrije Universiteit Amsterdam is being founded in 1880. The VU Amsterdam is one of two large, publicly funded research universities in the city."

text = "Best foldable Android phone: Samsung Galaxy Z Fold 4 Best foldable Android phone Photo by Sam Rutherford / Engadget Samsung Galaxy Z Fold 4 $1,760. Samsung's Z fold 4 is like having three devices in one, which makes it a unicorn among mobile devices. $1,760 at Amazon $1,800 at Samsung. While the Galaxy Z Flip 4 is arguably the most stylish and compact phone on the market, the bigger and more expensive Z Fold 4 is like three devices in one, which makes it a unicorn among mobile devices. When you just need to respond to a text or look up an address quickly, its 6.2-inch exterior cover screen makes that a cinch. But when you want to sit down to watch a movie or play a game, you can open up the Fold to reveal a stunning 7.8-inch flexible display. As a foldable phone, it's compact when you need it to be, while providing an immersive viewing experience on a large screen when you don’t. And thanks to support for stylus input, you even can use one of Samsung’s S Pens designed specifically for the Fold to quickly draw or jot down a note. On top of all that, its OLED display makes the Z Fold 4 great for reading books and comics. And unlike practically any other non-Samsung foldable, the Fold also has an IP68 rating for dust and water resistance. In a lot of ways, this thing is the Swiss Army knife of phones. Sure, it’s a bit bulky, and at $1,800 it’s not what anyone would call affordable. But this Samsung phone's ability to serve as a phone, a tablet, an e-reader and more depending on the situation puts the Z Fold 4 in a category of its own. Read our Full Review of Samsung Galaxy Z Fold 4. The best Android phones for 2023 thebuyersguide gear evergreen best tech feature commerce shoppable streamshopping Terms and Privacy Policy Privacy & Cookie Settings About Our Ads © 2023 Yahoo."


# Use the 'openie' annotator to extract relations
output = nlp.annotate(text, properties={
    'annotators': 'openie',
    'outputFormat': 'json',
    'openie.triple.strict': 'true',
    'openie.max_entailments_per_clause': '1'
})


counter = 45

# Extract and print the relations
for sentence in output['sentences']:
    for triple in sentence['openie']:
        subject = triple['subject']
        relation = triple['relation']
        obj = triple['object']
        print(f'{counter}. Subject: {subject}, Relation: {relation}, Object: {obj}')
        counter += 1
