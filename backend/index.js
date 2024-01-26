const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 5000;
app.use(cors({ origin: '*' }));
app.use(bodyParser.json());

app.post('/api/register', (req, res) => {
  // Handle registration logic here
  const { username, email, password, name, age, phno } = req.body;

  // Perform validation and save user data to a database (not implemented in this example)
  console.log('User data received:', username, email, password, name, age, phno);

  res.json({ success: true, message: 'Registration successful' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
