/**
 * Car Model
 * ---------
 * Defines the schema for a car document in MongoDB
 * Each car record is associated with a dealership (via dealer_id)
 *
 * Collection name: cars
 */

const { Int32 } = require('mongodb');
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const cars = new Schema({
dealer_id: {
    type: Number,
    required: true
},
make: {
    type: String,
    required: true
  },
model: {
    type: String,
    required: true
  },
bodyType: {
    type: String,
    required: true
  },
year: {
    type: Number,
    required: true
  },
mileage: {
    type: Number,
    required: true
  }
});

// Export Mongoose model
// Will be stored in MongoDB under collection "cars"
module.exports = mongoose.model('cars', cars);