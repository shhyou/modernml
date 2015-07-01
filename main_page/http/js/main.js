function resizeMainContainer(){
	$("#main").css("min-height", window.innerHeight + "px");
	$("#main .container").css("min-height", window.innerHeight + "px");
  $("#overlay").css("width", window.innerWidth);
  $("#overlay").css("height", window.innerHeight);

  $(".rlk").css('max-height', window.innerHeight);
  $(".rlk").css("top", "0px");
  rlk_upperline = $(".rlk").offset().top;
  moveRelLink();
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

var rlk_upperline;
function moveRelLink(){
  if (rlk_upperline == undefined)
    $(".rlk").css('top', '0px');
  else if (parseInt($(window).scrollTop()) > rlk_upperline)
    $(".rlk").css('top', parseInt($(window).scrollTop() - rlk_upperline) + "px");
  else
    $(".rlk").css('top', '0px');
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
    var li_list = {}, counter = {};
    var cnt = 0;
    for (var j = 0; j < topic.item.length; j++){
      if (li_list[topic.item[j].href] == undefined){
        cnt++;
        li_list[topic.item[j].href] = $("<li>");
        counter[topic.item[j].href] = 0;
        $("#rel-link").append(li_list[topic.item[j].href]);
        var hdiv = $("<div>").addClass("collapsible-header truncate rel-link-header orange-text").html(cnt + ". " + topic.item[j].title).attr("title", topic.item[j].title);
        var bdiv = $("<div>").addClass("collapsible-body rel-link-body");
        li_list[topic.item[j].href].append(hdiv).append(bdiv);
      }      

      counter[topic.item[j].href]++;
      li_list[topic.item[j].href].children(".collapsible-body").append("(" + counter[topic.item[j].href] + ") " + topic.item[j].topic + "<br>")
      
    }

    for (var key in li_list){
      li_list[key].children(".collapsible-body").append($("<a>").addClass("right").attr("href", key).attr("target", "_new").html('<i class="mdi-action-exit-to-app"></i>Link'));
    }

    $('.collapsible').collapsible({
      accordion : false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
    });
  });
}

var keyword_now;
function send_noun(vocab){
  if (ws.readyState > 1){
    q_vocab = vocab;
    connectWS();
  }
  else
    ws.send(JSON.stringify({"vocab": vocab.substring(vocab.indexOf(" ")), "keyword": keyword_now}));
}

var loading = $('<div id="loading"><img src="stylesheets/images/support-loading.gif" height="32px" width="32px"></img></div>');
function process(res){
  $("#explanation").html('');
  $("#rel-link").html("");
	$(".hide").removeClass("hide");
	//$("#form").parent().removeClass("m12").addClass("m9");
	$("#main-1").css("min-width", "85%");
	$("#key").val(res.keyword);
	$("#key").focus();

  keyword_now = res.keyword;

	//add noun tab
  res.noun = res.terms;
	$("#noun").html("");
  if (res.noun != undefined){
  	for (var i = 0; i < res.noun.length; i++){
  		var li = $("<li>").html((i + 1) + ". " + res.noun[i]);
  		li.addClass("z-depth-1 col s3 blue-text noun-tab truncate waves-effect");
  		li.click(function(){
        $(".noun-tab.orange-text").removeClass("orange-text").addClass("blue-text");
        $(this).removeClass("blue-text");
        $(this).addClass("orange-text");
  			$("#explanation").html(loading);
  			if (ws.readyState != ws.OPEN){
  	      q_vocab = this.innerText;
  	    	connectWS();
  	    }
  	    else
          send_noun(this.innerText);
  		});
  		li.attr("title", res.noun[i]);
  		$("#noun").append(li);
  	}
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

  $(".rlk").css("top", "0px");
  rlk_upperline = $(".rlk").offset().top;

  $("#toc").html("");
  if (res.toc != undefined){
    for (var i = 0; i < res.toc.length; i++){
      var li = $("<li>").html((i + 1) + ". " + res.toc[i].topic);
      li.addClass("col s12 z-depth-1 toc-tab waves-effect");
      registerRelLink(li, res.toc[i]);
      $("#toc").append(li);
    }
  }
}

var ws, q_vocab;
function connectWS(){
	var url = "ws://linux17.csie.ntu.edu.tw:8357/";
  ws = new WebSocket(url);
  ws.onopen = function(){
    console.log("connect to: " + url + " success!");
    if (q_vocab != null){
      send_noun(q_vocab);
    	q_vocab = null;
    }
  };
  ws.onmessage = function(response){
    var res = JSON.parse(response.data);
    $("#explanation").html("");
    $("#explanation").append($("<h5>").append($("<a>").attr("target", "_new").attr("href", "https://en.wikipedia.org/wiki/" + res.title).html(res.title)));
  	$("#explanation").append($("<span>").html(res.content));
    $('#explanation').append("<br><br>");
    var span = $("<span>");
    $("#explanation").append(span);
    for (var i = 0; i < Math.min(res.others.length, 4); i++){
      res.others[i] = decodeURIComponent(decodeURI(decodeURI(res.others[i])));
      if (i == 0)
        span.append("Others: ");
      else
        span.append(", ");
      var a = $("<a>");
      span.append(a);
      a.attr("href", "https://en.wikipedia.org/wiki/" + res.others[i]).attr("target", "_new").html(res.others[i]);
    }
  };
  ws.onerror = function(){
  	console.log("connection failed.");
  	setTimeout(connectWS, 5000);
  }
}

window.onload = function(){
  window.addEventListener('resize', resizeMainContainer);
  window.addEventListener('scroll', moveBackground);
  window.addEventListener('scroll', moveRelLink);

  resizeMainContainer();

  $("#start-button").click(function(e){
  	e.preventDefault();
  	scrollToMain();
  });

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
  $("#submit").click(function(e){
    e.preventDefault();

    var query = $('#key').val();
    if (query == '')
      return;

    showOverlay();

    $.ajax({
      url: "/submit",
      type: "GET",
      dataType:'json',
      data: {"q": query},

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

  $("#noun-ex-btn").click(function(e){
    e.preventDefault();
    var key = $("#noun-ex-key").val();
    if (key != ""){
      $("#explanation").html(loading);
      send_noun("1. " + key); //fixed with noun-tag
    }
  });

  connectWS();
};
