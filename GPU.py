# crawler.py
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def crawl_page(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0")
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        # Extract JS, data-*, and src tags
        scripts = [script.get("src") for script in soup.find_all("script") if script.get("src")]
        iframes = [iframe.get("src") for iframe in soup.find_all("iframe") if iframe.get("src")]
        data_tags = [tag.attrs for tag in soup.find_all() if any(attr.startswith("data-") for attr in tag.attrs)]

        await browser.close()
        return {"url": url, "scripts": scripts, "iframes": iframes, "data_tags": data_tags}

urls = [
    "https://www.autocarindia.com",
    "https://www.charzer.com"
]

async def main():
    results = await asyncio.gather(*(crawl_page(url) for url in urls))
    for result in results:
        print(result)

asyncio.run(main())
