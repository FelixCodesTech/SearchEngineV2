# This is the class for the crawler
# It will crawl the web and get the data and return that (no processing, just pre-processing)


# imports
import requests
from bs4 import BeautifulSoup as bs
import time
import urllib.parse
from helpers import *



# class
class Crawler:
    # constructor
    def __init__(self):
        # 
        pass # no need for anything here
    

    # gets the site html & data
    def getSite(self, url:str):
        site = {}
        site['url'] = url


        try:
            # Setting up a session
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            })

            # Getting the source (and measuring time)
            startTime = time.time()
            source = session.get(site['url'], timeout=2).text
            endTime = time.time()
            
            site['loadingTime'] = endTime - startTime
            soup = bs(source, 'html.parser')
            site['HTML'] = soup
        except Exception as e:
            print("Error: ", e)
            return None

        return site


    # prepares the data for indexer (returns site dict containing HTML, url, extLinks, tags, title, contentLength)
    def processSiteData(self, site:dict):
        ### get external links
        site['extLinks'] = []
        ogFormattedNetloc = urllib.parse.urlparse(site['url']).netloc.replace('www.', '')

        for link in site['HTML'].find_all('a'):
            href = link.get('href')
            if not href or not href.startswith('https://'):
                continue
                
            parsedLink = urllib.parse.urlparse(href)
            formattedNetloc = parsedLink.netloc.replace('www.', '')
            netlocParts = formattedNetloc.split('.')
            isSameTopDomain = len(netlocParts) > 1 and netlocParts[-2] in ogFormattedNetloc # check if the domain (not subdomain) is the same


            # first check if valid and if really an external link (not the same domain)
            if not isSameTopDomain and formattedNetloc != ogFormattedNetloc:
                # # Ensure the link is in the format: https://example.com
                # formattedLink = 'https://' + parsedLink.netloc.replace('www.', '')

                # Ensure the link only contains https, netloc, path (no query, fragment, etc.)
                formattedLink = 'https://' + formattedNetloc + parsedLink.path

                # Append the formatted domain to the list if it's not already in the list
                if formattedLink not in site['extLinks']:
                    site['extLinks'].append(formattedLink)


        ### get hashed external links
        site['hashedExtLinks'] = [getHash(link, 10) for link in site['extLinks']]
    


        ### get tags
        # we get tags by taking the title and splitting with spaces (for now)
        # we only take tags consisting of alphanumeric characters
        html = site['HTML']
        title = html.title.string if html.title and html.title.string else ''
        title = title.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
        title = ' '.join(title.split()) # if there are multiple spaces next to each other
        site['title'] = title
        site['tags'] = []
        
        # tags from title
        if title and title != '':
            # Split the title by various delimiters and filter out non-alphanumeric tags
            delimiters = [' ', '&', '-', '|', '.', ':', '_', '/', '\\', ',', '!', '?', ':', '\n']
            tags = [title.lower()]
            for delimiter in delimiters:
                tags = [tag for part in tags for tag in part.split(delimiter)]
            
            site['tags'] = [tag for tag in tags if tag.isalnum()]

        

        ## tags from url (about.google.com -> ['about', 'google']) - by splitting netloc if necessary
        # Extract tags from the URL, excluding the top-level domain (TLD)
        parsedUrl = urllib.parse.urlparse(site['url'])
        domainParts = parsedUrl.netloc.replace('www.', '').split('.')
        
        # Exclude the last part (TLD) and ensure tags are alphanumeric
        site['tags'] += [tag for tag in domainParts[:-1] if tag.isalnum()]

        # clear out duplicate tags
        site['tags'] = list(set(site['tags']))


        ### get content length
        site['contentLength'] = len(html.get_text())


        ### backlinks
        site['backlinks'] = []
        site['backlinksScore'] = 0



        ### Get hash
        site['urlHash'] = getHash(site['url'], 10)

        return site