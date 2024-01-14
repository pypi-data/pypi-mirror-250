from gai.client.GaigenClient import GaigenClient
from gai.tools.Chunker import Chunker
from gai.common.sound_utils import play_audio
import sys

def main():
    # Check if there's anything on stdin
    if sys.stdin.isatty():
        raise ValueError("Input is required via stdin only.")

    input = sys.stdin.read().strip()
    sentences = Chunker.sentences(input)

    # Read from stdin
    gaigen = GaigenClient()
    for sentence in sentences:
        data = {
            "input": sentence.strip()+"\n",
            "voice": None,
            "language": None
        }
        response = gaigen("tts",**data)
        play_audio(response)

if __name__ == "__main__":
    main()