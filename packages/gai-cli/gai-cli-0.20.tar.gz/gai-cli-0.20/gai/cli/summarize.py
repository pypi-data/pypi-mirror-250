from gai.client.GaigenClient import GaigenClient
import sys

def main():
    content=""
    for line in sys.stdin:
        content+="\n"+line

    gaigen = GaigenClient()
    data = {
        "messages":[
            {"role":"system","content":"""
                You are an expert in summarizing <content> provided by the user and convert into point form summaries.
                Follow this steps:
                1) Ignore non-relevant, advertisements contents as well as content that describes the website instead of relevant to the user's query. 
                2) Proofread and summarise the content with minimum loss of important information.
                3) Present the summary in point form.
                """},
            {"role":"user","content":content},
            {"role":"assistant","content":""},
            ],
        "max_new_tokens":4000,
        "stream":True
    }
    for chunk in gaigen("ttt",**data):
        print(chunk.decode(),end="",flush=True)

if __name__ == "__main__":
    main()