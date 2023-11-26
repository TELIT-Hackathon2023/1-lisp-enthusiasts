#from config.settings import client
import requests
import openai
from pathlib import Path
import json
OPENAI_API_KEY=""
line = "https://marian.mach.website.tuke.sk/"
#line = "https://www.orange.sk/"
#x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={line}'
#print(f'Requesting {x}...')

#r = requests.get(x)
#final = r.json()
html = requests.get(line)

client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
)
with open('response.json', 'r') as f:
    json_data = json.load(f)
input_json = json_data['message']

jsonl_string = json.dumps(input_json)
with open('output.jsonl', 'w') as jsonl_output:
        #json.dump(entry, jsonl_output)
        #jsonl_output.write('\n')
        jsonl_output.write(jsonl_string + '\n')

client.files.create(
file=open("output.jsonl", "rb"),
purpose='fine-tune'
) 
#client.fine_tuning.jobs.create(
#  training_file='file-EI05zDVhhtK9FUhf6gzfTDLQ', 
#  model="gpt-3.5-turbo", 
#  hyperparameters={
#    "n_epochs":2
#  }
#)

messages = [
            #{"role": "system", "content": json.dumps(final)},
            #{"role": "system", "content": json.dumps(html)},
            {"role": "user", "content": "This is a HTML file that was loaded from a webpage. JSON (I provided you and it is in files) before is full of information of how page can be made better. I would like you to create code snippets of fixed code based on the problems that are found in the descriptions. Please generate HTML fixes if you can."}
        ]

#response = client.chat.completions.create(
#    model='gpt-4',
#    messages=messages
#)

#ans = response.choices[0].message.content.split('\n')

#print(ans)