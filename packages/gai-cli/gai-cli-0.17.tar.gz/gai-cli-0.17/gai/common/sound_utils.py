import subprocess

def play_audio(response):
    ffplay_cmd = ["ffplay", "-nodisp", "-autoexit", "-"]
    ffplay_proc = subprocess.Popen(ffplay_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    for chunk in response.raw.stream(1024, decode_content=False):
        if chunk:
            ffplay_proc.stdin.write(chunk)

    # close on finish
    ffplay_proc.stdin.close()
    ffplay_proc.wait()