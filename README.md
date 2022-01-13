# DSpaceDL

A tool for downloading files from DSpace items.

For some reason, DSpace systems have a dogshit UI, and Universities absolutely LOOOVE to use such software to cause as much pain to the student as humanly possible.

Well, that ends today. No longer will we be chained by the clunky UI of old websites that force you to download each file individually. No longer will we need to open 5000 browser tabs open so we can download files from DSpace systems.

I'm basically running a regex on the XML on DSpace and extracting each file's information so I can download it.

### Usage

`download.py` defines a `DSPACE_STEM` in it as a safety mechanism. This basically ensures you don't download the wrong files from the wrong link. It's also used for URL verification.

After making sure you have the correct `DSPACE_STEM` variable set, you can then download files from DSpace items like so:

#### Single files

```
python ./download.py https://demo.dspace.org/jspui/handle/10673/6.3
```

This downloads all the files in the given item to a folder with the name of the parent collection since that's usually the categorization you want instead of the item name itself.

Only the first collection's name is used in case the item is in multiple collections.

#### Files from multiple URLs

```
python ./download.py https://demo.dspace.org/jspui/handle/10673/6.3 https://demo.dspace.org/jspui/handle/10673/59 https://demo.dspace.org/jspui/handle/10673/60
```

There is no limit to how many URLs you can download from.

#### All files from a search query

```
python ./download.py http://125.22.54.221:8080/jspui/simple-search?location=&query=BITS+F110&rpp=10&sort_by=score&order=DESC&etal=0&submit_search=Update
```

This will download _all_ results. There is no limit. Be careful if you have a query with a large number of results.

### Why?

pain
