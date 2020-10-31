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
