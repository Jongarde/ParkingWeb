const request = require('request');

function getBrands(){
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
      request.post({
        url: 'http://127.0.0.1:8000/brands',
        body: {brands: brandNames},
        json: true
      }, (error, response, body) => {
        if (!error && response.statusCode === 200) {
          console.log(body);
        } else {
          console.error(error);
        }
      });
    }
  });
  
}

getBrands()
