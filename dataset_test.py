import json

# Read the subjects from the text file
with open('all_vu_wiki.txt', 'r') as file:
    subjects = file.read().splitlines()

# Create a list to store the subject instances
subject_instances = []

# Process each subject and create an instance
for subject in subjects:
    parts = subject.split(', Relation: ')
    subject_instance = {
        'Subject': parts[0].split('Subject: ')[1],
        'Relation': parts[1].split(', Object: ')[0],
        'Object': parts[1].split(', Object: ')[1]
    }
    subject_instances.append(subject_instance)

# Save the subject instances to a JSON file
with open('subjects.json', 'w') as file:
    json.dump(subject_instances, file, indent=4)
