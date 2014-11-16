var sock = new SockJS("http://localhost:8888/echo");
//var sock = new SockJS("http://93.175.18.108/echo");


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
		var msg = { action: 'ready' };

		sock.send(JSON.stringify(msg));
		
	} else if (data.action === "waiting") {
		//$("#main-content").html("<h2>Please, wait partner</h2>");
		
	} else if (data.action === "tasking") {
		//$("#main-content").html("<h2>Tasking</h2>");
		var score0 = data.score0,
			score1 = data.score1;
		
		for (i = 0; i < data.tasks0.length; i++) {
		//	$("#main-content").append("<h2>" + data.tasks0[i] + "</h2>");
            var game = document.getElementById("gameField"); 
            var canvas = game.getContext("2d");
            game.width = window.innerWidth;  
            game.height = 0.8*window.innerHeight;

            canvas.lineWidth = 5; 
            canvas.strokeStyle = "black";           
            canvas.strokeRect(20, game.height*0.05, window.innerWidth*0.47, game.height*0.9-10);
            canvas.strokeRect(game.width-0.47*window.innerWidth, game.height*0.05, window.innerWidth*0.47-20, game.height*0.9-10);
            canvas.font = "bold 24px vendra";
          /*  var img= new Image();
            
            img.src = "/static/images/11.png";
            canvas.drawImage(img,100,200);*/
            var x = Math.floor(Math.random() * ((window.innerWidth*0.47-50) - 70 + 1)) + 70;
            var y = Math.floor(Math.random() * (game.height*0.9-10 - 50 - game.height*0.05 - 50 + 1)) + Math.floor(game.height*0.05) + 50;
            var z = Math.floor(Math.random() * ((game.width-70) - (game.width-0.47*window.innerWidth+50) + 1)) + (game.width-0.47*window.innerWidth + 50);
            var t = Math.floor(Math.random() * (game.height*0.9-10 -50 - game.height*0.05 - 50 + 1)) + Math.floor(game.height*0.05) +50;
           
            canvas.fillStyle = "aqua";
            canvas.arc(x, y, 50, 0, 50);
            canvas.arc(z, t, 50, 0, 50);
            canvas.fill();
            canvas.fillStyle = "black";
            canvas.fillText(data.tasks0[i], x-25, y+5);
            canvas.fillText(data.tasks1[i], z-25, t+5);
	    }
		
		var msg = { action: 'ready' };
		sock.send(JSON.stringify(msg));
		
		
	} else if (data.action === "result") {
	//	$("#main-content").append("<h2>" + data.result + "</h2>");
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
