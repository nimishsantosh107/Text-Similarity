const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const http = require('http');
const fs = require('fs'); 
const exec = require('child_process').exec;
const vision = require('@google-cloud/vision');
const client = new vision.ImageAnnotatorClient();

var app = express();
var server = http.createServer(app);
app.use(bodyParser.json());


app.use('/',express.static(path.join(__dirname,'/views/home')));

app.use('/admin',express.static(path.join(__dirname,'/views/admin')));


server.listen(3000,()=>{console.log('SERVER IS UP ON PORT 3000');});