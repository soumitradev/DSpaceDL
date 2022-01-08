import requests
import re
import sys
import os

# Examples
# DSPACE_STEM = "https://demo.dspace.org"
DSPACE_STEM = "http://125.22.54.221:8080"

if len(sys.argv) <= 1:
    print("Error: Please provide atleast one URL to download from")
    exit()

for url in sys.argv[1:]:
    check = re.findall(
        "^http(s?):.+\/jspui\/handle\/[\d\.]+\/[\d\.]+$", url)

    if (not check) or (not url.startswith(DSPACE_STEM)):
        print("Error: Invalid URL format")
        exit()

    xmlURL = url.replace("/jspui/handle/", "/xmlui/handle/")

    x = requests.get(xmlURL)

    if x.ok:
        obj = re.findall(
            "(\/xmlui\/bitstream\/handle\/[\d\.]+\/[\d\.]+\/(.+)\?[^\"]*)", x.text)

        folderName = re.findall(
            "<a href=\"\/xmlui\/handle\/\d+\/\d+\">(.+)<\/a>", x.text)

        folderName = folderName[1]
        folderName = re.sub(r'[^\w\-_\. ]', '_', folderName)

        os.mkdir(folderName)

        for file in obj:
            print(f"Downloading {file[1]} into {folderName}...")
            downloadedFile = requests.get(
                DSPACE_STEM + file[0])
            if downloadedFile.ok:
                with open(os.path.join(folderName, file[1]), 'wb') as f:
                    f.write(downloadedFile.content)
            else:
                print(
                    "Error: Couldn't download file. Please DM or @ PyRet#4288 on Discord")
    else:
        print("Error: Couldn't fetch URL. Try checking your URL?")
        exit()
