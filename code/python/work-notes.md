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


## Write Music tags

So I want to move the Title into the correct tag for all files I download with the youtube script.

[Python Magic](https://github.com/ahupp/python-magic#dependencies) identifies the file types.

It is looking for the file here `C:\Users\miles\AppData\Local\Programs\Python\Python36\lib\site-packages\magic.py`

[Had to download another file](https://stackoverflow.com/questions/18374103/exception-valuefailed-to-find-libmagic-check-your-installation-in-windows-7) and run `pip install pip install python_magic_bin-0.4.14-py2.py3-none-win_amd64.whl` Downloaded that file from [here.](https://pypi.python.org/pypi/python-magic-bin/0.4.14)

To pass strings filenames you need to put a [r in front of the string so it gets read as a raw string](https://stackoverflow.com/questions/37400974/unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3-trunca?rq=1)
```
mp3 = r"C:\Users\miles\Dropbox\New Music\00-20CTa043IA.mp3"
```

Read up on Python lambda Expressions. What are they good for?

http://www.secnetix.de/olli/Python/lambda_functions.hawk

```
>>> foo = [2, 18, 9, 22, 17, 24, 8, 12, 27]
>>>
>>> print filter(lambda x: x % 3 == 0, foo)
[18, 9, 24, 12, 27]
>>>
>>> print map(lambda x: x * 2 + 10, foo)
[14, 46, 28, 54, 44, 58, 26, 34, 64]
>>>
>>> print reduce(lambda x, y: x + y, foo)
139
```

Also have list comprehensions.

```
mylist = [x*x for x in range(3)]
```

I had a lot of trouble with newlines getting in the way.
```
print(mysterytext.encode('UTF-8'))
```

Check if directory exists
```
import os
print(os.path.isdir("/home/el"))

To get the path this file is in use This
dir_path = os.path.dirname(os.path.realpath(__file__))
```
