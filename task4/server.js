var express = require('express');

var app = express();

var server = app.listen(process.env.PORT || 3000, listen);

function listen(){
  var host = server.address().address;
  var port = server.address().port;
  console.log('App listening at http://' + host + ':' + port);
}

app.use(express.static('p5Projects'));

