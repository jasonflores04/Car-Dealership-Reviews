/*
Entry point for the React application

Responsibilities:
Creates a React root element attached to the HTML element with id 'root'
Renders the App component inside the root element
*/

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { BrowserRouter } from "react-router-dom";

// Create the root element for React
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component inside BrowserRouter
root.render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
);