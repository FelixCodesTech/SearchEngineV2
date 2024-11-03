# This is the class for the indexer
# It will index the site and return that (no pre-processing, just processing)


# imports
import urllib.parse
from helpers import *


# class
class Indexer:
    # constructor
    def __init__(self):
        pass # no need for anything here


    # score everything
    def processSite(self, site:dict, db):
        url = site['url']
        extLinks = site['extLinks']
        tags = site['tags']
        loadingTime = site['loadingTime']
        title = site['title']
        contentLength = site['contentLength']


        ### MAIN SCORING ###


        # score the external links
        # lin func with 20 = 1 | 30 = 0.9 | 40 = 0.8 | 120 = 0
        site['extLinksScore'] = -0.01*len(extLinks) +1.2
        site['extLinksScore'] = clamp(site['extLinksScore'], 0, 1)


        # score the loading time
        # lin func with 0.2 = 1 | 2 = 0
        site['loadingTimeScore'] = -0.5*loadingTime +1.2
        site['loadingTimeScore'] = clamp(site['loadingTimeScore'], 0, 1)


        # score the tags
        # lin func with 0 = 0 | 10 = 1
        site['tagsScore'] = 0.1*len(tags)
        site['tagsScore'] = clamp(site['tagsScore'], 0, 1)


        # score the content length
        # lin func with 0 = 1 | 10000 = 0
        site['contentLengthScore'] = -0.0001*contentLength +1
        site['contentLengthScore'] = clamp(site['contentLengthScore'], 0, 1)


        return site


