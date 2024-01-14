from gai.tools.Scraper import Scraper
import sys

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: scrape <url>")
        sys.exit(1)

    url = args[0]
    text, links = Scraper.scrape(url)
    print(text)

if __name__ == "__main__":
    main()