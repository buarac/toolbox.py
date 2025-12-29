#!/usr/bin/env python3
"""
Web Scraper Tool 🕸️

A gentle, two-step web scraper that converts websites to Markdown files.

Steps:
1. Scan: Identify pages via sitemap.xml or crawling.
2. Scrape: Download pages and convert to Markdown with a polite delay.

Usage:
    python3 scripts/web_scraper/scraper.py --url <URL> --output <DIR> --step scan
    python3 scripts/web_scraper/scraper.py --output <DIR> --step scrape
"""
import argparse
import json
import logging
import os
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


def setup_args():
    parser = argparse.ArgumentParser(description="Web Scraper Tool")
    parser.add_argument("--url", type=str, help="Target URL (required for scan)")
    parser.add_argument(
        "--output", type=str, required=True, help="Output directory for data"
    )
    parser.add_argument(
        "--step",
        choices=["scan", "scrape"],
        default="scan",
        help="Action to perform (default: scan)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)",
    )
    return parser.parse_args()


def get_sitemap_urls(base_url):
    """Attempt to fetch URLs from sitemap.xml"""
    sitemap_url = urljoin(base_url, "/sitemap.xml")
    logging.info(f"🔎 Checking for sitemap at: {sitemap_url}")

    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "xml")
            urls = [loc.text for loc in soup.find_all("loc")]
            if urls:
                logging.info(f"✅ Found {len(urls)} URLs in sitemap.")
                return urls
    except Exception as e:
        logging.warning(f"⚠️ Could not fetch sitemap: {e}")

    return []


def crawl_site(base_url, max_pages=50):
    """Simple BFS crawl restricted to the same domain."""
    logging.info(f"🕷️ Starting crawl on {base_url} (limit: {max_pages} pages)...")
    
    domain = urlparse(base_url).netloc
    visited = set()
    queue = [base_url]
    found_urls = []

    while queue and len(found_urls) < max_pages:
        current_url = queue.pop(0)

        if current_url in visited:
            continue
        visited.add(current_url)
        found_urls.append(current_url)

        try:
            response = requests.get(current_url, timeout=5)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            for link in soup.find_all("a", href=True):
                href = link["href"]
                full_url = urljoin(base_url, href)
                parsed = urlparse(full_url)

                # Only follow internal links
                if parsed.netloc == domain and full_url not in visited and full_url not in queue:
                    # Filter out non-html extensions
                    if not any(full_url.endswith(ext) for ext in [".png", ".jpg", ".pdf", ".css", ".js"]):
                         # Minimal fragment handling
                         queue.append(full_url.split('#')[0])

        except Exception as e:
            logging.warning(f"Failed to crawl {current_url}: {e}")
            
    logging.info(f"✅ Crawl finished. Found {len(found_urls)} URLs.")
    return found_urls


def step_scan(url, output_dir):
    """Step 1: Identify pages to scrape."""
    if not url:
        logging.error("❌ --url is required for scanning.")
        return

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Strategy: Sitemap first, then Crawl
    urls = get_sitemap_urls(url)
    if not urls:
        logging.info("⚠️ No sitemap found. Falling back to crawler.")
        urls = crawl_site(url)

    if not urls:
        logging.error("❌ No URLs found. Exiting.")
        return

    # Save results
    sitemap_file = output_path / "sitemap.json"
    data = {"base_url": url, "urls": list(set(urls))} # De-duplicate
    
    with open(sitemap_file, "w") as f:
        json.dump(data, f, indent=2)

    logging.info(f"💾 Plan saved to {sitemap_file}")
    logging.info(f"📊 Total Pages identified: {len(data['urls'])}")
    logging.info("👉 Ready for Step 2. Run with '--step scrape'")


def clean_filename(url):
    """Generate a safe filename from URL."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        return "index"
    return path.replace("/", "_").replace("-", "_")


def step_scrape(output_dir, delay):
    """Step 2: Scrape pages and convert to Markdown."""
    output_path = Path(output_dir)
    sitemap_file = output_path / "sitemap.json"

    if not sitemap_file.exists():
        logging.error(f"❌ No scan file found at {sitemap_file}. Run 'scan' first.")
        return

    with open(sitemap_file, "r") as f:
        data = json.load(f)
    
    urls = data.get("urls", [])
    if not urls:
        logging.warning("⚠️ matches found in sitemap.json.")
        return

    logging.info(f"🚀 Starting scrape of {len(urls)} pages with {delay}s delay...")
    
    # Progress bar iteration
    for url in tqdm(urls, desc="Scraping", unit="page"):
        try:
            # Polite delay
            time.sleep(delay)
            
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                logging.warning(f"Failed to fetch {url} (Status: {response.status_code})")
                continue

            # Convert to Markdown
            markdown_content = md(response.text, heading_style="ATX")
            
            # Metadata header
            header = f"---\nurl: {url}\ndate: {time.strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n"
            full_content = header + markdown_content

            # Save file
            filename = clean_filename(url) + ".md"
            file_path = output_path / filename
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(full_content)
                
        except Exception as e:
            logging.error(f"Error scraping {url}: {e}")

    logging.info(f"✨ Scraping complete! Files saved in {output_dir}")


def main():
    args = setup_args()

    if args.step == "scan":
        step_scan(args.url, args.output)
    elif args.step == "scrape":
        step_scrape(args.output, args.delay)


if __name__ == "__main__":
    main()
