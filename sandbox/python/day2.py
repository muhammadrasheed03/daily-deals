import asyncio
import time
from datetime import datetime
from backend.models import Product, PriceHistory, ScraperError



async def scrape_product(url: str, delay: float) -> Product:
    print(f"Starting scrape: {url}")
    await asyncio.sleep(delay)
    print(f"Finished scrape: {url}")
    return Product(
        name=f"Product from {url}",
        url=url,
        price=99.99,
        original_price=129.99,
        retailer=url.split(".")[1],
        scraped_at=datetime.now()

    )

async def scrape_sequential(urls: list[str])->list[Product]:
    products = []
    for url in urls:
        product = await scrape_product(url, delay=2.0)
        products.append(product)
    return products

async def scrape_concurrent(urls: list[str]) -> list[Product]:
    tasks = [
        scrape_product(urls[0], delay=3.0),
        scrape_product(urls[1], delay=1.0),
        scrape_product(urls[2], delay=2.0),
        scrape_product(urls[3], delay=0.5),
        scrape_product(urls[4], delay=1.5),
    ]
    return await asyncio.gather(*tasks)

async def main():
    urls = [
        "https://amazon.com/laptop",
        "https://target.com/laptop",
        "https://bestbuy.com/laptop",
        "https://walmart.com/laptop",
        "https://newegg.com/laptop",
    ]

    # sequential
    print('--- Sequential ---')
    start = time.perf_counter()
    sequential_results = await scrape_sequential(urls)
    sequential_time = time.perf_counter()-start
    print(f"Sequential took: {sequential_time:.2f}s for {len(sequential_results)} products\n")

    # concurrent
    print("--- Concurrent ---")
    start = time.perf_counter()
    concurrent_results = await scrape_concurrent(urls)
    concurrent_time = time.perf_counter()-start
    print(f"Concurrent took: {concurrent_time:.2f}s for {len(concurrent_results)} products\n")

    print(f"Speedup: {sequential_time / concurrent_time:.1f}x faster")


asyncio.run(main())