const express = require('express');
require('dotenv').config();

const app = express();

// Set up a route to return configuration
app.get('/config.json', (req, res) => {
    // Build the JSON object based on environment variables
    const config = {
        classificationEndpoint: process.env.CLASSIFICATIONENDPOINT || 'http://localhost:5002',
        pathserviceEndpoint: process.env.PATHSERVICEENDPOINT || 'http://localhost:5003',
        droneSpeed: process.env.DRONESPEED || 0.5,
        tractorSpeed: process.env.TRACTORSPEED || 0.1,
        commSpeed: process.env.COMMSPEED || 1,
        wealthyCropInitialPercentage: process.env.WEALTHYCROPINITIALPERCENTAGE || 50,
      };
  
    // Send the JSON object as the response
    res.json(config);
  }); 

app.use(express.static('public'));

app.listen(3000, () => {
    console.log('Server started on port 3000');
  });
