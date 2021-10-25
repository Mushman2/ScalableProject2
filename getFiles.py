import requests

query = {'shortname':'gilbridj'}
response = requests.get("https://www.cs7ns1.scss.tcd.ie")
print(response)
