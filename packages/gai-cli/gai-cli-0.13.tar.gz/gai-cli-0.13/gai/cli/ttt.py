from gai.client.GaigenClient import GaigenClient
import sys

def main():
    argv=sys.argv
    content=argv[1] if len(argv)>1 else None

    gaigen = GaigenClient()
    data = {
        "messages":[{"role":"user","content":content}],
        "max_new_tokens":1000,
        "stream":True
    }
    for chunk in gaigen("ttt",**data):
        print(chunk.decode(),end="",flush=True)

if __name__ == "__main__":
    main()