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

# JS30-4 Array functions

The `filter` method allows you to write your own method to filter elements down to what you want in an array. You just return true for that element.

```js
const fifteen = inventors.filter(inventor => {
    return (inventor.year >= 1500 && inventor.year <= 1600);
});

console.table(fifteen);
```

For arrays you can display the output in console as a table. Use `console.table` instead of console.log.

The `map` method lets you iterate through the array and return an array of equal size after performing some action on each entry of data. It's like a machine that stamps all of the items. Filter lets you return less elements. Map isn't for that.

```js
fullNames = inventors.map(inventor => `${inventor.first} ${inventor.last}`);
```

The `sort` function needs a comparator function that returns 1 for increasing the array index and -1 for decreasing the array index. It gives you two of the array elements for you to compare. Sort is an in place algorithm so it modifies the object you're working on.

```js
 const ordered = inventors.sort((firstPerson, secondPerson) => firstPerson.year > secondPerson.year ? 1 : -1)
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
const parts = fullName.split(", ");
const [last, first] = fullName.split(", ");
```

When accessing a object key value pair use `obj.key` when you have the actual string key. When you're using a variable that stores the key, you use obj[myVariableName]. 

```js
const people = {name: 'Steve', height: 100, weight: 500};
console.log(people.name);

const people = {name: 'Steve', height: 100, weight: 500};
const measurment = 'height';
console.log(people[measurment]);
``` 