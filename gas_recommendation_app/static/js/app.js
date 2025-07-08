// Gas Station Recommendation App - Frontend JavaScript

class GasStationApp {
    constructor() {
        this.initializeEventListeners();
        this.loadConfiguration();
    }

    initializeEventListeners() {
        // Form submission
        document.getElementById('setupForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmission();
        });

        // Location type change
        document.getElementById('locationType').addEventListener('change', (e) => {
            this.handleLocationTypeChange(e.target.value);
        });

        // Fuel input type change
        document.getElementById('fuelInputType').addEventListener('change', (e) => {
            this.handleFuelInputTypeChange(e.target.value);
        });

        // Real-time fuel calculation
        document.getElementById('fuelValue').addEventListener('input', () => {
            this.calculateFuelNeeded();
        });

        document.getElementById('tankSize').addEventListener('input', () => {
            this.calculateFuelNeeded();
        });
    }

    async loadConfiguration() {
        try {
            const response = await fetch('/api/config');
            const config = await response.json();
            
            // Update form with default values
            document.getElementById('mpg').value = config.default_mpg;
            document.getElementById('tankSize').value = config.default_tank_size;
            document.getElementById('searchRadius').value = config.default_radius;
            
            // Update status with API availability
            this.updateStatus('Configuration loaded', 'success');
            this.updateApiStatus(config);
        } catch (error) {
            this.updateStatus('Failed to load configuration', 'error');
        }
    }

    updateApiStatus(config) {
        const statusContent = document.getElementById('statusContent');
        let apiStatus = '<div class="mb-3"><h6>API Status:</h6>';
        
        apiStatus += `<div class="mb-2">
            <span class="status-indicator ${config.has_google_maps ? 'success' : 'error'}"></span>
            Google Maps API: ${config.has_google_maps ? 'Available' : 'Not configured'}
        </div>`;
        
        apiStatus += `<div class="mb-2">
            <span class="status-indicator ${config.has_claude ? 'success' : 'error'}"></span>
            Claude AI: ${config.has_claude ? 'Available' : 'Not configured'}
        </div>`;
        
        apiStatus += `<div class="mb-2">
            <span class="status-indicator ${config.has_openai ? 'success' : 'error'}"></span>
            OpenAI: ${config.has_openai ? 'Available' : 'Not configured'}
        </div></div>`;
        
        statusContent.innerHTML = apiStatus + statusContent.innerHTML;
    }

    handleLocationTypeChange(locationType) {
        const addressInput = document.getElementById('address');
        if (locationType === 'address') {
            addressInput.disabled = false;
            addressInput.required = true;
        } else {
            addressInput.disabled = true;
            addressInput.required = false;
            addressInput.value = '';
        }
    }

    handleFuelInputTypeChange(inputType) {
        const fuelValue = document.getElementById('fuelValue');
        const fuelHelp = document.getElementById('fuelHelp');
        
        if (inputType === 'percent') {
            fuelValue.max = '100';
            fuelValue.step = '1';
            fuelHelp.textContent = 'Enter percentage (0-100)';
        } else {
            fuelValue.max = '50';
            fuelValue.step = '0.1';
            fuelHelp.textContent = 'Enter gallons';
        }
        
        this.calculateFuelNeeded();
    }

    async calculateFuelNeeded() {
        const inputType = document.getElementById('fuelInputType').value;
        const value = parseFloat(document.getElementById('fuelValue').value);
        const tankSize = parseFloat(document.getElementById('tankSize').value);
        
        if (!value || !tankSize) return;
        
        try {
            const response = await fetch('/api/calculate-fuel', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    input_type: inputType,
                    value: value,
                    tank_size: tankSize
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.updateStatus(`Fuel needed: ${result.fuel_needed.toFixed(1)} gallons`, 'info');
            }
        } catch (error) {
            console.error('Error calculating fuel:', error);
        }
    }

    async handleFormSubmission() {
        this.showLoading();
        this.updateStatus('Processing your request...', 'info');
        
        try {
            const formData = await this.getFormData();
            
            // Show specific status for address geocoding
            if (formData.location_type === 'address') {
                this.updateStatus('Geocoding address...', 'info');
            }
            
            const response = await fetch('/api/search-stations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.displayResults(result);
                this.updateStatus(`Found ${result.filtered_stations} stations within range`, 'success');
            } else {
                this.updateStatus(`Error: ${result.error}`, 'error');
            }
        } catch (error) {
            this.updateStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async getFormData() {
        const locationType = document.getElementById('locationType').value;
        const data = {
            mpg: parseFloat(document.getElementById('mpg').value),
            tank_size: parseFloat(document.getElementById('tankSize').value),
            fuel_needed: parseFloat(document.getElementById('fuelValue').value),
            fuel_grade: document.getElementById('fuelGrade').value,
            location_type: locationType,
            radius_miles: parseFloat(document.getElementById('searchRadius').value)
        };
        
        if (locationType === 'address') {
            data.address = document.getElementById('address').value;
        } else if (locationType === 'current') {
            // Get current location using browser geolocation
            try {
                this.updateStatus('Getting your current location...', 'info');
                const position = await this.getCurrentPosition();
                data.latitude = position.coords.latitude;
                data.longitude = position.coords.longitude;
                this.updateStatus('Location acquired successfully!', 'success');
            } catch (error) {
                this.updateStatus('Could not get your location. Please use address instead.', 'error');
                throw error;
            }
        }
        
        return data;
    }

    getCurrentPosition() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Geolocation is not supported by this browser.'));
                return;
            }

            const options = {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 300000 // 5 minutes
            };

            navigator.geolocation.getCurrentPosition(resolve, reject, options);
        });
    }

    displayResults(result) {
        // Display stations
        const resultsSection = document.getElementById('resultsSection');
        const resultsContent = document.getElementById('resultsContent');
        
        if (result.stations && result.stations.length > 0) {
            let stationsHtml = `
                <div class="row mb-3">
                    <div class="col-md-6">
                        <strong>Total stations found:</strong> ${result.total_stations}
                    </div>
                    <div class="col-md-6">
                        <strong>Stations in range:</strong> ${result.filtered_stations}
                    </div>
                </div>
                <div class="row">
            `;
            
            result.stations.forEach((station, index) => {
                const cardClass = this.getStationCardClass(station, index);
                const isRecommended = index === 0; // First station is recommended
                
                // Get fuel needed and grade from the form
                const fuelNeeded = parseFloat(document.getElementById('fuelValue').value) || 0;
                const fuelGrade = document.getElementById('fuelGrade').value;
                
                // Get the correct price for the selected fuel grade
                const gasPrices = station.gas_prices || {};
                const selectedPrice = gasPrices[fuelGrade] || station.price_per_gallon;
                
                stationsHtml += `
                    <div class="col-lg-6 col-md-12 mb-3">
                        <div class="station-card ${cardClass} fade-in">
                            ${isRecommended ? '<div class="recommended-badge"><i class="fas fa-star me-1"></i>RECOMMENDED</div>' : ''}
                            <div class="row">
                                <div class="col-8">
                                    <h5 class="mb-2">
                                        <i class="fas fa-gas-pump me-2"></i>${station.name}
                                    </h5>
                                    ${station.address ? `<div class="station-address"><i class="fas fa-map-marker-alt me-2"></i>${station.address}</div>` : ''}
                                    <p class="mb-1">
                                        <i class="fas fa-route me-2"></i>
                                        ${station.distance_miles.toFixed(1)} miles away
                                    </p>
                                    <p class="mb-1">
                                        <i class="fas fa-clock me-2"></i>
                                        ${station.travel_time_minutes} min travel time
                                    </p>
                                    ${station.brand ? `<p class="mb-1"><i class="fas fa-tag me-2"></i>${station.brand}</p>` : ''}
                                    ${station.rating ? `<p class="mb-1"><i class="fas fa-star me-2"></i>${station.rating}/5.0</p>` : ''}
                                </div>
                                <div class="col-4 text-end">
                                    <div class="price-display">$${selectedPrice.toFixed(2)}</div>
                                    <div class="cost-breakdown">
                                        <div>Fuel: $${(selectedPrice * fuelNeeded).toFixed(2)}</div>
                                        <div>Travel: $${station.travel_cost.toFixed(2)}</div>
                                        <div><strong>Total: $${station.total_cost.toFixed(2)}</strong></div>
                                    </div>
                                    ${gasPrices['87'] && gasPrices['89'] && gasPrices['91'] ? `
                                        <div class="fuel-grades mt-2">
                                            <small class="text-muted">
                                                <div>87: $${gasPrices['87'].toFixed(2)}</div>
                                                <div>89: $${gasPrices['89'].toFixed(2)}</div>
                                                <div>91: $${gasPrices['91'].toFixed(2)}</div>
                                            </small>
                                        </div>
                                    ` : ''}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            stationsHtml += '</div>';
            resultsContent.innerHTML = stationsHtml;
            resultsSection.style.display = 'block';
            
            // Smooth scroll to results
            this.smoothScrollTo(resultsSection);
        } else {
            resultsContent.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
                    <h5>No gas stations found</h5>
                    <p>Try increasing your search radius or check your location settings.</p>
                </div>
            `;
            resultsSection.style.display = 'block';
        }
        
        // Display AI analysis
        if (result.analysis) {
            const analysisSection = document.getElementById('analysisSection');
            const analysisContent = document.getElementById('analysisContent');
            
            analysisContent.innerHTML = `
                <div class="analysis-content slide-in">
                    <div class="mb-3">
                        <i class="fas fa-robot me-2"></i>
                        <strong>AI Recommendation Analysis:</strong>
                    </div>
                    <div class="analysis-text">
                        ${result.analysis.replace(/\n/g, '<br>')}
                    </div>
                </div>
            `;
            analysisSection.style.display = 'block';
            
            // Smooth scroll to analysis after a short delay
            setTimeout(() => {
                this.smoothScrollTo(analysisSection);
            }, 500);
        }
    }

    getStationCardClass(station, index) {
        // Add special styling for top recommendations
        if (index === 0) return 'recommended';
        if (station.distance_miles <= 2) return 'closest';
        if (station.price_per_gallon <= 3.5) return 'lowest-price';
        return '';
    }

    smoothScrollTo(element) {
        element.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }

    updateStatus(message, type = 'info') {
        const statusContent = document.getElementById('statusContent');
        const statusHtml = `
            <div class="alert alert-${this.getAlertClass(type)} alert-dismissible fade show" role="alert">
                <span class="status-indicator ${type}"></span>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Add to the beginning of status content
        statusContent.innerHTML = statusHtml + statusContent.innerHTML;
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alerts = statusContent.querySelectorAll('.alert');
            if (alerts.length > 0) {
                alerts[0].remove();
            }
        }, 5000);
    }

    getAlertClass(type) {
        switch (type) {
            case 'success': return 'success';
            case 'error': return 'danger';
            case 'warning': return 'warning';
            default: return 'info';
        }
    }

    showLoading() {
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        modal.show();
    }

    hideLoading() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
        if (modal) {
            modal.hide();
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GasStationApp();
});

// Add some utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDistance(miles) {
    if (miles < 1) {
        return `${Math.round(miles * 5280)} feet`;
    }
    return `${miles.toFixed(1)} miles`;
}

function formatTime(minutes) {
    if (minutes < 60) {
        return `${minutes} min`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
} 