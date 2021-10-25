import requests

query = {'shortname':'gilbridj'}
response = requests.get("https://cs7ns1.scss.tcd.ie/", params=query)

with open('gilbridj', 'wb') as writeable:
    writeable.write(response.content)

with open('gilbridj') as readable:
    first_line = readable.readline()
    new_request = first_line.split(": ")[2]
    print(new_request)


response = requests.get("https://cs7ns1.scss.tcd.ie/" + new_request, params=query)
with open('gilbridj-challenge-filenames.csv', 'wb') as writeable:
    writeable.write(response.content)

with open('gilbridj-challenge-filenames.csv') as readable:
    print(readable.content.decode('utf-8'))