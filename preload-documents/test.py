import requests
import json

url = "https://jp-ftd-openai.openai.azure.com/openai/deployments/ftd-embedding-ada/embeddings?api-version=2024-02-01"

payload = json.dumps({
  "input": "The food was delicious and the waiter..."
})
headers = {
  'Content-Type': 'application/json',
  'api-key': '29392cd0e4a54a919f390cc3b1baed26'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
