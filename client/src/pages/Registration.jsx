import React, { useState } from 'react';
import '../assets/css/Registration.css'; // Import your CSS file
import { Link } from 'react-router-dom';

function Registration() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    phno: '',
    age: '',
  });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      console.log(formData);
      const response = await fetch('http://localhost:5000/api/register/', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      console.log(data);

      if (data.message === 'Registration successful') {
        alert('Registration successful');
        console.log('Successfully signed up');
        window.location.replace('/login');
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="registration-container">
      <div className="background-pattern"></div>
      <h1 className="registration-title">Registration</h1>
      <form className="registration-form">
        <div className="registration-input-container">
          <input
            type="text"
            id="name"
            placeholder="Enter your Full Name"
            value={formData.name}
            onChange={handleInputChange}
            className="registration-input"
            required
          />
        </div>
        <div className="registration-input-container">
          <input
            type="email"
            id="email"
            placeholder="Enter your E-mail"
            value={formData.email}
            onChange={handleInputChange}
            className="registration-input"
            required
          />
        </div>
        <div className="registration-input-container">
          <input
            type="number"
            id="age"
            placeholder="Enter your Age"
            value={formData.age}
            onChange={handleInputChange}
            className="registration-input"
            required
          />
        </div>
        <div className="registration-input-container">
          <input
            type="text"
            id="phno"
            placeholder="Enter your Phone No"
            value={formData.phno}
            onChange={handleInputChange}
            className="registration-input"
            required
          />
        </div>
        <div className="registration-input-container">
          <input
            type="password"
            id="password"
            placeholder="Enter your Password"
            value={formData.password}
            onChange={handleInputChange}
            className="registration-input"
            required
          />
        </div>
        <button onClick={handleRegister} className="registration-button">
          Register
        </button>
      </form>
        <div className="registration-login-link">
            <p class="bottom-p">Already have an account?</p>
            <Link class="bottom-l" to="/login">Login</Link>
        </div>
    </div>
  );
}

export default Registration;
