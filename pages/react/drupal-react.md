---
layout: default
---

[Tutorial on including react](https://drupalize.me/tutorial/connect-react-drupal-theme?p=3253)

- Create a custom block.
- Create a new template file named to override the block display. `block--profileslider.html.twig` from `bootstrap/template/block/block.html.twig`
- Attach the react library to the template.

```
{{ attach_library('coopercenter_units/react') }}
{{ attach_library('coopercenter_units/react-app') }}

<div id="react-app">
```
- Insert a react component, like above, with an appropriate id like "react-app". This id matches the index.js file.
- Add the following to the `theme.libraries.yaml` file. Note that your react index.js file is listed so it can load.

```
react:
  version: 1.x
  header: true
  js:
    https://unpkg.com/react@16/umd/react.production.min.js: { external: true, minified: true }
    https://unpkg.com/react-dom@16/umd/react-dom.production.min.js: { external: true, minified: true }
    https://unpkg.com/babel-standalone@6.15.0/babel.min.js: { external: true, minified: true }
react-app:
  version: 1.0.0
  footer: true
  js:
    js/react/index.js: { preprocess: 0, attributes: { type: text/babel } }
```

-
