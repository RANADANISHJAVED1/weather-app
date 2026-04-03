const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();
const path = require('path');

// ============================================================================
// CONFIGURATION
// ============================================================================

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';

// ============================================================================
// MIDDLEWARE
// ============================================================================

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ============================================================================
// ROUTES
// ============================================================================

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        service: 'World Time & Weather Frontend',
        version: '1.0.0',
        timestamp: new Date().toISOString()
    });
});

// ============================================================================
// PROXY ROUTES TO PYTHON BACKEND
// ============================================================================

/**
 * GET /api/regions
 * Fetch time and weather data for all regions from Python backend
 */
app.get('/api/regions', async (req, res) => {
    try {
        console.log(`[${new Date().toISOString()}] Fetching regions data from ${BACKEND_URL}/api/regions`);
        
        const response = await axios.get(`${BACKEND_URL}/api/regions`, {
            timeout: 10000
        });
        
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching regions from backend:', error.message);
        
        // Return error response
        res.status(error.response?.status || 500).json({
            success: false,
            error: 'Failed to fetch data from backend',
            details: error.message,
            timestamp: new Date().toISOString()
        });
    }
});

/**
 * GET /api/time
 * Fetch time data for all regions from Python backend
 */
app.get('/api/time', async (req, res) => {
    try {
        console.log(`[${new Date().toISOString()}] Fetching time data from ${BACKEND_URL}/api/time`);
        
        const response = await axios.get(`${BACKEND_URL}/api/time`, {
            timeout: 10000
        });
        
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching time from backend:', error.message);
        
        res.status(error.response?.status || 500).json({
            success: false,
            error: 'Failed to fetch time data',
            details: error.message,
            timestamp: new Date().toISOString()
        });
    }
});

/**
 * GET /api/weather
 * Fetch weather data for all regions from Python backend
 */
app.get('/api/weather', async (req, res) => {
    try {
        console.log(`[${new Date().toISOString()}] Fetching weather data from ${BACKEND_URL}/api/weather`);
        
        const response = await axios.get(`${BACKEND_URL}/api/weather`, {
            timeout: 10000
        });
        
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching weather from backend:', error.message);
        
        res.status(error.response?.status || 500).json({
            success: false,
            error: 'Failed to fetch weather data',
            details: error.message,
            timestamp: new Date().toISOString()
        });
    }
});

// ============================================================================
// ERROR HANDLERS
// ============================================================================

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        error: 'Endpoint not found',
        path: req.path,
        method: req.method,
        timestamp: new Date().toISOString()
    });
});

// Error handler
app.use((err, req, res, next) => {
    console.error('Error:', err);
    
    res.status(err.status || 500).json({
        success: false,
        error: err.message || 'Internal server error',
        timestamp: new Date().toISOString()
    });
});

// ============================================================================
// SERVER STARTUP
// ============================================================================

app.listen(PORT, () => {
    console.log('╔════════════════════════════════════════════╗');
    console.log('║  World Time & Weather (Node.js Frontend)  ║');
    console.log('╠════════════════════════════════════════════╣');
    console.log(`║ Frontend: http://localhost:${PORT}`);
    console.log(`║ Backend:  ${BACKEND_URL}`);
    console.log('║ Open in browser: http://localhost:3000');
    console.log('╚════════════════════════════════════════════╝');
    console.log();
    console.log('Available routes:');
    console.log('  - GET /              (HTML page)');
    console.log('  - GET /health        (health check)');
    console.log('  - GET /api/regions   (all regions data)');
    console.log('  - GET /api/time      (all times)');
    console.log('  - GET /api/weather   (all weather)');
    console.log();
});
