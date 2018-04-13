from __future__ import unicode_literals
import youtube_dl, sys, pyperclip, threading

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
