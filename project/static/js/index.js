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
		$("#main-content").html("<div>Game is starting</div>");
		var msg = { action: 'ready'};
		sock.send(JSON.stringify(msg));
		
	} else if (data.action === "waiting") {
		$("#main-content").html("<div>Please, wait partner</div>");
		
	} else if (data.action === "tasking") {
		$("#main-content").html("<div>Tasking</div>");
		var score = 0;
		
		var msg = { action: 'ready'};
		sock.send(JSON.stringify(msg));
		
	} else if (data.action === "result") {
		$("#main-content").html("<div>Result</div>");
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
