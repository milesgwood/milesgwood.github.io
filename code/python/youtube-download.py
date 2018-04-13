from __future__ import unicode_literals
import youtube_dl, sys, pyperclip, threading

# 1. Use Python 36 from CMD using python command or F5 in Atom
# 2. `pip install youtube_dl`
# 3. `pip install pyperclip`
# 4. [Install FFmpeg windows](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg)
# 5. Add ffmpeg to path `C:\Program Files\ffmpeg-20180412-8d381b5-win64-static\bin`

# Getting this working on Mac Machines
# You'll may need to upgrade TLS to v1.2 - best to just use python3 https://news.ycombinator.com/item?id=13539034
# 1. Install HomeBrew ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# 2. brew install youtube-dl
# 3. pip3.6 install youtube-dl
# 4. pip3.6 install pyperclip
# 5. brew install ffmpeg

def get_all_command_line_ars():
    if len(sys.argv) > 1:
        # Get address from command line.
        url = ' '.join(sys.argv[1:])
    else:
        # Get address from clipboard.
        url = pyperclip.paste()
        print("URL from the clipboard: " + url)

def check_clipboard_for_youtube_url():
    url = pyperclip.paste()
    if "https://www.youtube.com" in url:
        if url not in mp3_downloaded_already:
            download_audio(url)
    print("Checking for youtube link...")
    threading.Timer(2.0, check_clipboard_for_youtube_url).start()

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    mp3_downloaded_already.append(url)
    print("Already downloaded these videos: ")
    print(mp3_downloaded_already)

mp3_downloaded_already = []
check_clipboard_for_youtube_url()
