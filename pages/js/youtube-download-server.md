---
layout: default
---

I started using python as my server but decided that using a node server would be easier. I can execute the python script from javascript.

## Windows CMD Setup

Make sure you're running the script using the Command Prompt as your default terminal. You can right click the server file and select `Run Python File in Terminal`.

CMD on Windows Command Prompt

```
python --version
Python 3.8.6

pip --version
pip 20.2.1 from c:\python38\lib\site-packages\pip (python 3.8)
```

Python is on the PATH - `PATH=C:\Python38\Scripts\;C:\Python38\`

Run the following to make sure the needed modules are installed.

```cmd
python -m ensurepip
pip install youtube_dl pyperclip libmagic eyeD3
pip install -U youtube-dl
pip install python-magic-bin==0.4.14
```

[Install FFmpeg windows](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg)
Add ffmpeg to path `C:\Program Files\ffmpeg-20180412-8d381b5-win64-static\bin`

## Run a local Python server - FAILED OPTION

```python
import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
```

At this point an index.html file should be served if you visit [http://localhost:8000/](http://localhost:8000/) through the correct port.

I can't specify what I want the server to do with a Get request of the route download so I'm switching back to javascript.

# Primary Tutorials

[How I made my own YouTube Downloader using JavaScript and Node.js](https://blog.usejournal.com/how-i-made-my-own-youtube-downloader-using-javascript-and-node-js-160b172f6e10)

This was useful for learning how to pass a value from the client side to the server using either the URL or a fetch.

```js
function sendURL(URL) {
  fetch(`http://localhost:4000/download?URL=${URL}`, {
    method: 'GET',
  })
    .then((res) => res.json())
    .then((json) => console.log(json));
}

function sendURL(URL) {
  window.location.href = `http://localhost:4000/download?URL=${URL}`;
}
```

[How to Run a Python File From Node](https://medium.com/swlh/run-python-script-from-node-js-and-send-data-to-browser-15677fcf199f)

This allows me to run the python script successfully.

The server is working with a URL input. Now I need to create an anonymous function that calls itself to download with one click.

```js
javascript: (function download() {
  let URL = window.location.href;
  fetch(`http://localhost:4000/download-mp3?URL=${window.location.href}`, { method: 'GET' })
    .then((res) => res.json())
    .then((json) => console.log(json));
})();
```
