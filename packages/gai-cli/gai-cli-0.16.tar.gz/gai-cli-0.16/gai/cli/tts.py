from gai.client.GaigenClient import GaigenClient
import sys

def main():
    # Check if there's anything on stdin
    if not sys.stdin.isatty():
        input = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        # If not, check for command line argument
        input = sys.argv[1]
    else:
        raise ValueError("No input provided. Please provide input either via stdin or as a command line argument.")


    gaigen = GaigenClient()
    data = {
        "input": input,
        "voice": None,
        "language": None
    }
    response = gaigen("tts",**data)

    from gai.common.sound_utils import play_audio
    play_audio(response)

if __name__ == "__main__":
    main()