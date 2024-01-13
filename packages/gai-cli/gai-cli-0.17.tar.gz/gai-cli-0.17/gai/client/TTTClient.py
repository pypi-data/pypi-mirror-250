from gai.client.ChunkWrapper import ChunkWrapper 
from gai.client.OpenAIChunkWrapper import OpenAIChunkWrapper
import gai.common.ConfigHelper as ConfigHelper
from gai.common.http_utils import http_post
from gai.common.utils import chat_string_to_list
import json

API_BASEURL = ConfigHelper.get_api_baseurl()

class TTTClient:

    def api(self, generator=None, messages=None, stream=True, **generator_params):
        if not messages:
            raise Exception("Messages not provided")
        
        if isinstance(messages,str):
            messages = chat_string_to_list(messages)

        cli_config = ConfigHelper.get_cli_config()
        if not generator:
            generator = cli_config["default_generator"]

        data = {
            "model": generator,
            "messages":messages,
            "stream":stream,
            **cli_config["generators"][generator]["default"],
            **generator_params
            }

        def streamer(response):
            for chunk in response.iter_lines():
                yield ChunkWrapper(chunk)

        response = http_post(f"{API_BASEURL}/gen/v1/chat/completions",data)
        if not stream:
            response.decode = lambda: response.json()["choices"][0]["message"]["content"]
            return response
        return streamer(response)        


    def __call__(self, generator=None, messages=None, stream=True, **generator_params):
        if generator=="gpt-4":
            return self.gpt_4(messages=messages,stream=stream,**generator_params)
        return self.api(generator,messages,stream,**generator_params)


    def gpt_4(self, messages=None, stream=True, **generator_params):
        import os, openai
        from openai import OpenAI
        from dotenv import load_dotenv        
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]
        client = OpenAI()

        if not messages:
            raise Exception("Messages not provided")
       
        def streamer(response):
            for chunk in response:
                yield OpenAIChunkWrapper(chunk)

        model="gpt-4"
        if isinstance(messages,str):
            messages = chat_string_to_list(messages)
        response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        stream=stream,
                        **generator_params
                    )

        if not stream:
            response.decode = lambda: response.choices[0].message.content
            return response
        return streamer(response) 