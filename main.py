# Imports
from crawler import Crawler
from indexer import Indexer
from database import Database
from bloomfilter import BloomFilter
from helpers import *
import time as t
import signal
import sys




### Config ###
linksToCrawl = ['https://nike.com']
lenLinksToCrawl = 1



# Inits
crawlerBot = Crawler()
indexerBot = Indexer()
db = Database()

# Bloom filters
hashedUrlBfExpectedInserts = 1000000     # bf = bloom filter
hashedUrlBfFalsePosRate = 0.01
hashedUrlBf = BloomFilter(hashedUrlBfExpectedInserts, hashedUrlBfFalsePosRate)
hashedUrlBf = loadBF('BloomFilters/hashedUrlBf.bf')
tagsBfExpectedInserts = 1000000
tagsBfFalsePosRate = 0.01
tagsBf = BloomFilter(tagsBfExpectedInserts, tagsBfFalsePosRate)
tagsBf = loadBF('BloomFilters/tagsBf.bf')





# TODO: Instead use try except so it can even crash and still save the bloom filters!!!

# Setting up the signal Handler to save the bloom filters on exit
def signalHandler(sig, frame):
    print('Saving bloom filters...')
    saveBF(hashedUrlBf, 'BloomFilters/hashedUrlBf.bf')
    saveBF(tagsBf, 'BloomFilters/tagsBf.bf')
    sys.exit(0)
signal.signal(signal.SIGINT, signalHandler)




#### Main loop ####
# This will consist of:
# - Crawling the web (recursively via linksToCrawl)
# - Indexing the sites
# - Storing the data in the database

while True:
    currentUrl = linksToCrawl.pop(0)
    # Check if url is already in the database (via urlHash)
    if getHash(currentUrl, 10) in hashedUrlBf:
        print("Site already exists in the database")
        continue


    print(f"Crawling: {currentUrl}      ({lenLinksToCrawl} links left)")
    site = crawlerBot.getSite(currentUrl)
    if site == None:
        continue
    site = crawlerBot.processSiteData(site)
    site = indexerBot.processSite(site, db)


    # Saving to db
    siteID = db.addToMainIndex(site)
    db.addToQuickLookupIndex(site, siteID, tagsBf)
    hashedUrlBf.put(site['urlHash'])

    # Add the site to the backlinks of the sites it links to
    # db.addSiteToBacklinked(site, db)
    # db.addExistingBacklinks(site, db)


    # Add the site to the linksToCrawl
    lenLinksToCrawl = len(linksToCrawl)
    if lenLinksToCrawl < 50:
        for extLink in site['extLinks'][:20]:
            if not extLink in linksToCrawl and not getHash(extLink, 10) in hashedUrlBf:
                linksToCrawl.append(extLink)
    elif lenLinksToCrawl < 200:
        for extLink in site['extLinks'][:3]:
            if not extLink in linksToCrawl and not getHash(extLink, 10) in hashedUrlBf:
                linksToCrawl.append(extLink)

