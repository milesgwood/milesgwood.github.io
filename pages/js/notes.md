---
layout: default
---

[Overview of the JS Development Space](https://medium.com/the-node-js-collection/modern-javascript-explained-for-dinosaurs-f695e9747b70)

1. npm - node package manager
2. module bundlers - Webpack
3. Transpilers - Babel

# Javascript 30 - 1 - Drum Kit

You can select elements using custom `data-` attributes. The following selects audio elements with a data-key attribute. Also note the ES6 syntax.

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
document.documentElement.style.setProperty('--blur', '20px');
```

# JS30-4 Array functions

The `filter` method allows you to write your own method to filter elements down to what you want in an array. You just return true for that element.

```js
const fifteen = inventors.filter((inventor) => {
  return inventor.year >= 1500 && inventor.year <= 1600;
});

console.table(fifteen);
```

For arrays you can display the output in console as a table. Use `console.table` instead of console.log.

The `map` method lets you iterate through the array and return an array of equal size after performing some action on each entry of data. It's like a machine that stamps all of the items. Filter lets you return less elements. Map isn't for that.

```js
fullNames = inventors.map((inventor) => `${inventor.first} ${inventor.last}`);
```

The `sort` function needs a comparator function that returns 1 for increasing the array index and -1 for decreasing the array index. It gives you two of the array elements for you to compare. Sort is an in place algorithm so it modifies the object you're working on.

```js
const ordered = inventors.sort((firstPerson, secondPerson) =>
  firstPerson.year > secondPerson.year ? 1 : -1
);
```

The `reduce` array function lets you iterate through all the elements and accumulate some value from them all.

```js
const totalYears = inventors.reduce((total, inventor) => {
  return total + (inventor.passed - inventor.year);
}, 0);
console.log(`Total Years Lived = ${totalYears}`);
```

Notice that the callback function takes in two parameters, an accumulator and the next object from the array. Reduce sometimes needs a default value to avoid an error. That's why that 0 exists after the callback function.

You can destructure arrays automatically putting them into variable names.

```js
const parts = fullName.split(', ');
const [last, first] = fullName.split(', ');
```

When accessing a object key value pair use `obj.key` when you have the actual string key. When you're using a variable that stores the key, you use obj[myVariableName].

```js
const people = { name: 'Steve', height: 100, weight: 500 };
console.log(people.name);

const people = { name: 'Steve', height: 100, weight: 500 };
const measurment = 'height';
console.log(people[measurment]);
```

# JS30-5

You can toggle classes on an element with the toggle function. Notice that I'm using `event.target` to access the element. You could also use `this.classList` since our eventListener is added to the panel element we want to add a class to.

```js
event.target.classList.toggle('open-active');
```

New on the CSS front, you can set the transition duration for a specific css attribute. The panel class takes 0.5s to do transforms like translateY(100%) because of this line `transition: transform 0.5s;`. You can set the transition properties for any css attribute you're changing (margin-right, height, width etc.) The changes occour when some event occours like hover or an attached event listener like onclick.

# JS30-6 Promises and Ajax Form List

The following fetches json data from an endpoint. The fetch funtion returns a promise which gets resolved as a stream of data. We then need to turn the returned data into JSON using the json function. Finally we take the JSON object and spread the data into our already declared citites array.

```js
const endpoint =
  'https://gist.githubusercontent.com/Miserlou/c5cd8364bf9b2420bb29/raw/2bf258763cdddd704f8ffd3ea9a3e81d25e2c6f6/cities.json';

const cities = [];
fetch(endpoint)
  .then((blob) => blob.json())
  .then((data) => cities.push(...data));
```

Regular expressions are used in the match function which determines if there is a match in the string. The `g` and `i` flags match globally in the string and search case insensitivley.

```js
const regex = new RegExp(wordToMatch, 'gi');
```

Using regex we can easily wrap certain sections in highlighting spans. Note the es6 syntax requires back ticks.

```js
const cityName = place.city.replace(regex, `<span class="hl">${this.value}</span>`);
```

# break vs continue

Break takes you out of your current loop. Continute just increases the iterator once.

# Console Log variable with name

You can log the variable with the name by adding the es6 {}.

```js
console.log({ allAdults });
```

# Array Methods - JS30-7

`array.some()` returns true if some of the elements pass a condition.
`array.every()` returns true if every element of the array passes a condition.
`array.find()` reuturns the object that matches the callback function criteria.
`array.findIndex()` returns the index so you can delete it or do something else with it
`array.splice(index, 1)` returns a new array with the 1 element removed

# Canvas - JS30-8

To get VS code reccomendations on elements, you need to add a `@type` comment declaration.

```js
/**
 * @type CanvasRenderingContext2D
 */
const ctx = canvas.getContext('2d');
```

# Console Methods - JS30-9

[MDN Reference on Console Methods](https://developer.mozilla.org/en-US/docs/Web/API/Console)

Most useful of them is `console.dir()` which displays an interactive list of the properties of the specified JavaScript object. Using `console.log()` only gives you the HTML element.

```js
const x = document.querySelector('p');
console.log('String');
console.info('Info');
console.warn('Warning');
console.error('Fuck!');
```

You can run tests through the console to check if your code breaks things.

```js
console.assert(1 === 2, "One doesn't Equal 2");
```

If you are logging a lot of messages, you can group them together. You just have to specify the same string for group and groupEnd. You can also have the data as collapsed by default with `console.groupCollapsed()`.

```js
const instrument = 'bass';

console.group('Primus');
console.log(`Lex Claypool plays ${instrument}`);
console.log(`Larry plays Guitar`);
console.log(`Jay plays Drums`);
console.groupEnd('Primus');
```

`console.table()` displays an Array as a nicely formatted table.

You can time how long things take to run using `console.time('Timer Name')` and `console.timeEnd('Timer Name')`.

Both the time and group functions require strings for names.

### Fun console logging

You can apply css styles to the console using `%c` at the front of the string.

```js
console.info('%c My cat is the best cat!', 'font-size: 30px; color: red;');
```

# Video Player - JS30-11

You can select elements by their data attributes that you set on them. This is useful for attaching event listeners to lots of elements that need similar functionality throughout the page.

```js
const skipButtons = document.querySelector('[data-skip]');
```

This checks if the mousedown flag is set to true and if it is then it runs scrub(). This is similar to bash scripting.

```js
progressBar.addEventListener('mousemove', mousedownFlag && scrub(e));
```

You can create full screen videos using css and teh request full screen function.

```js
function toggleFullscreen() {
  document.body.requestFullscreen();
  player.classList.toggle('fullscreen');
}
```

# JS30-13 Slide animation and Debounce

A debounce method improves performance by avoiding running a function but ever so often, for example waiting until a user stops typing to fetch typeahead search results.

```js
function debounce(func, wait = 20, immediate = true) {
  var timeout;
  return function () {
    var context = this,
      args = arguments;
    var later = function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}

const images = document.querySelectorAll('img');
// debounce returns a function that executes slideIn after a wait period
document.addEventListener('scroll', debounce(slideIn));

function slideIn(e) {
  const topOfPage = window.pageYOffset;
  const bottomOfPage = topOfPage + window.innerHeight;

  images.forEach((image) => {
    const imageTop = image.offsetTop;
    const imageHeight = image.height;
    const middleOfImage = imageTop + image.height / 2;
    if (bottomOfPage > middleOfImage) {
      image.classList.add('active');
    }
  });
  console.log(e);
}
```

# JS30 14 - Objects vs Arrays Reference vs Deep Copy

Strings nubers and booleans are replaced directly if you reassign them.

Arrays and objects are passed as a reference to the associated data structure. They are not deep copies. Notice if we change elements in our players2 array the changes are also reflected in the original players array.

```js
const players = ['Wes', 'Sarah', 'Ryan', 'Poppy'];
const players2 = players;
players2[1] = 'changed';
```

There is only one array in this situation above.

To make a deep copy of an array you must copy all the elements into a new array, not just copy a reference to an already existing array. There are numerous ways to do this. I prefer the es6 spread and the slice method. Concat has you create a new array and concatenate all the elements to the new empty array you made.

```js
const players = ['Wes', 'Sarah', 'Ryan', 'Poppy'];
const playersSliceCopy = players.slice();
const playersConcatCopy = [].concat(players);
const playersSpreadCopy = [...players];
```

Objects work similarly but only do a **shallow copy**! You only get one level deep within the object. If our person object contains

```js
const person = {
  name: 'Wes Bos',
  age: 80,
  socials: { facebook: 'wesbos', twitter: 'wesbos' },
};

const personCopy = Object.assign({}, person);
personCopy.name = 'Fucker'; //Only replaces the name in the copy
personCopy.socials.facebook = 'Changed In Both'; //Alters BOTH the original and the shallow copy since it is a nested object.
```

# JS30 -15 Local Storage andEvent Delegation

On a form you want to have an event listener attached to the `submit` event! Not click or anything else.

```js
myForm.addEventListener('submit', analyzeSubmission);

function analyzeSubmission(e) {
  e.preventDefault();
  //Prevents the page refreshing and you can do something else.
}
```

Labels and inputs are linked together using the attributes `for` and `id`.

```html
<input id="item${i}" type="checkbox" /> <label for="item${i}">${plate.text}</label>
```

Local Storage can store key value pairs of strings (not objects). There are three methods we'll commonly use. You can view the storage in the `Application tab`.

```js
localStorage.setItem('key', 'value');
localStorage.getItem('key');
localStorage.removeItem('key');
```

You have to `stringify` your objects and `parse` the JSON to get objects into and out of localstorage.

```js
localStorage.setItem('items', JSON.stringify(items));
JSON.parse(localStorage.getItem('items'));
```

When we initialize the page we need to check local storage to see if there is already data. We can take care of this where we declared our items array. This will either grap the local storage or create an empty array.

```js
const items = JSON.parse(localStorage.getItem('items')) || [];
```

We also need to populate our list with what we retreived in local storage so at the bottom of our script we add our populateList function.

```js
populateList(items, platesList);
```

# Event delegation

Event delegation. Since we are creating the child list items using javascript we can't add event listeners to the children on page load. What we can do is add an event listener to the parent and then check which of the new children triggered the event. This is why we added a `data-index` attribute in our map function so we could identify which child is responsible for the event.

```js
if (!e.target.matches('input')) return;
// We can use the matches function to check if the target is correct.
console.log(e.target.dataset.index);
```

## Chris Ferdinandi Event Delegation

[Explanation](https://gomakethings.com/why-event-delegation-is-a-better-way-to-listen-for-events-in-vanilla-js/)

Attaching an event listener to the document to listen for all events is actually performant and easier than attaching loads of other event listeners.

The `closest()` method works like the `matches()` method. But instead of checking to see if the element matches a selector, it also checks to see if any parent element does.

```js
// Listen to all click events on the document
document.addEventListener('click', function (event) {
  // If the clicked element does not have the .click-me class, ignore it
  if (!event.target.matches('.click-me')) return;

  // Otherwise, do something...
});
```

# JS-15 text Shadow and mousemove offsets

The `conetenteditable` attribute allows users to alter the text however they want.

```html
<h1 contenteditable>🔥WOAH!</h1>
```

Tracking mousemove events can be tricky. We have an event listener on the entire screen. There are so many x and y coordinates to choose from:

clientX : clientY
layerX : layerY
offsetX : offsetY
movementX : movementY
pageX : pageY
screenX : screenY
x : y

All I can tell is screen seems to include the entire screen including the top bar and bookmark bar. `offset` seems to give you the distance from the deepest HTMLelement in the tree. So if you have an event listener on the parent div the offset will become (0, 0) when you cross over the left corner of a child div.

`e.target` is the element that actually heard the event. So when going from the top of the page to the bottom we will increase our offsetY until we hit a child element. There our offsetY restarts at 0 so we must add `e.target.offsetTop` which is how far child element is from the top of the page. This makes this tutorial only useful if you're trying to animate something at the top of a page.

# JS-17 String Replace and Regular Expressions

We want to alphabetize an array while ignoring the article words like `An A And The`. The replace function can take in a regular expression `/^(a |the |an )/i`. This means it starts with any of those three words and is case insensitive. We are replacing any matches with an empty string and trimming off any extra spaces.

```js
function strip(bandName) {
  return bandName.replace(/^(a |the |an )/i, '').trim();
}

const alphaBands = bands.sort(function (a, b) {
  return strip(a) > strip(b) ? 1 : -1;
});
```

# JS-18 Reduce Map and destructuring

Here we're taking a timeString like "8:45" and destructuring it into a min and seconds variable.

```js
const [mins, secs] = timeString.split(':').map(parseFloat);
```

Note that strings are white text in console and numbers are purple. This is due to my dark theme. On any other machine strings are black and numbers are still purple.

Call `Array.from(NodeList)` on a NodeList to turn it into an array that you can use map and reduce functions on.

Trickiest part of all of this was needing to pass an initial value of 0 to my reduce function otherwise it would concatenate strings.

[MDN Notes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/Reduce)

Array.reduce(callbackfn(accumulator, currentArrayThing, index), `initialVal`)

I also found that by writing cleaner code, my implementation actually ran faster.

```js
const videoSeconds = Array.from(document.querySelectorAll('[data-time]'))
  .map((node) => node.dataset.time)
  .map((timeString) => timeString.split(':').map(parseFloat))
  .reduce((total, minSecArr) => total + minSecArr[0] * 60 + minSecArr[1], 0);
```

This above code ran faster than this below.

```js
const videoSeconds2 = Array.from(document.querySelectorAll('[data-time]')).reduce((total, node) => {
  const [mins, secs] = node.dataset.time.split(':').map(parseFloat);
  return total + mins * 60 + secs;
}, 0);
```

# JS-19 Webcam and NPM basics

Through either npm or your VS Code server, you are able to view the site you're working on through your local network as well. Navigate to [192.168.86.43:5500](192.168.86.43:5500) on your phone and you'll see a live phone version.

## Start a NPM server

Here is the basic `package.json` file with a `start` command included.

```json
{
  "name": "gum",
  "version": "1.0.0",
  "description": "NPM Server for JS30 Webcam Demo including browser-sync",
  "main": "scripts.js",
  "scripts": {
    "start": "browser-sync start --server --files \"*.css, *.html, *.js\""
  },
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "browser-sync": "^2.12.5 <2.23.2"
  }
}
```

I have npm installed on both the Windows Machine as well as the linux subsystem on windows. Since we're just starting a local server from the command line I'll use WSL for this.

### Update node on WSL

My node version is `v12.7.0` and I want to update to the Latest Long Term Support version of node which is `v14.15.0`. I found this information by running `nvm ls-remote`. Now I want to actaully install teh version with `nvm install 14.15.0`. I also wanted to clear up some disk space so I ran `nvm uninstall 12.7.0`.

### Update npm on WSL

First I updated npm with `npm install -g npm` which got me to version `6.14.8`. Then I ran `npm install` to install the browser-sync dependency listed in the package.json.

List all of your globally installed packages vs your project specific packages with the -g variable.

```
npm list -g --depth=0
npm list --depth=0

/home/milesgwood/.nvm/versions/node/v14.15.0/lib
└── npm@6.14.8

gum@1.0.0 /mnt/w/JavaScript30/19 - Webcam Fun
└── browser-sync@2.26.13
```

Now I can finally run `npm start` and the local server will run.

We're updating the canvas context every so often using the `setTimeout` fucntion. setTimeout is similar to `setInterval` function except the timeout only waits once. Interval is for if you want to run something over and over.

Creating new document elements in two syntaxes

```js
const img = document.createElement('img');
img.src = imageData;
img.alt = 'Fucking Alts';
link.appendChild(img);

vs.

const link = document.createElement('a');
link.innerHTML = `<img src="${imageData}"></img>`;
```

Then you can append or add the element either to the start or end of the parent element.

```js
//Adds photo to the end of the parent's Element List
parentElement.appendChild(link);

// Adds the photo to the front of the strip
parentElement.insertBefore(link, strip.firstChild);
```

# Chrome Dev Tools and Console Tips

Chrome console has a command pallette just like VS Code. `Cmd + Shift + P` shows the command pallette where you can switch between different tabs. They demonstrated how you can open up the media loading timeline by searching form media. It tells you the resolution as well.

You can access an elements properties directly in the Elements pane. Just select Properites instead of Styles.

# JS-20 Speech Recognition

You can list sections as `contenteditable` and that allows the user to type to change the text. The [speech reconition API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition) lists the constructor, properties, methods, events, and examples.

# JS-21 Compass and Geolocation

The vscode server works better than the server that npm install sets up. I'm able to access my webapps on my phone more easily. If you wan to develop for mobile webapps, it's best to do so on a mac. You get access to xcode and geolocation data. You can simulate a phone as well. Not sure if there is an equivalent for android but iPhone users spend more.

# JS-22 Follow Along Link Highlighting

The difference between `append` and `appendChild` is as follows:

ParentNode.append() has **no return** value, whereas Node.appendChild() **returns the appended** Node object.
ParentNode.append() **can append several** nodes and strings, whereas Node.appendChild() can only append **one node**.

## Keyboard notes

`Shift Alt Arrow` selects the whole word you are presently in. `Shift Ctrl Aarow` selects the rest of the word from where your cursor is.
`Shift Alt Down` Copies the line you're on.

# JS - 23 Speech Senthesis

`querySelectorAll` can select inputs using multiple attributes. It just needs to be a valid css string. Note that we are selecting two inputs and one textarea. They are **different HTML elements** being selecting using their attributes.

```js

<input name="rate" type="range" min="0" max="3" value="1" step="0.1" />
<input name="pitch" type="range" min="0" max="2" step="0.1" />
<textarea name="text">Hello! I love JavaScript 👍</textarea>

const options = document.querySelectorAll('[type="range"], [name="text"]');
```

Setting an attribute on a variable when the attribute name is a string variable require `[]`.

Normally you would set an attribute like so:

```js
msg.text = 'Hi Steve';
```

If you have a variable attribute you're trying to change the `.` can't be used.

```js
options.forEach((option) => option.addEventListener('change', setOption));

function setOption() {
  console.log(this.name, this.value);
  //We set the name of the inputs to match the name of the attributes on our SpeechSythesisUtterance object called msg
  msg[this.name] = this.value;
}
```

This makes event listeners much better as we can use the attributes on the actual HTML input element. You should create your inputs based on the API that you're working with.

## How to pass a variable to an event listener

You **can't** do the following as it will run the toggle function on page load. So how do we pass in variables?

```js
stopButton.addEventListener('click', toggle(false));
```

Option 1 - use a global variable

Option 2 - create an anonymous function which calls our toggle function and pass the variable in.

```js
stopButton.addEventListener('click', () => toggle(false));

OR;

stopButton.addEventListener('click', function () {
  toggle(false);
});
```

Option 3 - [Use Bind](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind)

The `bind()` method creates a new function that, when called, has its this keyword set to the provided value, with a given sequence of arguments preceding any provided when the new function is called.

So you pass bind the context or "this" to run the function in (in this case we don't care about the context so we pass null).
You follow the context with the list of arguments.

```js
stopButton.addEventListener('click', toggle.bind(null, false));
```

# JS30 - 24 fixed nav on scroll

A `fixed` element doesn't take up any space on the page. It floats on top of the browser. So we must add padding to the body to offset the newly fixed nav.

```css
body.fixed-nav nav {
  position: fixed;
  box-shadow: 0 5px 0 rgba(0, 0, 0, 0.1);
}
```

Here's the actual js that adds the css classes and sets the padding programatically.

```js
function fixNav() {
  if (scrollY >= topOfNav) {
    document.body.classList.add('fixed-nav');
    document.body.style.paddingTop = nav.offsetHeight + 'px';
  } else {
    document.body.classList.remove('fixed-nav');
    document.body.style.paddingTop = '0px';
  }
}
```

You can't animate a width from anything to auto. You must use a px value.

# JS30 - 25 Propagation Bubbling and Once - Event Listeners

When an event listener fires, it first traverses down the HTML tree capturing all of the elements that contain the clicked element. If div 3 is clicked then all all of the following will capture that click. html > body > div 1 > div 2 > div 3. Pro

If you add event listeners to all of the divs you the innermost div will fire it's event off first. Then we `bubble` up the tree. The event bubbles up from the most nested element.

We can manipulate this behavior with the options object parameter of [addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)

```js
target.addEventListener(type, listener [, options]);

div.addEventListener('click', purchaseButton, {
  capture: true,
  once: ture,
})
```

`Capture` causes the event listener to fire on the way down the HTML tree rather than while we are bubbling up. So the outermost containing element will fire it's event listener first.

`Once` unbinds the event listener after it is fired once. This is useful for purchase buttons in internet shopping.

You're also able to stop the event listener calls from propegating forward using `e.stopPropagation();`.

To recap, you can either use very specific onclick events with specific event listeners OR you can utilize capture and once to filter which elements actually get to run the event listeners.

# JS30- 26 Follow Along Hover Nav

When you pass a funtion to setTimeout or a similar timing function, the context (`this`) will change. In this function we are handling an event and adding a class to the element that triggered the event. If you use an aarow function, you inherit the context (`this`) of the parent function.

```js
function handleEvent() {
  this.classList.add('trigger-enter');
  setTimeout(funciton(){
      this.classList.add('trigger-enter-active')
  }, 150);
}

function handleEvent(){
  this.classList.add('trigger-enter');
  setTimeout(() => this.classList.add('trigger-enter-active'), 150);
}

//With an aarow function settimeout inherits the context of the parent //
```

To get the position of our opacity 0 dropdowns we use [getBoundingClientRect()](https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect) which returns a DomRect object. This tells us how far from the left and top of the viewport our element is. Remember, the viewport is the visible part of the screen so the values will change as you scroll. You can add `window.scrollX` and `window.scrollY` to get a bounding rectangle that is independent from the current scrolling position.

```js
bottom: 379.09375;
height: 232;
left: 821.453125;
right: 992.625;
top: 147.09375;
width: 171.171875;
x: 821.453125;
y: 147.09375;
```

# JS30 - 27 slider move left

Use the four mouse events to track the current position of the cursor and move the slider appropriatley. The four events we track are `mousedown`(set initial conditions of interaction), `mouseup` (stop), `mouseleave`(stop), and `mousemove` (perform the actual work).

# JS30 - 28 Video Speed Slider

In lesson 25 I learned that an aarow function preserves the context of the parent. This is true everywhere. That means if you use an aarow function as your event listener function then you get the context of the window, rather than the HTML element that the listener is attached to.

```js
video.addEventListener('mousemove', () => {
  console.log(this);
});

video.addEventListener('mousemove', function (e) {
  console.log(this);
});
```

Aarow function gets the window as this. The proper function gets the video element as this.

## Scroll Height vs clientHeight vs offsetHeight

**scrollHeight:** The scrollHeight value is equal to the minimum height the element would require in order to fit all the content in the viewport without using a vertical scrollbar.
`ENTIRE content & padding (visible or not)`

**clientHeight**: it includes the element’s padding, but not its border, margin or horizontal scrollbar (if present). It can also include the height of pseudo-elements such as ::before or ::after. If the element's content can fit without a need for vertical scrollbar, its scrollHeight is equal toclientHeight.
`VISIBLE content & padding`

**offsetHeight**: is a measurement in pixels of the element’s CSS height, including border, padding and the element’s horizontal scrollbar (if present, if rendered). It does not include the height of pseudo-elements such as ::before or ::after.

The following equivalence returns `true` if an element is at the end of its scroll, `false` if it isn't.

```
element.scrollHeight - element.scrollTop === element.clientHeight
```

If you surroud your console.log({var}) in brackets you'll see the variable name as well in the console.

To convert a percent to a range of values use

```js
rate const = percent * (max - min) + min;
```

50% on a scale of 20 to 120 = 0.5 \* (120 - 20) + 20 = 70

Note that 70 is indeed halfway between 20 and 120.

# JS30-29 Countdown timer

The Date object gives you the milliseconds elapsed since Jan 1 1970. You can get the current time as a timestamp and turn timestamps into text expressions of the date.

```js
const now = Date.now(); //get the current time using a new static method on Date
const nowAgain = new Date(now); //turn a timestamp back into a date object
```

You can alter the title of the document and the tab title.

```js
document.title = `4:22`; //Set the title of the page and the text in the tab
```

Forms can be selected directly using the `document` object and the `name` of the form.

```html
<form name="customForm" id="custom">
  <input type="text" name="minutes" placeholder="Enter Minutes" />
</form>
```

```js
const form = document.customForm;
const minutes = document.customForm.minutes.value;
```

# JS30-30 - Whack a Mole

Mouse Events have an isTrusted variable that let's you know if they triggered the event with javascript or if they actually clicked it.

This formula gives a nice round integer between a min and max value:

```js
function randomTime(min, max) {
    return Math.round(Math.random() * (max - min) + min);
}
```

`setTimeout(()=>{}, duration)` runs once while `setInterval` runs repeatedly. 