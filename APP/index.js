const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const http = require('http');
const fs = require('fs'); 
const {Question} = require('./db.js');
const exec = require('child_process').exec;
const vision = require('@google-cloud/vision');
const client = new vision.ImageAnnotatorClient();
const cloudinary = require('cloudinary').v2;
const multer  = require('multer');
const Datauri = require('datauri');
const axios = require('axios');
const CircularJSON = require('circular-json');
const request = require('request');


var storage = multer.memoryStorage()
var upload = multer({ storage: storage })

const dUri = new Datauri();
const datauri = (req)=>{return dUri.format(path.extname(req.file.originalname).toString(), req.file.buffer);} 

//config cloudinary
cloudinary.config({
    cloud_name: 'dedvnkbdm',
    api_key: '597473751772424',
    api_secret: 'iRB6apu_kORSFC2k-zXNgHCmSKk'
})

var app = express();
var server = http.createServer(app);
//app.use(bodyParser.json());

//UI ROUTES
	app.use('/',express.static(path.join(__dirname,'/views/home')));

	app.use('/admin',express.static(path.join(__dirname,'/views/admin')));


//DB ROUTES
	app.post('/postDB',bodyParser.json(),async (req,res ,next)=>{
		var obj = req.body;
		for(var i=0;i<3;i++){
			var newQuestion = new Question({
				question: obj[i].question,
				answer:obj[i].answer
			});
			var doc;
			var err;
			await newQuestion.save().then(
				(doc)=>{console.log(`SAVED ${i}`);},
				(err)=>{console.log(`ERROR SAVING ${i}`);res.status(418).send(err);}
			);
		}
		res.status(200).send('SAVED');
	});

	app.get('/getDB',(req,res)=>{
		Question.find({}).then(
			(questions)=>{console.log(questions);res.status(200).send(questions);},
			(err)=>{console.log(err);res.status(418).send(err);}
		);
	});

//CLOUDINARY ROUTE
	app.post('/uploadIMG', upload.single('image'), async (req, res, next)=>{
		var imageURL;
		if (req.file) {
	        const file = datauri(req).content;
	        const resultData = await cloudinary.uploader.upload(file);
	        imageURL = resultData.secure_url;
	        const [result] = await client.documentTextDetection(imageURL);
			var fullText = result.fullTextAnnotation.text;
			fullText = fullText.replace('\n','');
			console.log(fullText);

			var finalArr = []
			
			await axios.get('http://localhost:3000/getDB').then(function (response) {
			    response = response.data;
			    var reqObject = {
			    	teach: response[0].answer,
			    	stud: fullText
			    }
			    
			    reqObject = JSON.stringify(reqObject);
				axios({
				    method: 'post',
				    url: 'http://127.0.0.1:5000/python',
				    data: reqObject,
				    headers: {'Content-Type': 'application/json'}
				})
				.then(function (response) {
				    console.log(response.data[0]);
				    finalArr.push(response.data[0]);
				    res.status(200).send(finalArr);
				})
				.catch(function (error) {
				    console.log(error);
				});
			}).catch(function (error) {
			    console.log(error);
			});

			
	    }
		else res.status(418).send('NO FILE');
	});


server.listen(3000,()=>{console.log('SERVER IS UP ON PORT 3000');});