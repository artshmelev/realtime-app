//var sock = new SockJS("http://localhost:8888/echo");
var sock = new SockJS("http://93.175.18.108:8888/echo");

sock.onopen = function() {
    var msg = {
        action: 'connecting'
    }
    sock.send(JSON.stringify(msg));
};

sock.onmessage = function(e) {
	var data = JSON.parse(e.data);
	
	if (data.action === "startpage") {
		var canvas = document.getElementById("gameField"); 
        var ctx = canvas.getContext("2d");
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		$("#enter").hide();
		$("#play-btn").show();
		if ($("#play-btn").attr("disabled") !== undefined) {
			$("#play-btn").removeAttr("disabled");
		}
		
	} else if (data.action === "startgame") {
		$("#play-btn").hide();

        $("#enter").show();
		var msg = { action: 'ready' };

		sock.send(JSON.stringify(msg));
		
	} else if (data.action === "waiting") {
		
	} else if (data.action === "tasking") {
		$("#score0").text(data.score0);
		$("#score1").text(data.score1);

        var game = document.getElementById("gameField"); 
        var canvas = game.getContext("2d");
        game.width = window.innerWidth;  
        game.height = 0.8*window.innerHeight;
        canvas.lineWidth = 5; 
        canvas.strokeStyle = "black";           
        canvas.strokeRect(20, game.height*0.05, window.innerWidth*0.47, game.height*0.9-10);
        canvas.strokeRect(game.width-0.47*window.innerWidth, game.height*0.05, window.innerWidth*0.47-20, game.height*0.9-10);
        canvas.font = "bold 24px vendra";
		for (i = 0; i < data.tasks0.length; i++) {
            //var game = document.getElementById("gameField"); 
            //var canvas = game.getContext("2d");
            //game.width = window.innerWidth;  
            //game.height = 0.8*window.innerHeight;

            canvas.lineWidth = 5; 
            canvas.strokeStyle = "black";           
            //canvas.strokeRect(20, game.height*0.05, window.innerWidth*0.47, game.height*0.9-10);
            //canvas.strokeRect(game.width-0.47*window.innerWidth, game.height*0.05, window.innerWidth*0.47-20, game.height*0.9-10);
            canvas.font = "bold 24px vendra";
            
            var x = Math.floor(data.xs0[i] / 1366 * ((window.innerWidth*0.47-50) - 70 + 1)) + 70;
            var y = Math.floor(data.ys0[i] / 768 * (game.height*0.9-10 - 50 - game.height*0.05 - 50 + 1)) + Math.floor(game.height*0.05) + 50;
            var z = Math.floor(data.xs1[i] / 1366 * ((game.width-70) - (game.width-0.47*window.innerWidth+50) + 1)) + (game.width-0.47*window.innerWidth + 50);
            var t = Math.floor(data.ys1[i] / 768 * (game.height*0.9-10 -50 - game.height*0.05 - 50 + 1)) + Math.floor(game.height*0.05) +50;
           
            canvas.fillStyle = "aqua";
            canvas.arc(x, y, 50, 0, 50);
            canvas.arc(z, t, 50, 0, 50);
            //canvas.fill();
            canvas.fillStyle = "black";
            canvas.fillText(data.tasks0[i], x-25, y+5);
            canvas.fillText(data.tasks1[i], z-25, t+5);
	    }
		
		if (data.score0 > 50 || data.score1 > 50) {
			var msg = {
				action: 'gameover',
				score0: data.score0,
				score1: data.score1
			}
			sock.send(JSON.stringify(msg));
		} else {
			var msg = { action: 'ready' };
			sock.send(JSON.stringify(msg));
		}
		
		
	} else if (data.action === "result") {
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
canvas.strokeRect(game.width-0.47*window.innerWidth, game.height*0.05, window.innerWidth*0.47-20, game.height*0.9-10);

$("#play-btn").click(function() {
	if (!($("#play-btn").attr("disabled") !== undefined)) {
		var msg = { action: 'playgame' };
		sock.send(JSON.stringify(msg));
		
		$("#play-btn").attr("disabled", true);
	}
});

$("#ans").keypress(function(e) {
	if (e.which == 13) {
		var msg = { action: 'answer', answer: this.value };
		sock.send(JSON.stringify(msg));
		this.value = "";
	}
});
