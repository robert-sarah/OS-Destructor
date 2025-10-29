#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich Web Crawler"""

from rich.console import Console
from rich.progress import Progress
import requests
from bs4 import BeautifulSoup
import urllib.parse

console = Console()

class WebCrawler:
    def __init__(self):
        self.visited = set()
        
    def crawl(self, url, max_pages=10):
        """Crawl website"""
        console.print(f"[bold green]Crawling: {url}[/bold green]")
        
        with Progress() as progress:
            task = progress.add_task("Crawling...", total=max_pages)
            
            for i in range(max_pages):
                try:
                    response = requests.get(url, timeout=5)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    console.print(f"Page {i+1}: {url}")
                    progress.advance(task)
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    crawler = WebCrawler()
    crawler.crawl("https://example.com")

