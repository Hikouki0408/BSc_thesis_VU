from pycorenlp import StanfordCoreNLP

# Create a connection to the Stanford CoreNLP server
nlp = StanfordCoreNLP('http://localhost:9000')

# run this code: java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

# John works at a company in New York.
#"The Vrije Universiteit Amsterdam is being founded in 1880. The VU Amsterdam is one of two large, publicly funded research universities in the city."

text = ""

# Use the 'openie' annotator to extract relations
output = nlp.annotate(text, properties={
    'annotators': 'openie',
    'outputFormat': 'json',
    'openie.triple.strict': 'true',
    'openie.max_entailments_per_clause': '1'
})


counter = 1

# Extract and print the relations
for sentence in output['sentences']:
    for triple in sentence['openie']:
        subject = triple['subject']
        relation = triple['relation']
        obj = triple['object']
        print(f'{counter}. Subject: {subject}, Relation: {relation}, Object: {obj}')
        counter += 1
