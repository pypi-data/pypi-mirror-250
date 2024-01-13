import gai.common.ConfigHelper as ConfigHelper
from gai.common.http_utils import http_post
API_BASEURL = ConfigHelper.get_api_baseurl()

class STTClient:

    def __call__(self, generator=None, file=None):
        if not file:
            raise Exception("No file provided")
        
        files = {
            "model": (None,generator),
            "file": (file.name, file.read())
        }

        response = http_post(f"{API_BASEURL}/gen/v1/audio/transcriptions",files=files)
        response.decode = lambda: response.json()["text"]
        return response