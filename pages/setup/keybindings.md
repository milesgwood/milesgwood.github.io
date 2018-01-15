---
layout: default
---

So I need to generate the sliders quickly and I don't want to manually type them out. So I am making a python tool to do it for me.

Python is version 2.7. I also installed atom-beautify to to make it easy to auto format the output HTML string. You have to open the Atom Command Pallette with `Cntrl+Shift+P` and then type beautify.

I will se the HTML language to beautify on save. [You can see how to here on the packages page.](https://atom.io/packages/atom-beautify#usage)

Using Atom I also created a new keybinding using the expand-selection-to-quotes package. It makes `alt-q` into a entire quote selector. So if you need to replace a Quote or a url you can easily select the entire string and delete it. I had to create the keybinding in the Settings where you can open the .cson file.
```
'atom-workspace atom-text-editor:not([mini])':
  "alt-q": 'expand-selection-to-quotes:toggle'

'.platform-darwin atom-workspace atom-text-editor:not([mini])':
  'alt-q': 'expand-selection-to-quotes:toggle'

'atom-workspace atom-text-editor':
  'alt-q': 'expand-selection-to-quotes:toggle'
```
