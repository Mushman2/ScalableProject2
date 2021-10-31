#!/usr/bin/env python3

import requests
import os
import shutil
import argparse
import sys


def main():
        
    if(len(sys.argv) != 2):
        print("Script should be passed one argument, your network username.")

    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='TCD Username', type=str)
    args = parser.parse_args()

    if args.username is None:
        print("Please specify your TCD Username")
        exit(1)

    shortname = args.username

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

    htmlDirName = "./" + shortname + "_htmls"
    if not os.path.exists(htmlDirName):
        os.makedirs(htmlDirName)
        print("Created htmls directory.")

    imageDirName = "./" + shortname + "_images"
    if not os.path.exists(imageDirName):
        os.makedirs(imageDirName)
        print("Created images directory.")

    for filename in splitContent:
        filename = filename.strip()
        if len(filename != 0)
            query = {'shortname': shortname, 'myfilename': filename}
            response = requests.get("https://cs7ns1.scss.tcd.ie/", params=query, stream=True) 
            with open(htmlDirName + "/" + filename + ".html", 'wb') as writeable:
                writeable.write(response.content)

            with open(htmlDirName + "/" + filename + ".html") as readable:
                content = readable.read()
                path = content.split("<a href='")[1]
                path = path.split("' >")[0]

            response = requests.get("https://cs7ns1.scss.tcd.ie/" + path, stream=True)

            with open(imageDirName + "/" + filename, 'wb') as imageFile:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, imageFile)
                del response

    print("Complete.")

if __name__ == '__main__':
    main()