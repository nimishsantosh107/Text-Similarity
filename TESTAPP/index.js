const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const http = require('http');
const fs = require('fs'); 
const exec = require('child_process').exec;

var app = express();
var server = http.createServer(app);
app.use(bodyParser.json());

app.use('/',express.static(path.join(__dirname+'/public')));

app.post('/test',(req,res)=>{
	var obj = req.body;
	var JSONobj = JSON.stringify(obj);
	//WRITE JSON
	fs.writeFile("input.json", JSONobj, 'utf8', function (err) {
		if (err) console.log(err);
	});
	//EXEC
	exec('python pythonProcess.py', (err, stdout, stderr)=>{
		if (err) {console.log(err); return;}
		console.log(`stdout: ${stdout}`);
	});

});


server.listen(3000,()=>{console.log('SERVER IS UP ON PORT 3000');});