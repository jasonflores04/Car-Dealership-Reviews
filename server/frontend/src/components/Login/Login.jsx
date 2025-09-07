/**
 * React component that renders a login form as a modal for user authentication
 *
 * Responsibilities:
 * - Collect username and password inputs from the user
 * - Send login request to backend API
 * - Authenticate user and store session data in sessionStorage
 * - Redirect to homepage upon successful login
 * - Provide a cancel option to close the login modal
 * - Provide a link to the registration page for new users
*/

import React, { useState } from 'react';
import "./Login.css";
import Header from '../Header/Header';

const Login = ({ onClose }) => {
  // State to store username and password inputs
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  // State to track whether the login modal is open
  const [open,setOpen] = useState(true)

  // Backend login API URL
  let login_url = window.location.origin+"/djangoapp/login";

  // Function to handle login form submission
  const login = async (e) => {
    e.preventDefault(); // Prevent default form submission

    // Send POST request to backend with username and password
    const res = await fetch(login_url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "userName": userName,
            "password": password
        }),
    });
    
    const json = await res.json();
    // If authentication successful, store username in session and close modal
    if (json.status != null && json.status === "Authenticated") {
        sessionStorage.setItem('username', json.userName);
        setOpen(false);        
    }
    // Alert if login failed
    else {
      alert("The user could not be authenticated.")
    }
};

  // Redirect to homepage if modal closed after successful login
  if (!open) {
    window.location.href = "/";
  };
  

  return (
    <div>
      <Header/>
    <div onClick={onClose}>
      <div
        onClick={(e) => {
          e.stopPropagation();
        }}
        className='modalContainer'
      >
          <form className="login_panel" style={{}} onSubmit={login}>
              <div>
              <span className="input_field">Username </span>
              <input type="text"  name="username" placeholder="Username" className="input_field" onChange={(e) => setUserName(e.target.value)}/>
              </div>
              <div>
              <span className="input_field">Password </span>
              <input name="psw" type="password"  placeholder="Password" className="input_field" onChange={(e) => setPassword(e.target.value)}/>            
              </div>
              <div>
              <input className="action_button" type="submit" value="Login"/>
              <input className="action_button" type="button" value="Cancel" onClick={()=>setOpen(false)}/>
              </div>
              <a className="loginlink" href="/register">Register Now</a>
          </form>
      </div>
    </div>
    </div>
  );
};

export default Login;