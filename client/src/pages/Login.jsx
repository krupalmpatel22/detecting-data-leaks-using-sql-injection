import React, { useState } from 'react';
import '../assets/css/Login.css';
import { Link } from 'react-router-dom';

function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      console.log(formData);
      const response = await fetch('http://localhost:5000/api/login/', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      console.log(data);

      if (data.message === 'Registration successful') {
        console.log('Successfully signed up');
        window.location.replace('/login');
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="App">
      <h1 className="registration-title">Login Page</h1>
      <div>
        <input
          type="email"
          id="email"
          placeholder="Enter your E-mail"
          value={formData.email}
          onChange={handleInputChange}
          required
        />
      </div>
      <div>
        <input
          type="password"
          id="password"
          placeholder="Enter your Password"
          value={formData.password}
          onChange={handleInputChange}
          required
        />
      </div>
      <button onClick={handleRegister}>Login</button>
      <div className="registration-login-link">
            <p class="bottom-p">Create an account?</p>
            <Link class="bottom-l" to="/registration">Sign-up</Link>
        </div>
    </div>
  );
}

export default Login;
