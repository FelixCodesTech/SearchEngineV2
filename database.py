# This is the class for the crawler
# It will be the connecting part between the database and everything else


# Imports
import mysql.connector as connector
from helpers import *
import json



class Database:
    def __init__(self):
        # db Connections
        self.db = connector.connect(
            host="192.168.178.138",
            user="user",
            password="password",
            database="searchEngine"
        )

        # db contains 2 tables: siteIndex and quickLookupIndex
        # siteIndex:            ID, url, urlHash, title, loadingTime, loadingTimeScore, contentLength, contentLengthScore, extLinks, hashedExtLinks, extLinksScore, tags, tagsScore, backlinks, backlinksScore
        # quickLookupIndex:     tag, sites

        # Cursors
        self.dbCursor = self.db.cursor()
        
    def __del__(self):
        self.db.close()

    


    # Function to add a site to the main index
    # TODO: Probably add anti-duplicate check???
    def addToMainIndex(self, site):
        # Query to add a site to the main index
        query = (
            "INSERT INTO siteIndex (url, urlHash, title, loadingTime, loadingTimeScore, "
            "contentLength, contentLengthScore, extLinks, hashedExtLinks, extLinksScore, tags, "
            "tagsScore, backlinks, backlinksScore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
        )
        values = (
            site['url'][:250], site['urlHash'], site['title'][:250], site['loadingTime'], site['loadingTimeScore'],
            site['contentLength'], site['contentLengthScore'], json.dumps(site['extLinks']), json.dumps(site['hashedExtLinks']), site['extLinksScore'],
            json.dumps(site['tags']), site['tagsScore'], json.dumps(site['backlinks']), site['backlinksScore']
        )


        self.dbCursor.execute(query, values)
        self.db.commit()
        
        # Get the ID of the site for the quickLookupIndex
        ID = self.dbCursor.lastrowid
        return ID



    # Function to add a site to the quick lookup index
    def addToQuickLookupIndex(self, site, siteID, tagsBf):
        for tag in site['tags']:
            # Check if the tag definitely does not exist or if it probably does via the bloom filter
            if not tag in tagsBf:
                # If the tag definitely does not exist, create a new row
                query = (
                    "INSERT INTO quickLookupIndex (tag, sites) VALUES (%s, %s)"
                )
                values = (
                    tag, json.dumps([siteID])  # sites being a json list of the ID
                )

                tagsBf.put(tag)
            else:
                # If the tag probably exists, check the database
                query = (
                    "SELECT sites FROM quickLookupIndex WHERE tag = %s"
                )
                values = (
                    tag,
                )

                self.dbCursor.execute(query, values)
                result = self.dbCursor.fetchall()

                if result:
                    # If the tag exists, update the existing row
                    sites = json.loads(result[0][0])
                    sites.append(siteID)

                    query = (
                        "UPDATE quickLookupIndex SET sites = %s WHERE tag = %s"
                    )
                    values = (
                        json.dumps(sites), tag
                    )
                else:
                    # If the tag does not exist, create a new row
                    query = (
                        "INSERT INTO quickLookupIndex (tag, sites) VALUES (%s, %s)"
                    )
                    values = (
                        tag, json.dumps([siteID])  # sites being a json list of the ID
                    )

                    tagsBf.put(tag)

            self.dbCursor.execute(query, values)
            self.db.commit()



        




    ### Backlinks handling
    # Get all the hashedExtLinks linking to the given site already and add them to backlinks (then score them)
    def addExistingBacklinks(self, site):
        # Query to get all sites that have a link to the given site
        query = (
            "SELECT urlHash FROM siteIndex WHERE hashedExtLinks LIKE %s"
        )
        values = (
            f"%{site['urlHash']}%"
        )
        self.dbCursor.execute(query, values)
        results = self.dbCursor.fetchall()
        self.dbCursor.fetchall()  # Fetch all remaining results to avoid unread result error
        results = self.dbCursor.fetchall()

        # Add the backlinks to the site
        site['backlinks'] = [result['urlHash'] for result in results]
        
        # Score the backlinks (from 0 to 1)
        site['backlinksScore'] = clamp(len(site['backlinks'])/1000, 0, 1)



    
    # For all hashedExtLinks, add given site to their backlinks (json of urlHashes)
    def addSiteToBacklinked(self, site):
        # Get all sites from hashedExtLink (if they exist)
        for hashedExtLink in site['hashedExtLinks']:
            # Query to get the backlinks of the site
            query = (
                "SELECT backlinks FROM siteIndex WHERE urlHash = %s"
            )
            values = (
                hashedExtLink,
            )

            self.dbCursor.execute(query, values)
            result = self.dbCursor.fetchone()

            # If the site exists, add the given site to its backlinks
            if result:
                backlinks = json.loads(result[0]) if result[0] else []
                backlinks.append(site['urlHash'])

                # Query to update the backlinks of the site
                query = (
                    "UPDATE siteIndex SET backlinks = %s WHERE urlHash = %s"
                )
                values = (
                    json.dumps(backlinks), hashedExtLink
                )

                self.dbCursor.execute(query, values)
                self.db.commit()
    



    # Check if a site already exists in the database
    def checkIfSiteExists(self, url):
        # Query only the urlHash for faster lookup
        urlHash = getHash(url, 10)

        query = (
            "SELECT urlHash FROM siteIndex WHERE urlHash = %s"
        )
        values = (
            urlHash,
        )

        self.dbCursor.execute(query, values)
        result = self.dbCursor.fetchall()

        return True if result else False