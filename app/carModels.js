function getBrands(){
  const request = require('request');

  const options = {
    url: 'https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getMakes',
    headers: {
      'Content-Type': 'application/json'
    }
  };

  request(options, function(error, response, body) {
    if (!error && response.statusCode == 200) {
      body = body.substring(11, body.length - 3)
      const data = JSON.parse(body);
      const brandNames = data.map(item => item.make_display);
      console.log(brandNames);
    }
  });
}

function getModels(brand){
  const request = require('request');

  const options = {
    url: `https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getModels&make=${brand}`,
    headers: {
      'Content-Type': 'application/json'
    }
  };

  request(options, function(error, response, body) {
    if (!error && response.statusCode == 200) {
      body = body.substring(12, body.length - 3)
      const data = JSON.parse(body);
      const modelNames = data.map(item => item.model_name);
      console.log(modelNames);
    }
  });
}


