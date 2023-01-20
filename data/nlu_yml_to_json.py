import json
import yaml

# with open('data/nlu.yml', 'r') as file:
#     nlu_examples = yaml.safe_load(file)

# with open('data/nlu.json', 'w') as json_file:
#     json.dump(nlu_examples, json_file)
    
output = json.load(open('data/nlu.json'))
suggestions = []
avoided_intent = ['greet', 'goodbye', 'nlu_fallback']
for item in output['nlu']:
  if(item['intent'] not in avoided_intent):
    striped_op = [s.strip() for s in item['examples'].split("-")[1:]]
    suggestions = suggestions + striped_op
print(suggestions)
