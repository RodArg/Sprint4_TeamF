
const express = require('express');

const path = require('path');
const app = express();

app.set('view engine', 'hbs');
app.use(express.static(path.join(__dirname, '/public')));
app.use(express.urlencoded({ extended: false })); 

//create table object
//create transactin form




app.get('/', function(req, res) {
    res.render('login');
});

app.get('/budgeting', function(req,res) {
  res.render('budgeting'); //pass transaction form as an argument here
});  

app.post('/budgeting', function(req,res) {
  res.render('budgeting'); //pass transaction form as an argument here
}); //handle form submission data here

app.listen(3000);





