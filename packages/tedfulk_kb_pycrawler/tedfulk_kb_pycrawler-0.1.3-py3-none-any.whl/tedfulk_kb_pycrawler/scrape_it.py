import asyncio
import glob
import json
from playwright.async_api import async_playwright
from tedfulk_kb_pycrawler.models import WebPage, Knowledgebase, Config, NoSitemapError


async def scrape_website(config: Config):
    """
    Scrape the specified websites and generate a knowledgebase.

    Args:
        config (Config): Configuration object containing the URLs, output file name, and max pages to crawl.

    Raises:
        NoSitemapError: If no sitemap.xml is found for a given URL.

    Returns:
        None
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        for url, output_file_name in zip(config.urls, config.output_file_name):
            knowledgebase = Knowledgebase(kb=[])
            sitemap_url = url + "/sitemap.xml"
            response = await page.goto(sitemap_url)
            if response.status == 404:
                raise NoSitemapError(f"No sitemap.xml found for {url}")
            urls = await page.evaluate(
                '() => Array.from(document.querySelectorAll("loc")).map(e => e.textContent)'
            )
            for i, url in enumerate(urls):
                if (
                    config.max_pages_to_crawl is not None
                    and i >= config.max_pages_to_crawl
                ):
                    break
                await page.goto(url)
                body_content = await page.evaluate("() => document.body.textContent")
                web_page = WebPage(url=url, content=body_content)
                web_page.content = (
                    web_page.content.replace("\n", " ")
                    .replace("\t", " ")
                    .replace("\u2014", " ")
                    .replace("\u00b6", " ")
                    .replace("\u00a0", " ")
                    .replace("\u00ae", " ")
                    .replace("\u00b7", " ")
                    .replace("   ", " ")
                    .replace("    ", " ")
                    .replace("     ", " ")
                    .replace("       ", " ")
                )
                knowledgebase.kb.append(web_page)
            output_filename = get_output_filename(output_file_name)
            with open(output_filename, "w") as f:
                json.dump(knowledgebase.model_dump(), f, separators=(",", ":"))
            print(f"Knowledgebase written to {output_filename}")
        await browser.close()


def get_output_filename(file_name: str):
    json_files = glob.glob(f"{file_name}*.json")
    count = len(json_files) + 1
    output_filename = f"{file_name}-{count}.json"
    return output_filename


def scrape_it(config: Config):
    try:
        asyncio.run(scrape_website(config))
    except NoSitemapError as e:
        print(str(e))


# Create a Config instance with the desired URLs, output file name, and max pages to crawl
# Don't forget to add the trailing slash to the URL
# config = Config(
#     urls=[
#         # "https://jxnl.github.io/instructor/",
#         "https://turso.tech",
#     ],
#     output_file_name=["turso"],  # default is "output"
#     # output_file_name=["instructor", "turso"],  # default is "output"
#     max_pages_to_crawl=2,  # default is 10
# )
# scrape_it(config)
