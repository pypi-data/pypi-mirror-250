# Python Web Scraper

This script utilizes the **Playwright library** for scraping websites and generating a knowledgebase.

## Main Function: `scrape_website(config: Config)`

### Parameters

- `config`: An object containing URLs to scrape, output file name, and a limit on pages to crawl.

### Workflow

1. **Launch Chromium Browser**: Uses Playwright to start a new browser instance.
2. **URL Iteration**: For each URL in the `Config` object:
   - **Sitemap Processing**:
     - Navigate to `sitemap.xml`.
     - Raise `NoSitemapError` if not found, else extract URLs.
   - **Page Processing**: For each URL in the sitemap:
     - Stop if `max_pages_to_crawl` is reached.
     - Navigate to the URL and extract the page content.
     - Create a `WebPage` object with URL and content.
     - Clean content and add to `Knowledgebase` object.

### Output Generation

- **Knowledgebase to JSON**: Writes the `Knowledgebase` object to a JSON file.
- **Unique Filenames**: Uses `get_output_filename(file_name: str)` to ensure unique file names.
- **Browser Closure**: Closes the browser and proceeds to the next URL.
- **Error Handling**: Prints `NoSitemapError` to console if encountered.
