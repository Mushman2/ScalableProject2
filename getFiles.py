import requests

query = {'shortname':'gilbridj'}
response = requests.get("https://cs7ns1.scss.tcd.ie/", params=query)

if response.status_code != 200:
    print("error getting file")
    print(response)

with open('gilbridj', 'wb') as f:
    f.write(r.content)

print(response.content.decode('utf-8'))
