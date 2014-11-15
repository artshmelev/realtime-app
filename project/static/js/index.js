var sock = new SockJS("http://localhost:8888/echo");

sock.onopen = function() {
    var msg = {
        action: 'connecting';
    }
    sock.send(JSON.stringify(msg));
};

sock.onmessage = function(e) {
	var data = JSON.parse(e);
	
    switch (data.action) {
        case "waiting":
	        //рисуем ожидание        
            break;	
	    case "startgame":
	        //рисуем начало
	        var msg = {
                action: 'ready';
            }
	        sock.send(JSON.stringify(msg));
	        break;    
	    case "tasking":
	        //отрисовываем задание
	        
	        //посылаем answer
	        break;
	    case "result":
	        //добавляем счет, или нет
	        //если набрал счет - то, заканчиваем игру
	        break;    
};

sock.onclose = function() {
    var msg = {
        action: 'disconnetcing';
    }
};
