import requests
import os

query = {'shortname':'gilbridj'}
response = requests.get("https://cs7ns1.scss.tcd.ie/", params=query)

with open('gilbridj', 'wb') as writeable:
    writeable.write(response.content)

with open('gilbridj') as readable:
    content = readable.read()
    path = content.split("<a href='")[1]
    path = path.split("' >")[0]
    print(path)

response = requests.get("https://cs7ns1.scss.tcd.ie/" + path)
with open('gilbridj.csv', 'wb') as writeable:
    writeable.write(response.content)

with open('gilbridj.csv') as readable:
    content = readable.read()
    splitContent = content.split(",")

if not os.path.exists("./images"):
    os.makedirs(".images")

for filename in splitContent:
    filename = filename.strip()
    #print(filename)
    response = requests.get("https://cs7ns1.scss.tcd.ie/"+filename, params=query)
    with open("images/" + filename, 'wb') as imageFile:
        imageFile.write(imageFile.content)


