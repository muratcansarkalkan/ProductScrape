import ssl
import urllib.parse, urllib.error
import json
import amazontr
import trendyol
from utilities import ThreadWithReturnValue
from threading import Thread

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Asks for what would you like to search:
query = input("Search by product...")

# If you don't have a number input it quits.
try:
    limit = int(input("How many results do you want?"))
except ValueError:
    print("No, please give a number!")
    print("As you didn't give a number, I will quit.")
    quit()

# Defines query for Amazon and Trendyol
searchamazon = amazontr.AmazonTR(query)
searchtrendyol = trendyol.Trendyol(query)

# Executes query link adaptations
amazon = searchamazon.link()
trendy = searchtrendyol.link()

# JSON file is demonstrated
outfile = open('results.json', 'w', encoding='utf8')

# Tries to produce a result from search links, if there are no results, then it prints a message.
# Threading is used in case one of them takes too much time.
print("Looking up...")

try:
    # Runs parser
    proam = ThreadWithReturnValue(target=(amazontr.AmazonTR.parser), args=(amazon, limit))
    # Start is starting the defined threads, while join is for making sure thread dies
    proam.start()
    # As we used thread with return value, resultam and resulttr are lists we wanted
    resultam = proam.join()
    # Lists are converted to JSON format then written to JSON.
    # jsonAmazonTRStr = json.dumps([i.__dict__ for i in resultam], indent=1, ensure_ascii=False)
    # outfile.write(jsonAmazonTRStr)
except:
    print("Sorry, we could not find any products regarding your search from Amazon. Checkout the error above")

try:
    # Runs parser
    protr = ThreadWithReturnValue(target=(trendyol.Trendyol.parser), args=(trendy, limit))
    # Start is starting the defined threads, while join is for making sure thread dies
    protr.start()
    # As we used thread with return value, resultam and resulttr are lists we wanted
    # Lists are converted to JSON format then written to JSON.
    resulttr = protr.join()
    # jsonTrendyolStr = json.dumps([i.__dict__ for i in resulttr], indent=1, ensure_ascii=False)
    # outfile.write(jsonTrendyolStr)
except:
    print("Sorry, we could not find any products regarding your search from Trendyol. Checkout the error above")
