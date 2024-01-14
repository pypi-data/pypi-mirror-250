from gai.tools.Googler import Googler
import sys

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: gg <search term>")
        sys.exit(1)
    search_term = args[0]
    results = Googler.google(search_term)
    for result in results:
        print(result["title"])
        print(result["url"])
        print()

if __name__ == "__main__":
    main()
