const express = require('express');
const app = express();
const measureTime = require("./utils").measureTime;
const charset = require("charset");

// Middleware to log headers
app.use((req, res, next) => {
    console.log("Headers:");
    console.log(req.headers);
    next();
});

// Route to handle root URL
app.get('/', (req, res) => {
    console.log("Root ===========================>")
    res.send('Hello World!');
});

// Route to handle URL with parameter
app.get('/user/:id', (req, res) => {
    const userId = req.params.id;
    console.log("NOT KEY ===========================>")

    
    let t = measureTime(function () {
        charset("encoding=" + " ".repeat(userId));
    });
    let time = t[0] + t[1] / 1000000000;

    res.send(`User ID: ${userId} ${time}`);
});

app.get('/user', (req, res) => {
    const userId = req.query.id;
    console.log("Here===========================>")
    res.send(`User ID: ${userId}`);
});

const PORT = process.env.PORT || 80;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
