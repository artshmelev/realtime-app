var sock = new SockJS("http://localhost:8888/echo");

sock.onopen = function() {
	console.log("open");
	sock.send("test_message");
};

sock.onmessage = function(e) {
	console.log("message", e.data);
	$("#test").text(e.data);
};

sock.onclose = function() {
	console.log("close");
};