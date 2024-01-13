import json
class ChunkWrapper:

    # chunk is json in binary representation
    def __init__(self, chunk):
        self.chunk = chunk

    def __str__(self):
        return self.chunk.decode('utf-8')

    def decode(self):
        decoded_chunk = json.loads(self.chunk.decode('utf-8'))
        return decoded_chunk["choices"][0]["delta"]["content"]
    
    def __dict__(self):
        return json.loads(self.chunk.decode('utf-8'))

