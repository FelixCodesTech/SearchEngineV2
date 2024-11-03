from crawler import Crawler
from indexer import Indexer
from database import Database



crawlerBot = Crawler()
indexerBot = Indexer()


site = crawlerBot.getSite('https://reddit.com/r/itchio')
site = crawlerBot.processSiteData(site)
site = indexerBot.processSite(site, None)

print(f'Url: {site["url"]}')
print(f'UrlHash: {site["urlHash"]}')
print(f'Title: {site["title"]}')
print(f'Loading Time: {site["loadingTime"]}')
print(f'Content Length: {site["contentLength"]}')
print(f'External Links: {site["extLinks"]}')
print(f'Tags: {site["tags"]}')
print(f'ID: {site["ID"]}')
print(f'Loading Time Score: {site["loadingTimeScore"]}')
print(f'Content Length Score: {site["contentLengthScore"]}')
print(f'External Links Score: {site["extLinksScore"]}')
print(f'Tags Score: {site["tagsScore"]}')
print(f'Backlinks: {site["backlinks"]}')
print(f'Backlinks Score: {site["backlinksScore"]}')
