from gai.client.ChunkWrapper import ChunkWrapper
import gai.common.ConfigHelper as ConfigHelper
from gai.common.http_utils import http_post
from gai.common.image_utils import base64_to_imageurl
API_BASEURL = ConfigHelper.get_api_baseurl()

class ITTClient:

    def __call__(self, model="llava-transformers", base64_image=None, message_text=None, stream=True, **model_params):
        if not base64_image:
            raise Exception("The parameter 'base64_imageurl' is required.")
        if not message_text:
            message_text="Describe this image."

        base64_imageurl = base64_to_imageurl(base64_image)
        data = {
            "model": model,
            "messages": [
                {"role":"user",
                "content":[
                    {"type":"text","text":message_text},
                    {"type":"image_url","image_url":base64_imageurl}
                ]}
            ],
            "stream": stream,
        }

        def streamer(response):
            for chunk in response.iter_lines():
                yield ChunkWrapper(chunk)

        response = http_post(f"{API_BASEURL}/gen/v1/vision/completions",data)
        if not stream:
            response.decode = lambda: response.json()["choices"][0]["message"]["content"]
            return response
        return streamer(response)
    
