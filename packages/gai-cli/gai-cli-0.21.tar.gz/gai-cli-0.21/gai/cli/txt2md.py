from markdownify import markdownify as md
import sys

def main():
    for line in sys.stdin:
        md_line = md(line)
        print(md_line)

if __name__ == "__main__":
    main()
