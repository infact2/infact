import validators
import re
import urllib
from urllib.parse import urlparse

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
DANGEROUS = "nuh uh"

def scrape(url):
    if dangerous(url):
        return DANGEROUS
    else:
        return urllib.request.urlopen(urllib.request.Request(url, headers=hdr))

def dangerous(url):
    # disabled until I find a fix

    # make sure domain is valid
    if validators.domain(urlparse(url).netloc) != True:
        print(urlparse(url).netloc)
        return True
    return False