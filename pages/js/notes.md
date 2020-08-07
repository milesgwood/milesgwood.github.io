---
layout: default
---

# Javascript 30 - 1 - Drum Kit

You can select on custom data- attributes using a css like query selector. The following selects items based on a variable based off of the event based variable.

<audio data-key="65" src="sounds/clap.wav"></audio>
document.querySelector(`audio[data-key="${e.keyCode}"]`);


# What's the difference between const let and var

[Read Me](https://medium.com/javascript-scene/javascript-es6-var-let-or-const-ba58b8dcde75)

const does't let you change your variable

