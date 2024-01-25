import React, { useState } from 'react';
import './App.css';

function App() {
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [phno, setPhno] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password, name, age, phno}),
      });

      const data = await response.json();

      console.log(data);
    } catch (error) {
      console.error('Error during registration:', error);
    }
  };

  return (
    <div className="App">
      <h1>Registration Page</h1>
      <div>
        <label>Full Name:</label>
        <input type="text" value={username} onChange={(e) => setName(e.target.value)} />
      </div>
      <div>
        <label>Username:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div>
        <label>Email:</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div>
        <label>Age:</label>
        <input type="number" value={username} onChange={(e) => setAge(e.target.value)} />
      </div>
      <div>
        <label>Phone No:</label>
        <input type="number" value={username} onChange={(e) => setPhno(e.target.value)} />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <button onClick={handleRegister}>Register</button>
    </div>
  );
}

export default App;
