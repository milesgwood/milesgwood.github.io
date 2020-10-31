---
layout: default
---

# Bookmarklet that makes ` favorite current song

```js
javascript: (function listenForFave() {
  document.addEventListener('keydown', (event) => {
    if (event.keyCode === 192) {
      document.querySelector('.control-button-heart button').click();
    }
  });
})();
```

# Click the play button if an Advert has stopped play

First we need to see if we are playing an advert. The Aria Label actually tells us if it is an ad.

```js
let now = document.querySelector('.now-playing');
let song = now.ariaLabel;
let isAdvert = now.ariaLabel.includes('Advert');
```

Next we need to grab the play button so we can click it. Here is the button HTML

```html
<button
  class="control-button spoticon-pause-16 control-button--circled"
  data-testid="control-button-pause"
  title="Pause"
></button>
```

We want to click the button if we are paused on an advert.

```js
let unPause = document.querySelector('button[title="Pause"]');
unPause.click();
```

Now we need to run this function every time there is a change in song. However I can't seem to find an event listener that triggers when I change the song. I can just run my code all the time instead of listening for a specific event.

All we have to do to make it a bookmarklet is add `javascript: ` and remove the line breaks.

```js
javascript: console.log('No Pause Injected');
let unPause = document.querySelector('button[title="Pause"]');
let now = document.querySelector('.now-playing');
let song = now.ariaLabel;
function checkForSongChange() {
  if (song == now.ariaLabel) {
    return;
  } else {
    console.log('Checking if Song is Advert');
    let isAdvert = now.ariaLabel.includes('Advert');
    if (isAdvert) {
      console.log("It's An Ad!");
      document.querySelector('button[title="Pause"]').click();
    }
    song = now.ariaLabel;
  }
}
setInterval(checkForSongChange, 300);
```
