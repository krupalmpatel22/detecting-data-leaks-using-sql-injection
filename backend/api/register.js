const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 5000;

app.use(bodyParser.json());

app.post('/api/register', (req, res) => {
  // Handle registration logic here
  const { username, email, password } = req.body;

  // Perform validation and save user data to a database (not implemented in this example)

  res.json({ success: true, message: 'Registration successful' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
