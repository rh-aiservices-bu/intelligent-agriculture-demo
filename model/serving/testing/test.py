import requests

url = 'http://127.0.0.1:5000/prediction'
file = {'file': open('healthy.jpg', 'rb')}
resp = requests.post(url=url, files=file) 
print(resp.json())

file = {'file': open('unhealthy.jpg', 'rb')}
resp = requests.post(url=url, files=file) 
print(resp.json())