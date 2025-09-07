
const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = 3050;

app.use(cors());
app.use(express.urlencoded({extended: false}));

const Cars = require('./inventory');
const carsData = JSON.parse(fs.readFileSync('car_records.json'));

mongoose.connect('mongodb://mongo_db:27017/', {dbName: 'dealershipsDB'})
        .then(async () => {
            console.log('MongoDB connected');

            try {
                await Cars.deleteMany({});
                const insertedCars = await Cars.insertMany(carsData.cars);
                console.log(`Initial data inserted: ${insertedCars.length} documents inserted`);
            }
            catch(error){
                console.error('Error initializing database:', error);
            }
        })
        .catch(err => {
            console.error('MongoDB connection error:', err);
        });

app.get('/', async (req, res) => {
    res.send('Welcome to the Mongoose API');
});

app.get('/cars/:id', async (req, res) => {
    try{
        const document = await Cars.find({dealer_id: req.params.id});
        res.json(document); // Sends the JSON response and terminates the function
    } 
    catch(error){
        res.status(500).json({error: 'Error fetching cars'}); //Sends an error message and terminates the function
    };
});

app.get('/carsbymake/:id/:make', async (req, res) => {
    try{
        const { id, make } = req.params;

        if (!id || !make) {
            return res.status(400).json({ error: 'Missing parameters: id and make are required' });
        }

        const document = await Cars.find({dealer_id: id, make: make});

        if (!document || document.length === 0) {
            return res.status(404).json({ error: 'No cars found' });
        }

        res.json(document);
    } 
    catch(error){
        console.error('Error fetching cars:', error); 
        res.status(500).json({error: 'Error fetching cars'});
    };
});

app.get('/carsbymodel/:id/:model', async (req, res) => {
    try{
        const document = await Cars.find({dealer_id: req.params.id, model: req.params.model});
        res.json(document);
    } 
    catch(error){
        console.error('Error fetching cars:', error); 
        res.status(500).json({error: 'Error fetching cars'});
    };
});

app.get('/carsbymaxmileage/:id/:mileage', async (req, res) => {
    try {
        let mileage = parseInt(req.params.mileage)
        let condition = {}
        if(mileage === 50000) {
          condition = { $lte : mileage}
        } else if (mileage === 100000){
          condition = { $lte : mileage, $gt : 50000}
        } else if (mileage === 150000){
          condition = { $lte : mileage, $gt : 100000}
        } else if (mileage === 200000){
          condition = { $lte : mileage, $gt : 150000}
        } else {
          condition = { $gt : 200000}
        }
        const documents = await Cars.find({ dealer_id: req.params.id, mileage : condition });
        res.json(documents);
      } catch (error) {
        res.status(500).json({ error: 'Error fetching dealers by ID' });
      }
    });

app.get('/carsbyprice/:id/:price', async (req, res) => {
    try {
        let price = parseInt(req.params.price)
        let condition = {}
        if(price === 20000) {
            condition = { $lte : price}
        } else if (price=== 40000){
            condition = { $lte : price, $gt : 20000}
        } else if (price === 60000){
            condition = { $lte : price, $gt : 40000}
        } else if (price === 80000){
            condition = { $lte : price, $gt : 60000}
        } else {
            condition = { $gt : 80000}
        }
        const documents = await Cars.find({ dealer_id: req.params.id, price : condition });
        res.json(documents);
        } catch (error) {
        res.status(500).json({ error: 'Error fetching dealers by ID' });
        }
});

app.get('/carsbyyear/:id/:year', async (req, res) => {
    try {
        const {id, year} = req.params;

        // Verify `id` type
        const idNumber = parseInt(id, 10);
        if (isNaN(idNumber)) {
            return res.status(400).json({ error: 'Invalid id type: id should be a number' });
        }

        // Verify and convert 'year' type
        const yearNumber = parseInt(year, 10);
        if (isNaN(yearNumber)) {
            return res.status(400).json({ error: 'Invalid year type: year should be a number' });
        }

        // Additional check for valid year range
        const currentYear = new Date().getFullYear();
        if (yearNumber < 1900 || yearNumber > currentYear) {
            return res.status(400).json({ error: `Invalid year: year should be between 1900 and ${currentYear}` });
        }

        const documents = await Cars.find({ dealer_id: idNumber, year : { $gte : yearNumber}});
        res.json(documents);

    } catch (error) {
        console.error('Error fetching cars by year:', error);
        res.status(500).json({ error: 'Error fetching dealers by ID' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});