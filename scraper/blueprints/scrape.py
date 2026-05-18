from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup
from html import unescape

#a Blueprint is a group of related routes
#like a mini flask app that gets registered onto the main app
#name = "scrape" is used internally by Flask for url_for() lookups
scrape_bp = Blueprint("scrape", __name__)

@scrape_bp.get("/scrape")
def scrape_product():
    """
    Accepts a URL as a query parameter, fetches the page,
    and returns whatever structured data it can extract.

    Example: GET /api/scrape?url=https://books.scrape.com/catalogue/a-light-in-the-attic_1000/index.html
    """
    #get the url from query params - e.g. /api/scrape?url=https://
    url = request.args.get("url")

    #validate that a URL was actually provided
    if not url:
        return jsonify({"error": "url parameter is required"}), 400
    
    try:
        #requests.get() fetches the page - synchronous, blocks until response
        #headers pretend we're a browser so sites don't immediately block us
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }, timeout=10)

        #raise an exception if the status code is 4xx or 5xx

        #BeautifulSoup parses the raw HTl into a navigable tree
        # "lxml" is the parser - fast and lenient with malformed HTML
        soup = BeautifulSoup(response.content, "lxml")

        #extract text from the page
        #these selectors work for books.toscrape.com - safe practice site
        title = soup.select_one("h1")
        price = soup.select_one(".price_color")
        availability= soup.select_one(".availability")

        return jsonify({
            "url": url,
            "title": title.text.strip() if title else None,
            "price": unescape(price.text.strip()) if price else None,
            "availability": availability.text.strip() if availability else None,
            "status":"success"
        })
    
    except requests.exceptions.Timeout:
        return jsonify({"error": "request timed out", "url": url}), 504
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e), "url": url}), 502


RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

@scrape_bp.get("/scrape/books")
def scrape_books():
    """
    Scrapes the main listing page of books.toscrape.com and returns
    every book on the page with its title, price, and star rating.

    Example: GET /api/scrape/books
    """
    url = "https://books.toscrape.com"
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.content, "lxml")
        books = []
        for article in soup.select("article.product_pod"):
            title = article.select_one("h3 > a")["title"]
            price = unescape(article.select_one(".price_color").text.strip())
            # Rating is encoded as a CSS class name, e.g. <p class="star-rating Three">
            rating_class = article.select_one("p.star-rating")["class"][1]
            rating = RATING_WORDS.get(rating_class)
            books.append({"title": title, "price": price, "rating": rating})

        return jsonify({"status": "success", "count": len(books), "books": books})

    except requests.exceptions.Timeout:
        return jsonify({"error": "request timed out"}), 504

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502