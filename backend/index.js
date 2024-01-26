const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const mysql = require('mysql2');

require('dotenv').config();

const pool = mysql.createPool({
  host: process.env.MYSQL_HOST,
  port: process.env.MYSQL_PORT,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DATABASE,
}).promise();

const app = express();
const port = 5000;
app.use(cors({ origin: '*' }));
app.use(bodyParser.json());

app.post('/api/register', (req, res) => {
  // Handle registration logic here
  const { email, password, name, age, phno } = req.body;

  // Perform validation and save user data to a database (not implemented in this example)
  console.log('User data received:', email, password, name, age, phno);

  // Sending data to MySQL database table 'users'
  pool.query(`
  INSERT INTO users (Email, Password, Name, Age, phno) 
  VALUES (?, ?, ?, ?, ?)
  `, [email, password, name, age, phno]);

  res.json({ success: true, message: 'Registration successful' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
