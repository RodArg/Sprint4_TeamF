const express = require('express');
const path = require('path');
const app = express();

let {PythonShell} = require('python-shell');

app.set('view engine', 'hbs');
app.use(express.static(path.join(__dirname, '/public')));
app.use(express.urlencoded({ extended: false }));

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
	if(req.query.userName === 'pat' && req.query.password === 'pat') {
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
	if(req.body.length != 0) {
		let fileNamePy = req.body.fileName;

		PythonShell.run('TextExtraction/console.py', 
			{mode: 'text', args: [fileNamePy]}, 
			function (err, results) {

				if(results === undefined) {
					console.log('undefined results'); //test
				}

				let json = JSON.parse(results.slice(-1)[0]);

				if (err) throw err;

				const newTrans = new transaction(new Date("2020-08-01"), json.vendor, parseFloat(json.amount)); //not working
				console.log(newTrans);
				transArr.push(newTrans); 
				console.log(transArr); //test
		});

		//for display: make a chart, get each date year, month, day for one col, vendor for second col, amount col
	}
}); 

app.listen(3000);


