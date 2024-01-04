const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 80;

// Serve static files
app.use(express.static(path.join(__dirname, 'dist')));

// Handle SPA routing, return index.html for all routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
