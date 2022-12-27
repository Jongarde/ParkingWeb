const request = require('request');

const options = {
  url: 'https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getModels&make=Ford',
  headers: {
    'Content-Type': 'application/json'
  }
};

request(options, function(error, response, body) {
  if (!error && response.statusCode == 200) {
    const data = JSON.parse(body);
    console.log(data.Models);
  }
});