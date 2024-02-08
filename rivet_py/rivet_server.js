// rivet_server.js

// Import the express module for creating a web server
const express = require('express');

// Initialize an Express application
const app = express();

// Use express.json() middleware to parse JSON request bodies
app.use(express.json());

// Import functions from the @ironclad/rivet-node package
const { loadProjectFromFile, runGraph } = require('@ironclad/rivet-node');

// Define the project to load, from 'RIVET_PROJECT_FILEPATH' environment variable
const projectFilePath = process.env.RIVET_PROJECT_FILEPATH;
let project;

// Load project at startup
loadProjectFromFile(projectFilePath)
    .then(loadedProject => {
        project = loadedProject;
        console.log('Rivet project loaded successfully: ' + projectFilePath);
    })
    .catch(error => {
        console.error('\x1b[91mFailed to load Rivet project:\x1b[0m', error);
        process.exit(1);
    });

// Define a GET endpoint at '/health' for health checking
app.get('/health', (req, res) => {
    // Respond with HTTP 200 status code and 'OK' message
    res.status(200).send('OK');
});

// Define a POST endpoint at '/run-graph' to run the Rivet graph
app.post('/run-graph', async (req, res) => {
    try {
        // Print received request
        console.log('\x1b[90mReceived POST request at /run-graph with body:\x1b[0m');
        console.log(req.body)

        // Extract options from the request body
        const { options } = req.body;

        // Run the graph using the loaded project and provided options
        const result = await runGraph(project, options);

        // Send the result back as JSON response
        res.json(result);

        // Print response sent (success)
        console.log('\n\x1b[90mResponse sent:\x1b[0m');
        console.log(result)
    } catch (error) {
        // Send the result back as a JSON response {'error': 'error message'}
        res.status(500).send({ 'error': error.message });

        // Print response sent (error) with color red
        console.error('\x1b[91mResponse sent:', 'error:', error.message, '\x1b[0m');
    }

    // Print '-----'
    console.log('\x1b[90m' + '-'.repeat(100) + '\x1b[0m');

});

// Define the port number on which the server will listen, from 'PORT' environment variable (default is 3000)
const PORT = process.env.PORT;

// Start the server on the specified port and log a message on success
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
}).on('error', (err) => {
    // Log an error message and exit if the server fails to start
    console.error('Failed to start server:', err);
    process.exit(1);
});
