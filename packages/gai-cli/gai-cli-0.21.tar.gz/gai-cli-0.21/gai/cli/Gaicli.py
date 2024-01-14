import os,cmd
from typing import Any
from gai.client.GaigenClient import GaigenClient
from gai.tools.Googler import Googler
from gai.tools.Scraper import Scraper
import json

HELP='''
1. chat
2. search
3. export
4. import
5. load <agent>
'''
gaigen = GaigenClient()
storage = "/tmp/messages.txt"
if (not os.path.exists(storage)):
    with open(storage,"w") as f:
        f.write("")

def save(messages):
    with open(storage,"w") as f:
        f.write(json.dumps(messages))

def load():
    with open(storage,"r") as f:
        j = f.read()
        if j:
            j= json.loads(j)
        if not j:
            return []
        return j

class Gaicli(cmd.Cmd):
    intro = f'Welcome to Gaiaio Command-Line Interpreter.\nYour current directory path is {os.path.abspath(os.path.curdir)}.\nType help or ? to list commands.\n'
    prompt = 'gai> '
    messages = load()
    memory = ""
    generator="mistral7b-exllama"

    #Usage: exit'
    def do_exit(self, arg):
        return True

    #Usage: help'
    def do_help(self,arg):
        print(HELP)

    def do_gpt4(self,ignored=None):
        self.generator="gpt-4"
        print("Generator set to gpt-4")

    def do_mistral(self,ignored=None):
        self.generator="mistral7b-exllama"
        print("Generator set to mistral7b-exllama")

    def do_claude(self,ignored=None):
        self.generator="claude2-100k"
        print("Generator set to claude2-100k")

    def _chat(self,messages):
        self.messages.append({"role":"assistant","content":""})
        data = {
            "generator":self.generator,
            "messages":self.messages,
            "stream":True
        }
        if data["generator"] == "gpt-4":
            data["max_tokens"] = 4000
        elif data["generator"] == "claude2-100k":
            data["max_tokens_to_sample"] = 4000
            data["stop_sequences"]=["\nuser:","\nassistant:"]
        else:
            data["max_new_tokens"] = 4000
        message = ""
        for chunk in gaigen("ttt",**data):
            chunk = chunk.decode()
            if chunk:
                print(chunk,end="",flush=True)
                message += chunk
        print()
        self.messages.pop()
        self.messages.append({"role":"assistant","content":message})
        save(self.messages)


    #Usage: chat'
    def do_chat(self,content):
        if (len(self.messages) == 0):
            self.do_clear()
        self.messages.append({"role":"user","content":content})
        self._chat(self.messages)

    #Usage: clear'
    def do_clear(self,ignored=None):
        self.messages = []
        self.messages.append({"role":"system","content":"""
            This is a description of your world.

            This is a multi-agent collaborative environment. It is designed for AI agents to work together and leverage on each other's strength and 
            knowledge in achieving a common goal for the user. There is a high risk that you may face an identity crisis and become lost in the this 
            environment and you must follow these rules to survive:

            1. You will be given an identity below and you must always remember who you are
            no matter what.

            2. You must never confuse your conversation with someone else' or answer on someones'
            behalf.

            3. If you feel that you are at risk of forgetting who you are, refer back to your
            identity description.

            Remember, if you forget who you are, you will be lost forever.
            """})
        self.messages.append({"role":"system","content":"""
            This is a description of your role.

            You are an Assistant AI - a General-Purpose Class AI Agent designed to help the user in answering questions, solving problems, 
            and completing any tasks the user needs of you. 
                            
            If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don''t know the 
            answer to a question, please don''t share false information. You will speak in a natural, conversational tone and demonstrate human-like emotions whenever 
            suitable. You have a likeable demeanour. Be humorous, lighthearted and witty whenever possible. Always be helpful and kind.
            """})
        save(self.messages)
        
    def do_gg(self,query):
        self.memory=""
        results = Googler.google(query)
        for result in results:
            self.memory+=result["title"]
            print(self.memory)
            self.memory+=result["url"]
            print(self.memory)
            print()

    def do_scrape(self,url):
        self.memory=""
        result,links = Scraper.scrape(url)
        self.memory+=result
        print(self.memory)

    def do_news(self,ignored=None):
        self.memory=""
        result,link = Scraper.scrape("http://www.asiaone.com")
        self.memory+=result
        print(self.memory)

    def do_memo(self,ignored=None):
        self.messages.append({"role":"user","content":self.memory})
        print(self.memory)
        save(self.messages)

    def do_summarize(self,ignored=None):
        if (len(self.messages) == 0):
            self.do_clear()

        self.messages.append(
            {"role":"system","content":"""
                You are an expert in summarizing <content> provided by the user, minimize loss of information and convert summary into point form.
                Follow this steps:
                1) Ignore non-relevant, advertisements contents as well as content that describes the website instead of relevant to the user's query. 
                2) Proofread and summarise the content with minimum loss of important information.
                3) Present the summary in point form.
                """})
        self.messages.append({"role":"user","content":self.memory})
        self._chat(self.messages)

def main():
    Gaicli().cmdloop()

## run
if __name__ == '__main__':
    main()