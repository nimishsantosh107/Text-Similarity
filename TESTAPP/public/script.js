const sel = function (name){return document.querySelector(name);}

//SERVER COMM FOR TEST
const string1 = sel("#string1");
const string2 = sel("#string2");
const testButton = sel("#testButton").addEventListener('click',function () {
	obj ={};
	obj["S1"]=string1.value.toLowerCase();
	obj["S2"]=string2.value.toLowerCase();
	JSONobj=JSON.stringify(obj);
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.open("POST", "/test", true);
	xmlhttp.setRequestHeader('Content-Type', 'application/json');
	xmlhttp.send(JSONobj);
});