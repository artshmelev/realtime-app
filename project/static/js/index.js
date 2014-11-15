var sock = new SockJS("http://localhost:8888/echo");

sock.onopen = function() {
//	alert("open");
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
		
	} else if (data.action === "startgame") {
		$("#play-btn").hide();
		$("#main-content").html("<h2>Game is starting</h2>");
		var msg = { action: 'ready' };
		sock.send(JSON.stringify(msg));
		
	} else if (data.action === "waiting") {
		$("#main-content").html("<h2>Please, wait partner</h2>");
		
	} else if (data.action === "tasking") {
		$("#main-content").html("<h2>Tasking</h2>");
		var score0 = data.score0,
			score1 = data.score1;
		
		for (i = 0; i < data.tasks0.length; i++) {
			$("#main-content").append("<h2>" + data.tasks0[i] + "</h2>");
		}
		
		var msg = { action: 'ready' };
		sock.send(JSON.stringify(msg));
		
	} else if (data.action === "result") {
		$("#main-content").html("<h2>Result</h2>");
	}
};

sock.onclose = function() {
    var msg = {
        action: 'disconnecting'
    }
    //sock.send(JSON.stringify(msg));
};

$("button").click(function() {
	var msg = { action: 'playgame' };
	//alert("Clicked");
	sock.send(JSON.stringify(msg));
});
