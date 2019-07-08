#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup

class ScannerScraper(object):
    def __init__(self):
        self.search_request = {
            "scan_clause" : "{cash}+(+net+profit[yearly]+>+ttm+net+profit+*+2+)+and+(+net+profit[yearly]+>+0+)+and+(+ttm+net+profit+>+0+)"
        }

    def scrape(self):
        scans = self.scrape_scans()
        for scan in scans:
            print(scan)

    def scrape_scans(self):
        scans = []
        
        self.search_request['scan_clause'] = "{cash}+(+net+profit[yearly]+>+ttm+net+profit+*+2+)+and+(+net+profit[yearly]+>+0+)+and+(+ttm+net+profit+>+0+)"
        i=2
        while i>1:
            payload = { 
                'scan_clause': json.dumps(self.search_request),
                
            }

            r = requests.post(
                url='https://chartink.com/screener/process',
                data=payload,
                headers={
                    'X-Requested-With': 'XMLHttpRequest'
                }
            )

            s = BeautifulSoup(r.text , features="lxml")
            if not s.requisition:
                break

            for r in s.findAll('requisition'):
                scan = {}
                scan['nsecode'] = r.nsecode.text
                scan['name'] = r.name.text
                scans.append(scan)

            # Next page
        i=i-1
            

        return scans

if __name__ == '__main__':
    scraper = ScannerScraper()
    scraper.scrape()
