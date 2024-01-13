import sys
from nltk.tokenize import sent_tokenize

def main():
    # Read from stdin
    input_text = sys.stdin.read().strip()

    # Split into sentences
    sentences = sent_tokenize(input_text)

    # Print sentences one by one
    for sentence in sentences:
        print(sentence)

if __name__ == "__main__":
    main()
