var ws;
var index = 0;

function createBlock(name) {
	var block = document.createElement("div");
	block.id = "b" + (index++).toString();
	
	var header = document.createElement("p");
	header.innerHTML = name;
	header.onclick = function() {
		var data = {
			target: name,
			id: block.id,
			text: ""
		};
		ws.send(JSON.stringify(data));
	};
	
	block.appendChild(header);

	return block;
}

function openWS(msgContainer) {
	ws = new WebSocket("ws://localhost:8888/ws");

	ws.onmessage = function(e) {
		var data = JSON.parse(e.data);
		if (data.type == 0) {
			while (msgContainer.firstChild) {
				msgContainer.removeChild(msgContainer.firstChild);
			}
			msgContainer.appendChild(createBlock(".."))
			for (var i = 0; i < data.list.length; i++) {
				msgContainer.appendChild(createBlock(data.list[i]));
			}

		} else {
			var block = document.getElementById(data.id);
			
			if (block.firstChild != block.lastChild) {
				while (block.firstChild != block.lastChild) {
					block.removeChild(block.lastChild);
				}
			} else {
				var codeBlock = document.createElement("div");
				codeBlock.id = "editor";
				block.appendChild(codeBlock);
				
				var saveButton = document.createElement("button");
				saveButton.innerHTML = "Save";
				saveButton.onclick = function() {
					var data = {
							target: block.firstChild.innerHTML,
							id: -1,
							text: ace.edit("editor").getSession().getValue()
					};
					ws.send(JSON.stringify(data));
				}
				block.appendChild(saveButton);

				var editor = ace.edit("editor");
				editor.setTheme("ace/theme/monokai");
				editor.getSession().setMode("ace/mode/c_cpp");
				editor.setAutoScrollEditorIntoView(true);
				editor.setOption("maxLines", 20);
				editor.session.setValue(data.text);
			}
		}
	};

	ws.onclose = function(e) {
		openWS(msgContainer);
	};
}

window.onload = function() {
	var msgContainer = document.getElementById("mainblock");
	if ("WebSocket" in window) {
		openWS(msgContainer);
	} else {
		msgContainer.appendChild(createBlock("ERROR"));
	}
}
