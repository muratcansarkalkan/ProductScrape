import urllib.request, urllib.parse, urllib.error
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import utilities
import time
import random
import json

outfile = open('resultstrendyol.json', 'w', encoding='utf8')

# Randomly switches User Agents to minimize 503 Errors.
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

user_agent = random.choice(user_agent_list)

# Specifies the header.
headers = {'User-Agent': user_agent}

main = "https://www.trendyol.com"
trendyollist = []

class Trendyol():
    def __init__(self, query):
        self.query = query
    
    def link(self):
        link = "https://www.trendyol.com/sr?"

        if len(self.query) > 0:
            query = (urllib.parse.quote(self.query).replace("%20","+"))
            link = link+"q="+query
            return link
        else:
            return link
    
    def parser(url0, limit):
        def cardsingle(url):
            req = Request(url, headers=headers)
            webpage = urlopen(req, timeout=3).read()
            sou = soup(webpage, "html.parser")
            cardsingle = sou.findAll("div","p-card-wrppr")
            return cardsingle

        def detailedparser(c,r,limit):
            try:
                # Prepares the product card.
                regextitle = re.compile('.*prdct-desc-cntnr-name.*')
                print(f"Trying to parse {r} of {limit} results from Trendyol...")
                title = str(c.find("span", {"class" : regextitle})['title'])
                price = str(c.find("div", class_="prc-box-dscntd").string)

                if "TL" not in price:
                    price = "Not available, please view the product page"
                
                productlink = main+str(c.find("a")['href'])

                req = Request(productlink, headers=headers)
                webpage = urlopen(req, timeout=5).read()
                sou = soup(webpage, "html.parser")

                id3 = (sou.find("h1",class_="pr-new-br"))
                id = (id3.text).split()[-1]

                product = utilities.ProductCard(id, title, price, productlink)
                print(f"Parsing successful for product {r}.")
                
                if len(trendyollist) < limit:
                    jsonTrendyolStr = json.dumps(product.__dict__, indent=1, ensure_ascii=False)
                    outfile.write(jsonTrendyolStr)
                    trendyollist.append(product)
                else:
                    print("Max limit")
                time.sleep(1)
                    
            except:
                print("Sorry, product could not be parsed")
        # Defines page and product cards. Results per page was 24
        pages = (limit // 24)
        card = []
        
        for i in range(1,pages + 2):
            if i == pages+1:
                url = f"{url0}&pi={i}"
                cardsingle = cardsingle(url)
                # Strips the number of output using remainder func
                cardtup = cardsingle[0:limit % 24]
                card = card+cardtup
            elif i == 1:
                url = f"{url0}"
                cardtup = cardsingle(url)
                card = card+cardtup
            else:
                url = f"{url0}&pi={i}"
                cardtup = cardsingle(url)
                card = card+cardtup

        for c in card:
            try:
                # Starts parsing products
                twrv = utilities.ThreadWithReturnValue(target=detailedparser, args=(c,(card.index(c)+1), limit,))
                twrv.start()
            except:
                print("Sorry, the product could not be parsed.")
        # Closes
        twrv.join()
        return trendyollist

# searchtrendyol = Trendyol("kitap")
# trendy = searchtrendyol.link()
# Trendyol.parser(trendy, 96)