const express = require("express");
const app = express();
const cors = require('cors');
const port = process.env.PORT || 8080;
const { Deta } = require('deta');


// Allow only one site to access this API
const corsOptions = {
    //origin: 'http://localhost:4200'
    origin: 'https://condor.2187.io'
};


const deta = Deta("YourProjectKey"); 

// Connect to db
const db = deta.Base('Condor');
const db_strategies = deta.Base('StrategyPerformance');

// Enable CORS for one site with the options
app.use(cors(corsOptions));

app.listen(port, () => {
  console.log(`App listening on port ${port}!`);
});


app.get("/", (req, res) => {

    let dataPromise = db.fetch();
    let strategiesPromise = db_strategies.fetch();

    Promise.all([dataPromise, strategiesPromise]).then(([data, strategies]) => {
      let response = { data, strategies };
      res.json(response);
    }).catch((error) => {
      console.error('Error:', error);
      res.status(500).json({ error: 'An error occurred while fetching the data.' });
    }); 
    
  });