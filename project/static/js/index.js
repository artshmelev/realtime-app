var sock = new SockJS("http://localhost:8888/echo");

sock.onopen = function() {
	alert("open");
    var msg = {
        action: 'connecting'
    }
    sock.send(JSON.stringify(msg));
};

sock.onmessage = function(e) {
	var data = JSON.parse(e);
	
	if (data.action === "startpage") {
		//$("main-content").text = "Hello";
		alert("msg");
	}
    /*switch (data.action) {
    	case "startpage":
    		//$("main-content").text = "Hello";
    		break;
        case "waiting":
	        //рисуем ожидание        
            break;	
	    case "startgame":
	        //рисуем начало
	        var msg = {
                action: 'ready'
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
	        break;    */
};

sock.onclose = function() {
    var msg = {
        action: 'disconnetcing'
    }
};
