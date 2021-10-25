import requests
import os
import shutil
import sys

if(len(sys.argv) != 2):
    print("Script should be passed one argument, your network username.")

shortname = sys.argv[1]

query = {'shortname': shortname}
response = requests.get("https://cs7ns1.scss.tcd.ie/", params=query)

with open(shortname, 'wb') as writeable:
    writeable.write(response.content)
    print("Got initial response.")

with open(shortname) as readable:
    content = readable.read()
    path = content.split("<a href='")[1]
    path = path.split("' >")[0]
    print("Parsed path from initial response.")

response = requests.get("https://cs7ns1.scss.tcd.ie/" + path)
with open(shortname + '.csv', 'wb') as writeable:
    writeable.write(response.content)
    print("Got second response.")

with open(shortname + '.csv') as readable:
    content = readable.read()
    splitContent = content.split(",")
    print("Split second response.")

dirName = "./" + shortname + "_images"

if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Created images directory.")

for filename in splitContent:
    filename = filename.strip()
    response = requests.get("https://cs7ns1.scss.tcd.ie/"+filename, params=query, stream =True)
    if(not(filename and filename.strip())):
        with open(dirName + "/" + filename, 'wb') as imageFile:
            shutil.copyfileobj(response.raw, imageFile)
            del response

print("Complete.")