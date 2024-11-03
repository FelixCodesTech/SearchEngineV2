# imports
from crawler import Crawler
from indexer import Indexer
import time as t
import csv



# main (testing)
remainingLinksList = ['https://zonelets.net/posts/2020-11-08-Comparison-to-Other-Blogging-Methods']
CSVNAME = 'data.csv' # this has the columns: URL, extLinks, tags, loadingTime, title, contentLength, extLinksScore, loadingTimeScore, tagsScore, contentLengthScore


# Classes setup
crawlerBot = Crawler()
indexerBot = Indexer()

while len(remainingLinksList) > 0:
    currURL = remainingLinksList.pop(0)
    print("Remaining links: ", len(remainingLinksList))

    # Crawling
    # print("Crawling: ", currURL)
    site = crawlerBot.getSite(currURL)
    if site == None:
        continue
    site = crawlerBot.processSiteData(site)


    # Indexing
    # print("Indexing: ", currURL)
    indexedStats = indexerBot.processSite(site)


    # Saving to CSV
    print("Saving to CSV: ", currURL)
    with open(CSVNAME, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([indexedStats['url'], indexedStats['extLinks'], indexedStats['tags'], indexedStats['loadingTime'], indexedStats['title'], indexedStats['contentLength'], indexedStats['extLinksScore'], indexedStats['loadingTimeScore'], indexedStats['tagsScore'], indexedStats['contentLengthScore']])

        # Add the external links to remainingLinksList that arent already in the list or in the CSV or the current url anyway
        if len(remainingLinksList) < 400:
            for link in indexedStats['extLinks']:
                if link not in remainingLinksList and link != currURL:
                    isAlreadyInCSV = False
                    with open(CSVNAME, 'r') as readFile:
                        reader = csv.reader(readFile)
                        for row in reader:
                            if link == row[0]:
                                isAlreadyInCSV = True
                                break
                    if not isAlreadyInCSV:
                        remainingLinksList.append(link)
        else: # remove random ones
            remainingLinksList = remainingLinksList[50:350]
            print('Removing random links')
        


    # Sleep for 1 second
    t.sleep(0.1)