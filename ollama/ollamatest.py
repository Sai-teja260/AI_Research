import requests
import json

response = requests.post(
    url="http://82.29.165.165:11434/api/generate",
    headers={
        "Authorization": "abcd",
        "HTTP-Referer": "<your_site_url>",
        "X-Title": "<your_site_name>"
    },
    data=json.dumps({
        "model":"llama3.2:1b",
        "prompt": "who is the pm of pakistan?",
        "stream":False
    })
)
#print(response.content)
response_data = response.json()

# Print only the 'response' message
print(response_data['response'])
