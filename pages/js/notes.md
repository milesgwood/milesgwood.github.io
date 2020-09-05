---
layout: default
---

# Javascript 30 - 1 - Drum Kit

You can select on custom data- attributes using a css like query selector. The following selects items based on a variable based off of the event based variable.

<audio data-key="65" src="sounds/clap.wav"></audio>
document.querySelector(`audio[data-key="${e.keyCode}"]`);


# What's the difference between const let and var

[Read Me](https://medium.com/javascript-scene/javascript-es6-var-let-or-const-ba58b8dcde75)

const does't let you change your variable.

# Altering CSS in dev tools

You can increment a value by highlighting it and using the aarow keys. Shift makes larger jumps. For example increasing the degrees of rotation on a transform. You can increment by 10 degrees by highlighting the degree value and shift + aarow keys.

# CSS Variables - Javascript30-3

You can declare CSS variables by attaching them to the root node and giving them the prefix `--`.

```css
   :root {
      --base: #ffc600;
      --spacing: 10px;
      --blur: 10px;
    }
```

Then you can use the variables with the var() css function.

```css
    img {
        padding: var(--spacing);
    }
```

You can update the variable's value through a form control using javascript. You have to update the documentElement like so

```js
document.documentElement.style.setProperty("--blur", "20px");
```

