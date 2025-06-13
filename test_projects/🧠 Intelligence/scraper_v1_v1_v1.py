# Sample web scraper with intentional issues
from datetime import datetime

import bs4
import requests


def scrape_website(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    # Missing error handling
    title = soup.find("title").text

    # Unused variable
    current_time = datetime.now()

    return title


def main():
    url = "https://example.com"
    result = scrape_website(url)
    print(result)


if __name__ == "__main__":
    main()
