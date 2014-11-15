var sock = new SockJS("http://localhost:8888/echo");

sock.onopen = function() {
	alert("open");
    var msg = {
        action: 'connecting'
    }
    sock.send(JSON.stringify(msg));
};

sock.onmessage = function(e) {
	var data = JSON.parse(e.data);
	
	if (data.action === "startpage") {
		//$("#main-content").html("<button class='btn btn-primary'>Hello</button>");
		$("#play-btn").show();
		alert("startpage");
	} else if (data.action === "startgame") {
		alert("Start Game");
		$("#play-btn").hide();
	} else if (data.action === "waiting") {
		alert("waiting");
	} else if (data.action === "tasking") {
		alert("tasking");
	} else if (data.action === "result") {
		alert("result");
	}
};

sock.onclose = function() {
    var msg = {
        action: 'disconnetcing'
    }
    //sock.send(JSON.stringify(msg));
};

$("button").click(function() {
	var msg = { action: 'playgame' };
	alert("Clicked");
	sock.send(JSON.stringify(msg));
});
