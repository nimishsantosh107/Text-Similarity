const mongoose = require('mongoose');

mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost:27017/angel',{ useNewUrlParser: true });

const questionSchema = new mongoose.Schema({
	question: { type: String,},
	answer: { type: String }
});
const Question = new mongoose.model('question', questionSchema);

module.exports = {Question};