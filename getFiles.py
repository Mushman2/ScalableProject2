import requests
import os
import shutil

if(len(sys.argv) != 1):
    print("Script should be passed one argument, your network username.")

shortname = argv[0]

query = {'shortname': shortname}
response = requests.get("https://cs7ns1.scss.tcd.ie/", params=query)

with open(shortname, 'wb') as writeable:
    writeable.write(response.content)

with open(shortname) as readable:
    content = readable.read()
    path = content.split("<a href='")[1]
    path = path.split("' >")[0]
    print(path)

response = requests.get("https://cs7ns1.scss.tcd.ie/" + path)
with open(shortname + '.csv', 'wb') as writeable:
    writeable.write(response.content)

with open(shortname + '.csv') as readable:
    content = readable.read()
    splitContent = content.split(",")

if not os.path.exists("./" + shortname + "images"):
    os.makedirs("./" + shortname + "images")

for filename in splitContent:
    filename = filename.strip()
    response = requests.get("https://cs7ns1.scss.tcd.ie/"+filename, params=query, stream =True)
    with open("images/" + filename, 'wb') as imageFile:
        shutil.copyfileobj(response.raw, imageFile)
        del response


