const express = require('express');
const cors = require('cors');
const app = express();
const port = 3001;

// Enable CORS
app.use(cors({
    origin: ['http://localhost:3000', 'http://192.168.8.246:3000', 'https://beta.superstonk.army']
}));

// Root route
app.get('/', (req, res) => {
    res.send('Stonk Army, assemble!');
});

// API endpoint
app.get('/api/ping', (req, res) => {
    res.json({ message: 'pong' });
});

// Start server
app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
