---
layout: default
---

## Python Projects

### Youtube Download Tool

 I want to make a tool to easily download Youtube videos. There is already a youtube_dl package that I installed for the 2.7 version of python. [It required a FFmpeg program](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg) and I'm not clear if installing it for the Linux subsystem allows Windows to see the program too. [This question](https://superuser.com/questions/1146303/how-to-add-a-windows-path-to-the-windows-ubuntu-subsystem-path) seems to suggest that you have to login and pass the Windows path to the Linux subsystem. I'm testing it now by installing FFMpeg for Linux. If it works for both windows and linux then it is working for both.

 The windows and linux shells do not share programs or data. I got the youtube_dl package to work with Python2.7. The package isn't even installed for python2 on windows or python3 in linux. It only works through a hyper invocation using Python 2.

I want this tool to automatically copy what is in my keyboard and download it if it is from youtube.

To use the windows clipboard, I need to have the script run on my windows machine. This is where I would be a lot happier to have all of this working in Windows nativley or linux nativley.

So for the windows setup I need to...

1. Use Python 36 from CMD using python command or F5 in Atom
2. `pip install youtube_dl`
3. `pip install pyperclip`
4. [Install FFmpeg windows](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg)
5. Add ffmpeg to path `C:\Program Files\ffmpeg-20180412-8d381b5-win64-static\bin`


The python scripts that are actually being used on windows are here `C:\Users\miles\AppData\Local\Programs\Python\Python36\Scripts\`. All the rest of them are not being used by windows as far as I can tell.

I should probably uninstall the other versions to avoid this confusion.

It only works if launched from within Atom using the F5 key. Anytime I launch it by clicking on it, it exits prematurely.


There is definitely a way to launch the python script and not have it fail like it does. Here is the console output from atom.
```
f5 pressed
C:\Users\miles\.atom\packages\atom-python-run\lib\terminal.js:216 platform: win32
shell: C:\WINDOWS\system32\cmd.exe
option: /c,start
call: python
script: C:\Users\miles\.atom\packages\atom-python-run\lib\..\cp\main.py
command: tell app "Terminal" to do script " python C:\Users\miles\Dropbox\New Music\youtube-download.py"
C:\Users\miles\.atom\packages\atom-python-run\lib\terminal.js:227 pause: true
pipeFile: false
pipePath:
log: true
args: python,C:\Users\miles\Dropbox\New Music\youtube-download.py
options: {
    "cwd": "C:\\Users\\miles\\Dropbox\\New Music",
    "detached": true
}
```
I can see that some javascript file is running some main.py python script and then running my script from that python process. It detaches the process and it runs successfully.
