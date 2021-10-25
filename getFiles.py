import requests

query = {'shortname':'gilbridj'}
response = requests.get("https://cs7ns1.scss.tcd.ie/", params=query)

with open('gilbridj', 'wb') as writeable:
    writeable.write(response.content)

with open('gilbridj') as readable:
    content = readable.read()
    content = content.split("<a href='")[1]
    content = content.split("' >")[0]
    print(content)

'''
query = {'shortname': new_request}
response = requests.get("https://cs7ns1.scss.tcd.ie/", params=query)
with open('gilbridj-challenge-filenames.csv', 'wb') as writeable:
    writeable.write(response.content)

with open('gilbridj-challenge-filenames.csv') as readable:
    content = readable.read()
    print(content)
    '''