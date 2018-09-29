function play(ele){
  var type=ele.getAttribute("data-type");
  var series=ele.getAttribute("data-series");
  var episode=ele.getAttribute("data-episode");


  var video_choice = {
    "type": type,
    "series": series,
    "episode": episode
  };

  // query = "http://localhost:8000" + "\?" + type + "\\" + series + "\\" + episode
  var query = "http://localhost:8000/\?" + ele.id

  const myRequest = new Request(query , {method: 'GET'});

  fetch(myRequest)
  .then(response => {
    if (response.status === 200) {
      return;
    } else {
      throw new Error('Something went wrong on video server!');
    }
  })
  .then(response => {
    console.debug(response);
    // ...
  }).catch(error => {
    console.error(error);
  });
}
