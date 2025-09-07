/**
 * Review Model
 * ------------
 * Defines the schema for a customer review document in MongoDB.
 * Each review is linked to a dealership (via dealership field).
 *
 * Collection name: reviews
 */

const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const reviews = new Schema({
	id: {
    type: Number,
    required: true,
	},
	name: {
    type: String,
    required: true
  },
  dealership: {
    type: Number,
    required: true,
  },
  review: {
    type: String,
    required: true
  },
  purchase: {
    type: Boolean,
    required: true
  },
  purchase_date: {
    type: String,
    required: true
  },
  car_make: {
    type: String,
    required: true
  },
  car_model: {
    type: String,
    required: true
  },
  car_year: {
    type: Number,
    required: true
  },
});

// Export Mongoose model
// Will be stored in MongoDB under collection "reviews"
module.exports = mongoose.model('reviews', reviews);