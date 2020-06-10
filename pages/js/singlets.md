---
layout: default
---

```js
setInterval(function() {
  var eligible = ["edit-pavement","edit-drainage","edit-structures-bridges-eligible","edit-other","edit-traffic-control-operations","edit-emergency-snow-and-ice-removal","edit-other-emergency-services","edit-engineering","edit-other-traffic-services-roadside-","edit-general-administration-and-miscellaneous-expenditures","edit-rights-of-way-eligible","edit-engineering-where-separable-","edit-construction"];
  var total = ["edit-structures-bridges","edit-emergency-snow-and-ice-removal-total","edit-other-emergency-services-total","edit-engineering-total","edit-other-traffic-services-roadside-total","edit-general-administration-and-miscellaneous-expenditures-total","edit-rights-of-way-total","edit-engineering-where-separable-total","edit-construction-total","edit-traffic-control-operations-total","edit-pavement-total","edit-drainage-total","edit-other-total"];
  var sum_total = 0;
  var sum_elig = 0;

  if(document.getElementById('edit-total-spending') != null){
    for (i = 0; i < total.length; i++) {
      var parsed = parseFloat(document.getElementById(total[i])['value']);
      if(! isNaN(parsed)){
          sum_total = sum_total + parsed;
      }
    }
    console.log("Updated Total Sum: " + sum_total);
    document.getElementById('edit-total-spending')['value'] = sum_total;

    for (i = 0; i < eligible.length; i++) {
      var parsed = parseFloat(document.getElementById(eligible[i])['value']);
      if(! isNaN(parsed)){
          sum_elig = sum_elig + parsed;
      }
    }
    console.log("Updated Eligible Sum: " + sum_elig);
    document.getElementById('edit-actual-spending-on-eligible-facilities')['value'] = sum_elig;
  }
}, 500);
```


```js
if(document.getElementById('view-field-locality-table-column') != null){
  var cells = document.getElementsByTagName("table")[0].rows[1].cells;
  var carryReceipts = cells[1]['innerHTML'].trim().substring(1);
  var newReceipts = cells[2]['innerHTML'].trim().substring(1);
  var totalReceipts = cells[3]['innerHTML'].trim().substring(1);
  document.getElementById('edit-receipt-carry-over-from-previous-year')['value'] = parseFloat(carryReceipts);
  document.getElementById('edit-new-receipts')['value'] = parseFloat(newReceipts);
  document.getElementById('edit-total-receipts')['value'] = parseFloat(totalReceipts);
}
```


## I want to download the currently playing song with js function
```js
(function(){
  var songs = document.getElementsByTagName('video');
  for(var i = 0 ; i < songs.length ; i++ ){
    if(songs[i].getAttribute("jw-played") == ""){
      window.open(songs[i]["src"]);
    }
  }
}) ();
```

# Dynamically creating New Items from an XML document for VPR site

```JavaScript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script><script type="text/javascript">
    function create(htmlStr) {
      var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
      temp.innerHTML = htmlStr;
      while (temp.firstChild) {
        frag.appendChild(temp.firstChild);
      }
      return frag;
    }

    $.ajax({
      url: 'https://api.rss2json.com/v1/api.json',
      method: 'GET',
      dataType: 'json',
      data: {
        rss_url: 'https://us6.campaign-archive.com/feed?u=ad59b4c4385511a9ec177859c&id=16860b7f9e',
        api_key: 'ourf2jvebbdifvv8g98zaunzzdky69ciafk8fzig', // put your api key here
        count: 2
      }
    }).done(function(response) {
      if (response.status != 'ok') {
        throw response.message;
      }

      console.log('====== ' + response.feed.title + ' ======');

      var item = response.items[0];
      console.log(item.title);
      console.log(item.content);
      console.log(item.pubDate);
      console.log(item.link);
      console.log(item.pubDate);
      console.log(item);

      var fragment = create("<a href='" + item.link + "'><h3>" + item.title + "</h3></a><span>" + item.pubDate + "</span><p>" + item.content + "</p>");
      document.getElementById('rss_feed').append(fragment);
    });
  </script>
```

http://www.facebook.com/uvavpr
http://www.virginia.edu/vpr
vpresearch@virginia.edu
http://www.twitter.com/uvavpr

If the xml data contains a &nbsp the title gets split up a lot. So to check for that you check the actual character.

https://stackoverflow.com/questions/5237989/nonbreaking-space
```
var x = td.text();
if (x == '\xa0') { // Non-breakable space is char 0xa0 (160 dec)
  x = '';
}
```
