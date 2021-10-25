import requests

query = {'shortname':'gilbridj'}
response = requests.get("https://www.cs7ns1.scss.tcd.ie", params=query)

if response.status_code != 200:
    print("error getting file")
    print(response)
    return 1

print(response.content.decode('utf-8'))
