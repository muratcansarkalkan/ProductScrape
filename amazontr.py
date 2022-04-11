import urllib.request, urllib.parse, urllib.error
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import utilities
import time
import random
import json

# Randomly switches User Agents to minimize 503 Errors.
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
for i in range(1,4):
    user_agent = random.choice(user_agent_list)

# Specifies the header.
headers = {'User-Agent': user_agent}

origin = "https://www.amazon.com.tr"
outfile = open('resultsamazon.json', 'w', encoding='utf8')

class AmazonTR():
    def __init__(self, query):
        self.query = query

    def link(self):
        # Main link
        link = "https://www.amazon.com.tr/s?"
        # If query exists, it is adapted to url
        if len(self.query) > 0:
            query = (urllib.parse.quote(self.query).replace("%20","+"))

            link = link+"k="+query
            return link
        else:
            return link
    # Initial parse of search results. 14 results per page
    def parser(url0, limit):
        def detailedparser(i, r, limit):
            try:
                # Prepares the product card.
                asin = asincode(i)
                print(f"Trying to parse {r} of {limit} results from Amazon...")
                req = Request(i, headers=headers)
                webpage = urlopen(req, timeout=5).read()
                pro = soup(webpage,"html.parser")
                priceu = pro.find_all('span', class_="a-offscreen")
                price = priceu[0].string
                
                if "TL" not in price:
                    price = "Not available, please view the product page"

                title = pro.find('span', id='productTitle')
                title = (title.string.lstrip()).rstrip()

                product = utilities.ProductCard(asin,title,price,i)
                # amazonlist.append(product)
                jsonAmazonTRStr = json.dumps(product.__dict__, indent=1, ensure_ascii=False)
                outfile.write(jsonAmazonTRStr)
                print(f"Parsing successful for product {r}.")
                time.sleep(1)
            except:
                print("Sorry, product could not be parsed")
        
        # Defines link, page, amazonlist and asinlist. Results per page was 14
        links = []
        pages = (limit // 14)
        amazonlist = []
        asinlist = []

        # Used to get ASIN from link instead of parsed output.
        def asincode(lin):
            j = urllib.parse.unquote(lin).split("dp/")
            k = (j[1]).split("/")
            asin = k[0]
            return asin

        # Here some functions are written repeatedly to assure the script ran correctly first.
        for i in range(1,pages + 2):
            if i == pages + 1:
                url = f"{url0}&page={i}"
                req = Request(url, headers=headers)
                webpage = urlopen(req, timeout=3).read()
                sou = soup(webpage,"lxml")
                list = sou.find_all('a', href=True)
                
                for a in list:
                    if "keywords" in a['href']:
                        # Clears irrelevant results that are displayed when ads are on and a link is appended only once
                        lin = origin+a['href']

                        if lin not in links and not "slredirect" in lin and ".tr/gp/" not in lin:
                            asin = asincode(lin)

                            if asin not in asinlist:
                                asinlist.append(asin)
                                links.append(lin)
                        else:
                            continue

            elif i == 1:
                url = f"{url0}"
                req = Request(url, headers=headers)
                webpage = urlopen(req, timeout=3).read()
                sou = soup(webpage,"lxml")
                list = sou.find_all('a', href=True)

                for a in list:
                    if "keywords" in a['href']:
                        # Clears irrelevant results that are displayed when ads are on and a link is appended only once
                        lin = origin+a['href']

                        if lin not in links and not "slredirect" in lin and ".tr/gp/" not in lin:
                            asin = asincode(lin)

                            if asin not in asinlist:
                                asinlist.append(asin)
                                links.append(lin)
                        else:
                            continue
   
            else:
                url = f"{url0}&page={i}"
                req = Request(url, headers=headers)
                webpage = urlopen(req, timeout=3).read()
                sou = soup(webpage,"lxml")
                list = sou.find_all('a', href=True)

                for a in list:
                    if "keywords" in a['href']:
                        # Clears irrelevant results that are displayed when ads are on and a link is appended only once
                        lin = origin+a['href']

                        if lin not in links and not "slredirect" in lin and ".tr/gp/" not in lin:
                            asin = asincode(lin)

                            if asin not in asinlist:
                                asinlist.append(asin)
                                links.append(lin)
                        else:
                            continue
             
            # req = Request(url, headers=headers)
            # webpage = urlopen(req, timeout=3).read()
            # sou = soup(webpage,"lxml")
            # list = sou.find_all('a', href=True)

            # for a in list:
            #     if "keywords" in a['href']:
            #         # Clears irrelevant results that are displayed when ads are on and a link is appended only once
            #         lin = origin+a['href']

            #         if lin not in links and not "slredirect" in lin and ".tr/gp/" not in lin:
            #             asin = asincode(lin)

            #             if asin not in asinlist:
            #                 asinlist.append(asin)
            #                 links.append(lin)
            #         else:
            #             continue
            #     if len(links) == limit:
            #         break
        links = links[0:limit]
        for i in links:
            try:
                twrv = utilities.ThreadWithReturnValue(target=detailedparser, args=(i,(links.index(i)+1), limit,))
                twrv.start()
            except:
                print("Sorry, the product could not be parsed.")
            if len(amazonlist) == limit:
                break
        
        twrv.join()
        return amazonlist

# searchtrendyol = AmazonTR("kitap")
# trendy = searchtrendyol.link()
# AmazonTR.parser(trendy, 6)