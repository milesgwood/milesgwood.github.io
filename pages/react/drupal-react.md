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

# Testing React App on BeHeardCVA

- Created an empty custom block called `Community Photo Gallery` and set the block to only show on the page `/gallery`
- Created a new template file called `block--communityphotogallery.html.twig` from `bootstrap/template/block/block.html.twig`
- Included these lines in the block twig file

```
{{ attach_library('beheardcva/react') }}
{{ attach_library('beheardcva/gallery-app') }}

<div id="root"></div>
```

- Create `themes/beheardcva/js/react/gallery-index.js`. This is where the code will go. To start testing it out include the hello world script.
```
ReactDOM.render(
    <h1>Hello, world!</h1>,
    document.getElementById('root')
);

```
- Add react library to `beheardcva.libraries.yml`

```
react:
  version: 1.x
  header: true
  js:
    https://unpkg.com/react@16/umd/react.production.min.js: { external: true, minified: true }
    https://unpkg.com/react-dom@16/umd/react-dom.production.min.js: { external: true, minified: true }
    https://unpkg.com/babel-standalone@6.15.0/babel.min.js: { external: true, minified: true }
gallery-app:
  version: 1.0.0
  footer: true
  js:
    js/react/gallery-index.js: { preprocess: 0, attributes: { type: text/babel } }
```

# Deployment - Webpack and Babel

[Tutorial](https://www.robinwieruch.de/minimal-react-webpack-babel-setup/)

[Another Babel Webpack tutorial](https://www.valentinog.com/blog/babel/)

So develpment is easy with the `create react app` command. However deployment requires you to transpile the code with `babel` and join the files with `webpack`.

To get this to work you need to run the following and then edit the package.json file to change the build command to the webpack command.

```
npm install --save react react-dom
npm install -g babel babel-cli babel-preset-react
npm install --save-dev @babel/preset-react
npm install --save-dev css-loader

Edit the package.json so that the build line is "build": "webpack --mode production"

npm run build
yes
```

This next line is optional to run as it will ask to install this if you run `npm run build` with the modified command `"build": "webpack --mode production"` in the package.json file.

```
npm install --save-dev webpack webpack-dev-server webpack-cli
```

Define `.babelrc` at project root level, with following content. Currently working version.

```
 {
   "presets": [
     "@babel/preset-env",
     "@babel/preset-react"
   ]
 }
 ```

Edit the scripts section in `package.json` so that we still have the start command but now we also have the build command with `webpack --mode production`
```
{
  "name": "beheard-photos",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "babel": "^6.23.0",
    "babel-cli": "^6.26.0",
    "babel-preset-react": "^6.24.1",
    "bootstrap": "^4.3.1",
    "react": "^16.8.6",
    "react-dom": "^16.8.6",
    "react-scripts": "3.0.1"
  },
  "scripts": {
    "wpstart": "webpack-dev-server --config ./webpack.config.js --mode development",
    "oldreactstart": "react-scripts start",
    "start": "react-scripts start",
    "oldreactbuild": "react-scripts build",
    "build": "webpack --mode production",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": "react-app"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "devDependencies": {
    "@babel/preset-react": "^7.0.0",
    "css-loader": "^3.1.0",
    "webpack": "^4.36.1",
    "webpack-cli": "^3.3.6",
    "webpack-dev-server": "^3.7.2"
  }
}
```

Create the webpack configuration called `webpack.config.js` in the root and add the following:
```
module.exports = {
  entry: './src/index.js',
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  output: {
    path: __dirname + '/dist',
    publicPath: '/',
    filename: 'bundle.js'
  },
  devServer: {
    contentBase: './dist'
  }
};
```

Now we are setup to transpile our code into useable javascript by running `npm run build`. Note that this is not the build command from the original react app. We changed it so that babel and webpack are building the `bundle.js` file which we will copy into the live drupal site.  

## CSS loader for webpack

The only issue remaining is the css will not work in this configuration. We need to tell webpack how to inline the css. Unfortunately creating this webpack builder has broken the react server. I will need to have two servers running. One for development and this webpack compiling version for deployment. We need a `css loader for webpack and react`.

```
npm install --save-dev css-loader
```

Now you just need to tell webpack to include the css in the build by adding the follwing to `webpack.config.js`

```
rules: [
  {
    test: /\.(js|jsx)$/,
    exclude: /node_modules/,
    use: ['babel-loader']
  },
  {
    test: /\.css$/i,
    use: ['style-loader', 'css-loader'],
  },
]
```


## Copying - Failed
Simply copying the fails because jsx is not supported natively by browsers. Copying the files directly from atom will result in an error `require not defined`

## Babel Tranpilation - Failed

Babel gets us half way there but only translates the jsx into javascript. We still need to join the files

- Install `npm install -g babel babel-cli babel-preset-react`
- Define .babelrc at project root level, with following content
```
{
  "presets": ["react"],
 }
 ```
- `babel {jsxFile}.jsx --out-file {jsFile}.js`

## npm run build - Fails

`npm run build` offers a way to build your site but only works if it is the only thing on the site. It doesn't work for embedded drupal react components as it builds it as if it is a stand alone site.


# JSON API

Install the JSON API Module and get your content type name. The request we'll be making is `https://beheardcvadev1.coopercenter.org/jsonapi/node/gallery_image`. Note the end of the request is `/jsonapi/node/gallery_image` we'll be using that to request our assets in react.

This longer form of the request gets the URL to the photo included as well.

```
https://beheardcvadev1.coopercenter.org/jsonapi/node/gallery_image?include=field_gallery_photo
/jsonapi/node/gallery_image?include=field_gallery_photo

You can add this to end to sort by date created.

&sort=-created
```

The request is getting blocked by the browser since I am requesting assets from beheardcva.org from my local machine of localhost. To get around this issue simply run chrome without the security checks

```
cmd+R
chrome.exe --user-data-dir="C://Chrome dev session" --disable-web-security
```

Make sure to delete C:/Chrome dev session after every launch as it won't work a second time.

We get our data in a JSON object. The data and included arrays within that object are what we want. The data array stores all the titles and the included array stores all the photo URLs.

We access elements of a JSON object with a `.` so responseData.data would get us the data array. We'll want to use map to iterate through that array.

When not iterating you can access an array index directly with array brackets. So you access objects elements with a `.` and array indexes with an index. Here we have a responseData object with an array called data, the first element of which is an object with an attributes object within it that contains a title string within that attributes object.

```
responseData.data[0].attributes.title
```

Render function without JSON

```js
render() {
  return(
    <div refs='gallery-container' className='container-fluid gallery-container'>
      <div className='row'>
        {
          this.props.imgUrls.map((url, index) => {
             return <div className='col-md-4 col-xl-3'>
                <div className='gallery-card'>
                  <GalleryImage className='gallery-thumbnail' src={url} alt={'Image number ' + (index + 1)} />

                  <span className='card-icon-open glyphicon glyphicon-fullscreen' value={url} onClick={(e) => this.openModal(url, e)}></span>
                </div>
              </div>
           })
         }
      </div>
       <GalleryModal isOpen={this.state.showModal} onClick={this.closeModal} src={this.state.url} />
    </div>
    )
  }
```

Render function with JSON.

Note that we are accessing the included and data arrays which were received through the JSON api call.

```js
render() {
  return(
    <div refs='gallery-container' className='container-fluid gallery-container'>

      <div className='row'>
        {
          this.state.included.map((image, index) => {
             return <div key={index} className='col-xs-12 col-sm-6 col-md-4 col-xl-3'>
                <div className='gallery-card'>
                  <GalleryImage key={index}image className='gallery-thumbnail' src={this.state.root + image.attributes.uri.url} alt={'Image number ' + (index + 1)} />

                  <span className='card-icon-open glyphicon glyphicon-fullscreen' value={image.attributes.uri.url} onClick={(e) => this.openModal(this.state.root + image.attributes.uri.url, this.state.data[index].attributes.title, e)}></span>
                </div>
              </div>
           })
         }
      </div>

       <GalleryModal key="modal" isOpen={this.state.showModal} onClick={this.closeModal} src={this.state.url} caption={this.state.caption} />
    </div>
    )
  }
```
