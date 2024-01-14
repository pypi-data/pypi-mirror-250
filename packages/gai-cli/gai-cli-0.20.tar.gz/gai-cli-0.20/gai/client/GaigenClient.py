from gai.client.TTTClient import TTTClient
from gai.client.STTClient import STTClient
from gai.client.TTSClient import TTSClient
from gai.client.ITTClient import ITTClient
from gai.client.RAGClient import RAGClient

class GaigenClient:

    def __call__(self, category, **model_params):
        if category.lower() == "ttt":
            ttt = TTTClient()
            return ttt(**model_params)
        elif category.lower() == "stt":
            stt = STTClient()
            return stt(**model_params)
        elif category.lower() == "tts":
            tts = TTSClient()
            return tts(**model_params)
        elif category.lower() == "itt":
            itt = ITTClient()
            return itt(**model_params)
        elif category.lower() == "index":
            rag = RAGClient()
            return rag.index_file(**model_params)
        elif category.lower() == "retrieve":
            rag = RAGClient()
            return rag.retrieve(**model_params)
        else:
            raise Exception(f"Unknown category: {category}")
