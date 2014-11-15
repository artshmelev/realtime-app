var sock = new SockJS("http://localhost:8888/echo");

sock.onopen = function() {
    var msg = {
        action: 'connecting'
    }
    sock.send(JSON.stringify(msg));
};

sock.onmessage = function(e) {
	var data = JSON.parse(e.data);
	
	if (data.action === "startpage") {
		$("#play-btn").show();
		
	} else if (data.action === "startgame") {
		$("#play-btn").hide();
		$("#enter").show();

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
		
        var game = document.getElementById("gameField"); 
        var canvas = game.getContext("2d");
        game.width = window.innerWidth;  
        game.height = 0.8*window.innerHeight;
        
        canvas.lineWidth = 5;
        canvas.strokeStyle = "black";
        canvas.strokeRect(20, game.height*0.05, window.innerWidth*0.47, game.height*0.9-10);
        canvas.strokeRect(window.innerWidth*0.47+30, game.height*0.05, window.innerWidth*0.47, game.height*0.9-10);
        
		var msg = { action: 'ready' };
		sock.send(JSON.stringify(msg));
		
	} else if (data.action === "result") {
		$("#main-content").append("<h2>" + data.result + "</h2>");
	}
};

sock.onclose = function() {
    var msg = {
        action: 'disconnecting'
    }
};

var game = document.getElementById("gameField"); 
var canvas = game.getContext("2d");
game.width = window.innerWidth;  
game.height = 0.8*window.innerHeight;

canvas.lineWidth = 5;
canvas.strokeStyle = "black";
canvas.strokeRect(20, game.height*0.05, window.innerWidth*0.47, game.height*0.9-10);
canvas.strokeRect(window.innerWidth*0.47+30, game.height*0.05, window.innerWidth*0.47, game.height*0.9-10);

$("button").click(function() {
	var msg = { action: 'playgame' };
	sock.send(JSON.stringify(msg));
});

$("#ans").keypress(function(e) {
	if (e.which == 13) {
		var msg = { action: 'answer', answer: this.value };
		sock.send(JSON.stringify(msg));
		this.value = "";
	}
});
