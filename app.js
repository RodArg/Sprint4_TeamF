const express = require('express');
const path = require('path');
const app = express();

let {PythonShell} = require('python-shell')
let pyshell = new PythonShell('my_script.py');

app.set('view engine', 'hbs');
app.use(express.static(path.join(__dirname, '/public')));
app.use(express.urlencoded({ extended: false })); 







/*
let options = {
  mode: 'text',
  pythonPath: 'path/to/python', //change path
  pythonOptions: ['-u'], // get print results in real-time
  scriptPath: 'path/to/my/scripts', //change path
  args: ['value1', 'value2', 'value3'] //change args
};

PythonShell.run('my_script.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});
*/
// sends a message to the Python script via stdin
pyshell.send('hello');

pyshell.on('message', function (message) {
  // received a message sent from the Python script (a simple "print" statement)
  console.log(message);
});

// end the input stream and allow the process to exit
pyshell.end(function (err,code,signal) {
  if (err) throw err;
  console.log('The exit code was: ' + code);
  console.log('The exit signal was: ' + signal);
  console.log('finished');
});










//temp hardcoding transaction data
class transaction {
	constructor(date, company, amount) {
		this.date = date;
		this.company = company;
		this.amount = amount;
	}
}

const transArr = [];
const trans1 = new transaction(new Date(2020, 08, 01), 'Wawa', 5.02);
const trans2 = new transaction(new Date(2020, 08, 01), 'Shop Rite', 43.64);
const trans3 = new transaction(new Date(2020, 08, 03), 'CVS', 12.99);
transArr.push(trans1, trans2, trans3);

app.get('/', function(req, res) { //for a fake auth
	if(req.query.password === 'pat') {
		res.redirect('/budgeting');
	}
	else {
		res.render('login', {errorMessage: "Incorrect login. Try again."});
	}
});

app.get('/budgeting', function(req,res) {
	res.render('budgeting', {transactionData: transArr}); 
});  

app.post('/budgeting', function(req,res) {
	res.render('budgeting', {transactionData: transArr}); 
}); //handle form submission data here

app.listen(3000);






