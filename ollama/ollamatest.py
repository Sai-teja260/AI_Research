import requests
import json

response = requests.post(
    url="http://localhost:11434/api/generate"
    headers={
        "Authorization": "abcd",
        "HTTP-Referer": "<your_site_url>",
        "X-Title": "<your_site_name>"
    },
    data=json.dumps({
        "model":"llama3.2:1b",
        "prompt": "Where is Hyderabad located?",
        "stream":False
    })
)
print(response.content)
