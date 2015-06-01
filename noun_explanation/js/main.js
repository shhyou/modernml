var url = "ws://toscanini.m6.ntu.edu.tw:8000/";

function initialize(){
  var input = document.getElementById("noun");
  var content = document.getElementById("context");
  var button = document.getElementById("search");
  var loading = document.getElementsByClassName("loading_container")[0];

  var ws;
  var q_vocab = null;

  function connect(){
	  ws = new WebSocket(url);
	  ws.onopen = function(){
	    console.log("connect to: " + url + " success!");
	    if (q_vocab != null){
	    	ws.send(q_vocab);
	    	q_vocab = null;
	    }
	  };
	  ws.onmessage = function(response){
	    content.innerHTML = response.data;
	    loading.style.display = "none";
	  };
	  ws.onerror = function(){
	  	console.log("connection failed.");
	  	setTimeout(connect, 5000);
	  }
	}

  button.addEventListener("click", function(e){
  	e.preventDefault();
  	var vocab = input.value;
  	if (vocab == "")
  	  return;
    loading.style.display = "block";
    if (ws.readyState != ws.OPEN){
      q_vocab = vocab;
    	connect();
    }
    else
  		ws.send(vocab);
  });

  connect();
}

window.onload = initialize;