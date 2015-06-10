function resizeMainContainer(){
	$("#main").css("min-height", window.innerHeight + "px");
	$("#main .container").css("min-height", window.innerHeight + "px");
  $("#overlay").css("width", window.innerWidth);
  $("#overlay").css("height", window.innerHeight);
}

function scrollToMain(){
  $("html, body").animate({scrollTop: $("#main").offset().top}, 800);
}

function moveBackground(){
  var delta = $("body").scrollTop();
  var pos = -delta * 150 / $("#main")[0].offsetTop;
  if (pos <= 0)
    $(".bg").css("background-position-y", pos + "px");
}

function showOverlay(){
	$('#overlay').show();
	$("#overlay").animate({'opacity': '1'}, 1000);	
}

function hideOverlay(){
	$("#overlay").animate({'opacity': '0'}, 1000);	
	setTimeout("$('#overlay').hide();", 1000);
}

var loading = $('<div id="loading"><img src="stylesheets/images/support-loading.gif" height="32px" width="32px"></img></div>');
function process(res){
	$(".hide").removeClass("hide");
	$("#form").parent().removeClass("m12").addClass("m9");
	$("#main-1").css("min-width", "85%");
	$("#key").val(res.keyword);
	$("#key").focus();

	//add noun tab
	$("#noun").html("");
	for (var i = 0; i < res.noun.length; i++){
		var li = $("<li>").html(res.noun[i]);
		li.addClass("z-depth-1 col s3 blue-text noun-tab truncate");
		li.click(function(){
			$("#explanation").html(loading);
			if (ws.readyState != ws.OPEN){
	      q_vocab = this.innerText;
	    	connect();
	    }
	    else
				ws.send(this.innerText)
		});
		li.attr("title", res.noun[i]);
		$("#noun").append(li);
	}

	//fixed noun tab
	liList = document.getElementsByClassName("noun-tab");
	for (var i = 0; i < res.noun.length; i += 4){
		var minH = 0;
		for (var j = 0; j < 4 && i + j < res.noun.length; j++)
			minH = Math.max(minH, liList[i + j].offsetHeight);
		for (var j = 0; j < 4 && i + j < res.noun.length; j++)
			$(liList[i + j]).css("height", minH + "px");
	}

	// add suggest link
	$("#rel-link").html("");
	for (var i = 0; i < res.link.length; i++){
		var a = $("<a>").html(res.link[i].title).attr("href", res.link[i].href).addClass("teal-text text-lighten-2");
		var li = $("<li>").append(a).attr("title", res.link[i].title);
		li.addClass("z-depth-1 col s12 noun-tab truncate");
		$("#rel-link").append(li);
	}

	// draw flowchart
	$("#diagram").html("");
	var diagram = flowchart.parse(res.flowchart);
  diagram.drawSVG('diagram');
}

var ws, q_vocab;
function connectWS(){
	var url = "ws://linux17.csie.ntu.edu.tw:8357/";
  ws = new WebSocket(url);
  ws.onopen = function(){
    console.log("connect to: " + url + " success!");
    if (q_vocab != null){
    	ws.send(q_vocab);
    	q_vocab = null;
    }
  };
  ws.onmessage = function(response){
  	$("#explanation").html(response.data);
  };
  ws.onerror = function(){
  	console.log("connection failed.");
  	setTimeout(connect, 5000);
  }
}

window.onload = function(){
  window.addEventListener('resize', resizeMainContainer);
  window.addEventListener('scroll', moveBackground);
  resizeMainContainer();

  $("#start-button").click(function(e){
  	e.preventDefault();
  	scrollToMain();
  });

  $("#submit").click(function(e){e.preventDefault()});
  $("#good").click(function(e){
  	e.preventDefault();
  	showOverlay();

  	$.ajax({
      url: "/random",
      type: "GET",
      dataType:'json',

      success: function(res){
          process(res);
          hideOverlay();
      },

      error:function(xhr, ajaxOptions, thrownError){
        alert(xhr.status);
        alert(thrownError);
        hideOverlay();
      }
  	});
  });

  connectWS();
};

s = "st=>start: Start:>http://www.google.com[blank]\ne=>end:>http://www.google.com\nop1=>operation: My Operation\nsub1=>subroutine: My Subroutine\ncond=>condition: Yes\nor No?:>http://www.google.com\nio=>inputoutput: catch something...\n\nst->op1->cond\ncond(yes)->io->e\ncond(no)->sub1(right)->op1\n"