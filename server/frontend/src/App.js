/*
This file defines the main React application component and configures
client-side routing

Routes:
/login: Renders the LoginPanel component for user authentication
/register: Renders the RegisterPanel component for user signup
/dealers: Displays a list of car dealers (Dealers component)
/dealer/:id = Displays details for a specific dealer (Dealer component)
/postreview/:id = Allows a logged-in user to submit a review for a dealer
/searchcars/:id = Displays available cars from a given dealer
*/

import LoginPanel from "./components/Login/Login"
import RegisterPanel from "./components/Register/Register"
import { Routes, Route } from "react-router-dom";
import Dealers from './components/Dealers/Dealers';
import Dealer from "./components/Dealers/Dealer"
import PostReview from "./components/Dealers/PostReview"
import SearchCars from "./components/Dealers/SearchCars";	

// Routes
function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<RegisterPanel />} />

      <Route path="/dealers" element={<Dealers/>} />
      <Route path="/dealer/:id" element={<Dealer/>} />
      <Route path="/postreview/:id" element={<PostReview/>} />

      <Route path="/searchcars/:id" element={<SearchCars />} />
    </Routes>
  );
}
export default App;