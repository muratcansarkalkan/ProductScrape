# Product Scraper
Brief Description: A script that scrapes Amazon TR and Trendyol products.

<h3>Introduction:</h3>
<ul>
<li>Amazon, a multinational technology company and a leader in international e-commerce business and** Trendyol**, one of the local e-commerce leaders which is valued around $16 billion, are the most common webpages for shopping online.</li>
<li>In this program, we will parse the products by the query and number of results wanted from each webpage. There are no other parameters that are needed to be given. There are 4 scripts inside the program.</li>
<li>With multithread function, there is no need to wait for web parsing to be completed link-by-link. When parsing is complete for a product, it is written to the JSON file. In any event, we will have a JSON file, even though specific crashes occur.</li>
</ul>

<h3>How does it work?</h3>
<ol>
<li>Run Windows PowerShell, then type python main.py.</li>
<li>You will be asked for query first, type a query.</li>
<li>Then you will be asked how many product results you want for each website. If you don&#39;t give a number, the program will be annoyed and quit.</li>
<li>Then, the search starts. After search, product links are prepared to be scraped as a list. For Amazon&#39;s scraping, some products not related to our search query are discarded. Also, if a product has the same link, it is not included.</li>
<li>Then the product results are appended to a list of links. These links are visited, then the product&#39;s title, price and specific ID (for Amazon, it is ASIN, while Trendyol, it&#39;s at end of the TITLE) with a link to visit.</li>
<li>The outputs are written to a JSON file (&quot;results.json&quot;) one by one, so when the whole process is complete, no successfully parsed result will be left out.</li>
</ol>

<ul>
<li>Timeout function is also included for both search result and product webpage parsing.</li>
<li>The program is available to scrape both Amazon and Trendyol.</li>
<li>Headers for URL requests are switched randomly, in order to increase efficiency of web scraping, as the websites doesn&#39;t allow visits without User Agents.</li>
<li>Here is an example of the program running.</li>
</ul>

![](https://i.imgur.com/rxefnCW.png)

<h3>Errors and Limitations:</h3>
<ul>
<li>Amazon&#39;s search results that HTML parser parsed can give 14 results per page. The number for Trendyol is 24.</li>
<li>Trendyol can load up to 208 pages. This means we can have a max results of 4992.</li>
<li>When the search link is unavailable, the script prints an error as &quot;Sorry, we could not find any products regarding your search from Amazon/Trendyol. (HTTP 503 Error)&quot; If a website is unavailable, the script continues running and moves onto next website. Amazon tends to have this error more than Trendyol does.</li>
<li>When the product link is unavailable, the script prints an error as &quot;Sorry, the product could not be parsed.&quot;</li>
<li>After the parsing process is complete, you can open results.json to see product ID, name, price and link.</li>
</ul>
