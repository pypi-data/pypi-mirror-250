from gai.common.http_utils import http_post
import gai.common.ConfigHelper as ConfigHelper
API_BASEURL = ConfigHelper.get_api_baseurl()

class TTSClient:

    def __call__(self, input, generator="xtts-2", stream=True,**generator_params):
        if not input:
            raise Exception("The parameter 'input' is required.")
        data = {
            "model": generator,
            "input": input,
            "stream": stream,
            **generator_params
        }
        response = http_post(f"{API_BASEURL}/gen/v1/audio/speech",data)
        return response

