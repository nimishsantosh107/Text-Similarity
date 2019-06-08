const sel = function (name){return document.querySelector(name);}

const postData = function () {
	var obj = {};
	for(var i=0;i<3;i++){
		var temp = {
			question:sel(`#Q${i+1}`).value,
			answer:sel(`#A${i+1}`).value
		}
		obj[i] = temp;
	}
	obj = JSON.stringify(obj);
	var xhttp = new XMLHttpRequest();
	xhttp.open("POST", "/postDB",true);
	xhttp.setRequestHeader('Content-Type', 'application/json');
	xhttp.send(obj);
}

sel('#postButton').addEventListener('click', postData);
