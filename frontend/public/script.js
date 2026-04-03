/**
 * World Time & Weather Dashboard
 * Frontend JavaScript
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

const API_URL = 'http://localhost:3000/api';
const REFRESH_INTERVAL = 30000; // 30 seconds
const TIMEZONE_OFFSET = new Date().getTimezoneOffset();

// ============================================================================
// DOM ELEMENTS
// ============================================================================

const regionsGrid = document.getElementById('regionsGrid');
const errorMessage = document.getElementById('errorMessage');
const errorDetails = document.getElementById('errorDetails');
const statusIndicator = document.getElementById('statusIndicator');
const lastUpdateElement = document.getElementById('lastUpdate');
const statusText = statusIndicator?.querySelector('.status-text');
const statusDot = statusIndicator?.querySelector('.status-dot');

// ============================================================================
// MAIN APPLICATION
// ============================================================================

class WorldTimeWeatherApp {
    constructor() {
        this.data = null;
        this.lastUpdateTime = null;
        this.isLoading = false;
        this.init();
    }

    /**
     * Initialize the application
     */
    init() {
        console.log('🌍 Initializing World Time & Weather App...');
        
        // Fetch initial data
        this.fetchData();
        
        // Set up auto-refresh
        setInterval(() => this.fetchData(), REFRESH_INTERVAL);
        
        // Update local clock every second
        setInterval(() => this.updateLocalClock(), 1000);
    }

    /**
     * Fetch data from the API
     */
    async fetchData() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.updateStatus('Loading...', false);
        
        try {
            console.log(`📡 Fetching data from ${API_URL}/regions`);
            
            const response = await fetch(`${API_URL}/regions`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const responseData = await response.json();
            
            if (!responseData.success) {
                throw new Error(responseData.error || 'Unknown error');
            }
            
            this.data = responseData;
            this.lastUpdateTime = new Date();
            
            console.log('✅ Data fetched successfully', this.data);
            
            // Render the data
            this.render();
            
            // Update status
            this.updateStatus('Connected', true);
            
            // Hide error message
            this.hideError();
            
        } catch (error) {
            console.error('❌ Error fetching data:', error);
            
            // Update status
            this.updateStatus(`Error: ${error.message}`, false);
            
            // Show error message
            this.showError(error.message);
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Render the regions data
     */
    render() {
        if (!this.data || !this.data.regions) {
            console.warn('No data to render');
            return;
        }

        // Clear previous content
        regionsGrid.innerHTML = '';

        // Render each region
        this.data.regions.forEach((region, index) => {
            const card = this.createRegionCard(region);
            regionsGrid.appendChild(card);
            
            // Stagger the animation
            card.style.animationDelay = `${index * 0.1}s`;
        });

        // Update last update time
        this.updateLastUpdateTime();
    }

    /**
     * Create a region card element
     * @param {Object} region - Region data
     * @returns {HTMLElement} Region card element
     */
    createRegionCard(region) {
        const card = document.createElement('div');
        card.className = 'region-card';

        const { name, flag, country, timezone, time, weather } = region;
        const timeData = time || {};
        const weatherData = weather || {};

        // Format time
        const timeFormatted = timeData.formatted || '--:--:--';
        const dayName = timeData.day || '---';
        const dateStr = timeData.date || '---';

        // Weather data
        const temperature = weatherData.temperature || '---';
        const description = weatherData.description || 'No data';
        const humidity = weatherData.humidity || '---';
        const windSpeed = weatherData.wind_speed || '---';
        const weatherIcon = this.getWeatherIcon(weatherData.icon) || '🌤️';

        card.innerHTML = `
            <!-- Region Header -->
            <div class="region-header">
                <div class="region-flag">${flag}</div>
                <div class="region-name">
                    <h2>${name}</h2>
                    <div class="region-country">${country}</div>
                    <div class="region-timezone">${timezone}</div>
                </div>
            </div>

            <!-- Time Section -->
            <div class="time-section">
                <div class="time-section-label">📍 Current Time</div>
                <div class="time-display">
                    <div class="time-value">${timeFormatted}</div>
                    <div class="time-details">
                        <div class="time-detail">
                            <span class="time-detail-value">${dayName}</span>
                            <div class="time-detail-label">Day</div>
                        </div>
                        <div class="time-detail">
                            <span class="time-detail-value">${dateStr}</span>
                            <div class="time-detail-label">Date</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Weather Section -->
            <div class="weather-section">
                <div class="weather-section-label">🌤️ Weather</div>
                <div class="weather-main">
                    <div class="weather-icon">${weatherIcon}</div>
                    <div class="weather-info">
                        <h3>${temperature}°C</h3>
                        <div class="weather-description">${description}</div>
                    </div>
                </div>
                <div class="weather-details">
                    <div class="weather-detail">
                        <span class="weather-detail-value">${humidity}%</span>
                        <div class="weather-detail-label">Humidity</div>
                    </div>
                    <div class="weather-detail">
                        <span class="weather-detail-value">${windSpeed}m/s</span>
                        <div class="weather-detail-label">Wind Speed</div>
                    </div>
                </div>
            </div>
        `;

        return card;
    }

    /**
     * Get weather icon emoji based on API code
     * @param {string} iconCode - Icon code from API
     * @returns {string} Emoji representation
     */
    getWeatherIcon(iconCode) {
        const iconMap = {
            '01d': '☀️',   // Clear sky day
            '01n': '🌙',   // Clear sky night
            '02d': '⛅',   // Few clouds day
            '02n': '🌤️',  // Few clouds night
            '03d': '☁️',   // Scattered clouds
            '03n': '☁️',   // Scattered clouds
            '04d': '☁️',   // Broken clouds
            '04n': '☁️',   // Broken clouds
            '09d': '🌧️',   // Shower rain
            '09n': '🌧️',   // Shower rain
            '10d': '🌦️',   // Rain day
            '10n': '🌧️',   // Rain night
            '11d': '⛈️',   // Thunderstorm
            '11n': '⛈️',   // Thunderstorm
            '13d': '❄️',   // Snow
            '13n': '❄️',   // Snow
            '50d': '🌫️',   // Mist
            '50n': '🌫️',   // Mist
        };
        return iconMap[iconCode] || '🌤️';
    }

    /**
     * Update the last update time display
     */
    updateLastUpdateTime() {
        if (!this.lastUpdateTime) return;

        const updateSpan = lastUpdateElement?.querySelector('span');
        if (!updateSpan) return;

        const hours = String(this.lastUpdateTime.getHours()).padStart(2, '0');
        const minutes = String(this.lastUpdateTime.getMinutes()).padStart(2, '0');
        const seconds = String(this.lastUpdateTime.getSeconds()).padStart(2, '0');

        updateSpan.textContent = `${hours}:${minutes}:${seconds}`;
    }

    /**
     * Update status indicator
     * @param {string} text - Status text
     * @param {boolean} isConnected - Connection status
     */
    updateStatus(text, isConnected) {
        if (!statusText) return;

        statusText.textContent = text;

        if (statusDot) {
            if (isConnected) {
                statusDot.style.background = '#00d084';
                statusDot.style.animation = 'pulse 2s infinite';
            } else {
                statusDot.style.background = '#ff3366';
                statusDot.style.animation = 'none';
            }
        }
    }

    /**
     * Show error message
     * @param {string} message - Error message
     */
    showError(message) {
        if (!errorMessage) return;

        errorDetails.textContent = message || 'An unexpected error occurred';
        errorMessage.style.display = 'block';
    }

    /**
     * Hide error message
     */
    hideError() {
        if (!errorMessage) return;
        errorMessage.style.display = 'none';
    }

    /**
     * Update local clock (optional feature)
     */
    updateLocalClock() {
        if (!this.lastUpdateTime) {
            this.updateLastUpdateTime();
        }
    }
}

// ============================================================================
// APPLICATION INITIALIZATION
// ============================================================================

// Start the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM Content Loaded');
    window.app = new WorldTimeWeatherApp();
});

// ============================================================================
// ERROR HANDLING
// ============================================================================

window.addEventListener('error', (event) => {
    console.error('🔴 Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('🔴 Unhandled promise rejection:', event.reason);
});

// ============================================================================
// UTILITIES
// ============================================================================

/**
 * Format time for display
 * @param {Date} date - Date object
 * @returns {string} Formatted time
 */
function formatTime(date) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${hours}:${minutes}:${seconds}`;
}

/**
 * Format date for display
 * @param {Date} date - Date object
 * @returns {string} Formatted date
 */
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

/**
 * Get day name
 * @param {Date} date - Date object
 * @returns {string} Day name
 */
function getDayName(date) {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return days[date.getDay()];
}
