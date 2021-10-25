import requests

query = {'shortname':'gilbridj'}
response = requests.get("https://cs7ns1.scss.tcd.ie/", params=query)

with open('gilbridj', 'wb') as writeable:
    writeable.write(response.content)

with open('gilbridj') as readable:
    first_line = readable.readline()
    new_request = first_line.split(": ")
    new_request = new_request.split(": ")
    print(first_line)