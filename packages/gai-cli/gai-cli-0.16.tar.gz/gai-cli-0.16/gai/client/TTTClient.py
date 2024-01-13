from gai.client.ChunkWrapper import ChunkWrapper
import gai.common.ConfigHelper as ConfigHelper
from gai.common.http_utils import http_post
from gai.common.utils import chat_string_to_list

API_BASEURL = ConfigHelper.get_api_baseurl()

class TTTClient:

    def __call__(self, generator=None, messages=None, stream=True, **generator_params):
        if not messages:
            raise Exception("Messages not provided")
        
        if isinstance(messages,str):
            messages = chat_string_to_list(messages)

        api_config = ConfigHelper.get_api_config()
        if not generator:
            generator = api_config["default_generator"]

        data = {
            "model": generator,
            "messages":messages,
            "stream":stream,
            **api_config["generators"][generator]["default"],
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

