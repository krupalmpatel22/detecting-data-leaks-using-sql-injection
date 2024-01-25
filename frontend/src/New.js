import React, { useState } from 'react';

function SignUpForm() {
  const [formData, setFormData] = useState({
    mail: '',
    password: '',
    phone: '',
    dob: '',
    captchaCode: '',
    otp: '',
  });
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Implement form validation here

    if (valid) {
      // Send form data to your backend server
      // ...

      // Clear form data and error message
      setFormData({
        mail: '',
        password: '',
        phone: '',
        dob: '',
        captchaCode: '',
        otp: '',
      });
      setErrorMessage('');
    } else {
      // Set error message
      setErrorMessage('Please correct the errors in the form');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Sign Up</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <div className="form-group">
        <label htmlFor="mail">Mail Id:</label>
        <input
          type="email"
          name="mail"
          id="mail"
          value={formData.mail}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          name="password"
          id="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="phone">Phone No:</label>
        <input
          type="tel"
          name="phone"
          id="phone"
          value={formData.phone}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="dob">DOB (DDMMYYYY):</label>
        <input
          type="date"
          name="dob"
          id="dob"
          value={formData.dob}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="captchaCode">Enter Captcha Code:</label>
        <img src="https://example.com/captcha.png" alt="CAPTCHA" />
        <input
          type="text"
          name="captchaCode"
          id="captchaCode"
          value={formData.captchaCode}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="otp">Enter OTP:</label>
        <input
          type="text"
          name="otp"
          id="otp"
          value={formData.otp}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Sign Up</button>
    </form>
  );
}

export default SignUpForm;
