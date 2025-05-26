const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();
const port = 3000;

const sql = require('mssql');
// SQL Server configuration
const config = {
  user: process.env.LOCAL_SQLEXPRESS_USER,
  password: process.env.LOCAL_SQLEXPRESS_PW,
  database: 'FamilyTree',
  server: 'localhost',
  port: 1433,
  options: {
    trustServerCertificate: true,
    trustedConnection: false, // Set to true if using Windows Authentication
    encrypt: false // for azure
  },
};


async function getMembers(){
  try {
    // Connect to the database
    const pool = await sql.connect(config);
    const result = await pool.request().query('select * from Members');
    console.log('getMembers', result);

    return result.recordset;
  } catch (err) {
    console.error('SQL error', err);
    throw err;
  }
}

app.get('/api/members', async (req, res) => {
  try {
    const members = await getMembers();
    res.json(members);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch members from database' });
  }
});

// Serve static files from public folder
app.use(express.static(path.join(__dirname, '..', 'public')));

// Start server
app.listen(port, () => {
  console.log(`Backend server running at http://localhost:${port}`);
});

