import requests
import re
import sys
import os
from urllib.parse import urlencode, urlparse, urlunparse
from urllib.parse import parse_qs

# Examples
# DSPACE_STEM = "https://demo.dspace.org"
DSPACE_STEM = "http://125.22.54.221:8080"


def downloadItem(xmlURL):
    x = requests.get(xmlURL)

    if x.ok:
        obj = re.findall(
            "((\/xmlui\/bitstream\/handle\/[\d\.]+\/[\d\.]+\/(.+))\?[^\"]*)", x.text)

        folderName = re.findall(
            "<a href=\"\/xmlui\/handle\/\d+\/\d+\">(.+)<\/a>", x.text)

        folderName = folderName[1]
        folderName = re.sub(r'[^\w\-_\. ]', '_', folderName)

        os.mkdir(folderName)

        fileDict = dict()
        for file in obj:
            fileDict[file[1]] = file[2]

        for fileURL, fileName in fileDict.items():
            print(f"Downloading {fileName} into {folderName}...")
            downloadedFile = requests.get(
                DSPACE_STEM + fileURL)
            if downloadedFile.ok:
                with open(os.path.join(folderName, fileName), 'wb') as f:
                    f.write(downloadedFile.content)
            else:
                print(
                    "Error: Couldn't download file. Please DM or @ PyRet#4288 on Discord")
    else:
        print("Error: Couldn't fetch URL. Try checking your URL?")
        exit()


if len(sys.argv) <= 1:
    print("Error: Please provide atleast one URL to download from")
    exit()

for url in sys.argv[1:]:
    check_if_item = re.findall(
        "^http(s?):.+\/jspui\/handle\/[\d\.]+\/[\d\.]+$", url)
    check_if_search = re.findall(
        "^http(s?):.+\/jspui\/simple-search\?(.+)(query=(.+))(.+)$", url)

    if not url.startswith(DSPACE_STEM):
        print("Error: Invalid URL format")
        exit()

    if check_if_item:
        xmlURL = url.replace("/jspui/handle/", "/xmlui/handle/")
        downloadItem(xmlURL)
    elif check_if_search:
        allFound = False
        start = 0
        while not allFound:
            parsed_url = urlparse(url)
            query = parse_qs(parsed_url.query)
            query["rpp"] = "100"
            query["start"] = start
            start += 100
            for queryParam in query:
                if type(query[f"{queryParam}"]) == list:
                    query[f"{queryParam}"] = query[f"{queryParam}"][0]
            queryString = urlencode(query)
            parsed_url = parsed_url._replace(query=queryString)
            unparsed = urlunparse(parsed_url)
            headers = {'Accept-Encoding': 'identity'}
            search_page = requests.get(unparsed, headers=headers)

            if search_page.ok:
                items = re.findall(
                    "\"(\/jspui\/handle\/[\d\.]+\/[\d\.]+)\"", search_page.text)
                if len(items) == 0:
                    allFound = True
                for item in items:
                    downloadItem(
                        DSPACE_STEM + item.replace("/jspui/handle/", "/xmlui/handle/"))
            else:
                print("Error: Couldn't fetch URL. Try checking your URL?")
                exit()
    else:
        print("Error: Invalid URL format")
        exit()
