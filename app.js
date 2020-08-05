const express = require('express');
const path = require('path');
const app = express();
let {PythonShell} = require('python-shell');

app.set('view engine', 'hbs');
app.use(express.static(path.join(__dirname, '/public')));
app.use(express.urlencoded({ extended: false }));




PythonShell.run('TextExtraction/pytess_extract.py', null, function (err, results) {
  if (err) throw err;
  console.log('results: %j', results);
});

//temp hardcoding transaction data
class transaction {
	constructor(date, vendor, amount) {
		this.date = date;
		this.vendor = vendor;
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
    res.render('login');
});

app.get('/budgeting', function(req,res) {
  res.render('budgeting', {transactionData: transArr});
});

app.post('/budgeting', function(req,res) {
  res.render('budgeting', {transactionData: transArr});
}); //handle form submission data here

app.listen(3000);
