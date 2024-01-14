from gai.tools.Googler import Googler
from gai.tools.Scraper import Scraper
from gai.client.GaigenClient import GaigenClient
from gai.common.logging import logging
logger = logging.getLogger(__name__)
import sys
import time

def main():
    start_time = time.time()
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: gg <search term>")
        sys.exit(1)
    search_term = args[0]
    results = Googler.google(search_term)
    gaigen = GaigenClient()
    summaries = ""
    n_results = 0
    max_results= 9
    for result in results:
        if n_results > max_results:
            break
        try:
            logger.info(f"Analysing {result['url']}...")
            # print(f"Link:{result['url']}")
            content = Scraper.scrape(result["url"])
            # print("Content:")
            data = {
                "messages":[
                    {"role":"system","content":"""You are an expert in summarizing <content> provided by the user that is scraped from the web and convert into point form summaries.
                    Follow this steps:
                    1) Ignore non-relevant, advertisements contents as well as content that describes the website instead of relevant to the user's query. 
                    2) Proofread and summarise the content relevant to the user's search.
                    3) Present the summary in point form."""},
                    {"role":"user","content":f"Summarize this <content>{content}</content>"},
                    {"role":"assistant","content":""},
                    ],
                "max_new_tokens":2000,
                "stream":False
            }
            summaries += gaigen("ttt",**data).decode() + "\n"
            n_results += 1
        except:
            continue
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"\nElapsed time: {elapsed_time} seconds")

    data = {
        "messages":[
            {"role":"user","content":f"Extact, proofread and summarize <content>{summaries}</content> that is relevant to {search_term} into point forms."},
            {"role":"assistant","content":""},
            ],
        "max_new_tokens":4000,
        "stream":True
    }
    for chunk in gaigen("ttt",**data):
        print(chunk.decode(),end="",flush=True)


if __name__ == "__main__":
    main()
