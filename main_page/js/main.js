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

function registerRelLink(li, topic){
  li.click(function(){
    $("#rel-link").html("");
    for (var j = 0; j < topic.item.length; j++){
      var tmp = $("<li>");
      var hdiv = $("<div>").addClass("collapsible-header truncate rel-link-header orange-text").html(topic.item[j].title).attr("title", topic.item[j].title);
      var bdiv = $("<div>").addClass("collapsible-body rel-link-body").html(topic.item[j].topic);
      bdiv.append($("<a>").addClass("right").attr("href", topic.item[j].href).attr("target", "_new").html('<i class="mdi-action-exit-to-app"></i>Link'));
      tmp.append(hdiv).append(bdiv);
      $("#rel-link").append(tmp);
    }
    $('.collapsible').collapsible({
      accordion : false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
    });
  });
}

var loading = $('<div id="loading"><img src="stylesheets/images/support-loading.gif" height="32px" width="32px"></img></div>');
function process(res){
	$(".hide").removeClass("hide");
	$("#form").parent().removeClass("m12").addClass("m9");
	$("#main-1").css("min-width", "85%");
	$("#key").val(res.keyword);
	$("#key").focus();

	//add noun tab
  res.noun = res.terms;
	$("#noun").html("");
	for (var i = 0; i < res.noun.length; i++){
		var li = $("<li>").html(res.noun[i]);
		li.addClass("z-depth-1 col s3 blue-text noun-tab truncate waves-effect");
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
	/*
  liList = document.getElementsByClassName("noun-tab");
	for (var i = 0; i < res.noun.length; i += 4){
		var minH = 0;
		for (var j = 0; j < 4 && i + j < res.noun.length; j++)
			minH = Math.max(minH, liList[i + j].offsetHeight);
		for (var j = 0; j < 4 && i + j < res.noun.length; j++)
			$(liList[i + j]).css("height", minH + "px");
	}
  */

  $("#toc").html("");
  for (var i = 0; i < res.toc.length; i++){
    var li = $("<li>").html(res.toc[i].topic);
    li.addClass("col s12 z-depth-1 toc-tab waves-effect");
    registerRelLink(li, res.toc[i]);
    $("#toc").append(li);
  }
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