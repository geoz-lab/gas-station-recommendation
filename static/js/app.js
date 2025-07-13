// Gas Station Recommendation App - Frontend JavaScript

class GasStationApp {
    constructor() {
        this.map = null;
        this.markers = [];
        this.userLocation = null;
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

    initializeMap() {
        // Wait for Google Maps API to load
        if (typeof google === 'undefined' || !google.maps) {
            setTimeout(() => this.initializeMap(), 100);
            return;
        }

        const mapElement = document.getElementById('map');
        if (!mapElement) return;

        // Check if Google Maps API key is available
        if (!window.googleMapsApiKey) {
            this.showMapFallback();
            return;
        }

        // Initialize map with default location (San Francisco)
        this.map = new google.maps.Map(mapElement, {
            center: { lat: 37.7749, lng: -122.4194 },
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false, // Disable map type control
            streetViewControl: true,
            fullscreenControl: true,
            zoomControl: true,
            scaleControl: true
        });

        // Show map controls
        this.showMapControls();
    }

    showMapFallback() {
        const mapElement = document.getElementById('map');
        if (mapElement) {
            mapElement.innerHTML = `
                <div class="map-loading">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div>
                        <h6>Google Maps API Key Required</h6>
                        <p class="mb-0">Please configure your Google Maps API key to view the interactive map.</p>
                        <small class="text-muted">You can still view gas station recommendations in the list below.</small>
                    </div>
                </div>
            `;
        }
    }

    resetMapView() {
        if (this.map && this.userLocation) {
            this.map.setCenter(this.userLocation);
            this.map.setZoom(13);
        }
    }



    showMapControls() {
        const mapControls = document.getElementById('mapControls');
        if (mapControls) {
            mapControls.style.display = 'block';
        }
    }

    showMapLegend() {
        const mapLegend = document.getElementById('mapLegend');
        if (mapLegend) {
            mapLegend.style.display = 'block';
        }
    }

    clearMap() {
        // Clear existing markers
        this.markers.forEach(marker => marker.setMap(null));
        this.markers = [];
    }

    addUserLocationMarker(lat, lng, address = null) {
        if (!this.map) return;

        const position = { lat: parseFloat(lat), lng: parseFloat(lng) };
        
        // Center map on user location
        this.map.setCenter(position);
        this.map.setZoom(13);

        // Add user location marker
        const userMarker = new google.maps.Marker({
            position: position,
            map: this.map,
            title: address || 'Your Location',
            icon: {
                url: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                scaledSize: new google.maps.Size(32, 32)
            }
        });

        // Add info window for user location
        const infoWindow = new google.maps.InfoWindow({
            content: `<div style="padding: 10px;">
                <h6><i class="fas fa-map-marker-alt text-primary"></i> Your Location</h6>
                ${address ? `<p class="mb-0">${address}</p>` : ''}
            </div>`
        });

        userMarker.addListener('click', () => {
            infoWindow.open(this.map, userMarker);
        });

        this.markers.push(userMarker);
        this.userLocation = position;
    }

    addStationMarkers(stations, aiRecommendations = []) {
        if (!this.map || !stations) return;

        // Ensure map is fully loaded
        if (!this.map.getCenter) {
            setTimeout(() => this.addStationMarkers(stations, aiRecommendations), 100);
            return;
        }

        stations.forEach((station, index) => {
            const position = { 
                lat: parseFloat(station.location?.latitude || station.latitude), 
                lng: parseFloat(station.location?.longitude || station.longitude) 
            };

            // Check if this station is AI recommended (only top 5)
            const isAIRecommended = index < 5 && aiRecommendations.some(rec => 
                station.name.toLowerCase().includes(rec.toLowerCase()) ||
                rec.toLowerCase().includes(station.name.toLowerCase())
            );

            // Get fuel grade and price for marker
            const markerFuelGrade = document.getElementById('fuelGrade').value;
            const markerGasPrices = station.gas_prices || {};
            const markerSelectedPrice = markerGasPrices[markerFuelGrade] || station.price_per_gallon;

            // Create custom marker with price
            const marker = new google.maps.Marker({
                position: position,
                map: this.map,
                title: isAIRecommended ? ` RECOMMENDED  Gas Station ($${markerSelectedPrice.toFixed(2)})` : ` Gas Station ($${markerSelectedPrice.toFixed(2)})`,
                label: {
                    text: `$${markerSelectedPrice.toFixed(2)}`,
                    color: isAIRecommended ? 'white' : 'black',
                    fontSize: '14px',
                    fontWeight: 'bold'
                },
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    fillColor: isAIRecommended ? '#FF4444' : '#4CAF50',
                    fillOpacity: 0.8,
                    strokeColor: isAIRecommended ? '#CC0000' : '#2E7D32',
                    strokeWeight: 2,
                    scale: isAIRecommended ? 16 : 14
                }
            });

            // Create info window content
            const fuelGrade = document.getElementById('fuelGrade').value;
            const gasPrices = station.gas_prices || {};
            const selectedPrice = gasPrices[fuelGrade] || station.price_per_gallon;
            
            const infoContent = `
                <div style="padding: 10px; min-width: 200px;">
                    <h6><i class="fas fa-gas-pump text-success"></i> ${station.name}</h6>
                    <p class="mb-1"><strong>Price:</strong> $${selectedPrice.toFixed(2)}/gallon</p>
                    <p class="mb-1"><strong>Distance:</strong> ${formatDistance(station.distance_miles)}</p>
                    <p class="mb-1"><strong>Travel Time:</strong> ${formatTime(station.travel_time_minutes)}</p>
                    <p class="mb-0"><strong>Address:</strong> ${station.location?.address || station.address || 'Address not available'}</p>
                    ${isAIRecommended ? '<div class="mt-2"><span class="badge bg-warning text-dark"><i class="fas fa-star"></i> RECOMMENDED</span></div>' : ''}
                </div>
            `;

            const infoWindow = new google.maps.InfoWindow({
                content: infoContent
            });

            marker.addListener('click', () => {
                infoWindow.open(this.map, marker);
            });

            this.markers.push(marker);
        });

        // Fit bounds to show all markers
        if (this.markers.length > 0) {
            const bounds = new google.maps.LatLngBounds();
            this.markers.forEach(marker => {
                bounds.extend(marker.getPosition());
            });
            this.map.fitBounds(bounds);
            
            // Add some padding to the bounds
            const listener = google.maps.event.addListener(this.map, 'idle', () => {
                if (this.map.getZoom() > 15) {
                    this.map.setZoom(15);
                }
                google.maps.event.removeListener(listener);
            });
        }
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
            Claude.ai: ${config.has_claude ? 'Available' : 'Not configured'}
        </div>`;
        
        apiStatus += `<div class="mb-2">
            <span class="status-indicator ${config.has_openai ? 'success' : 'error'}"></span>
            ChatGPT: ${config.has_openai ? 'Available' : 'Not configured'}
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
        // Initialize map if not already done
        if (!this.map) {
            this.initializeMap();
        }
        
        // Clear existing markers
        this.clearMap();
        
        // Extract AI recommendations first
        const aiRecommendations = this.extractAIRecommendations(result.analysis);
        
        // Sort stations by AI recommendations, cost, and rating
        let sortedStations = [...result.stations];
        sortedStations.sort((a, b) => {
            // First priority: AI recommendations
            const aIsRecommended = aiRecommendations.some(rec => 
                a.name.toLowerCase().includes(rec.toLowerCase()) ||
                rec.toLowerCase().includes(a.name.toLowerCase())
            );
            const bIsRecommended = aiRecommendations.some(rec => 
                b.name.toLowerCase().includes(rec.toLowerCase()) ||
                rec.toLowerCase().includes(b.name.toLowerCase())
            );
            
            if (aIsRecommended && !bIsRecommended) return -1;
            if (!aIsRecommended && bIsRecommended) return 1;
            
            // Second priority: Total cost
            const costDiff = Math.abs(a.total_cost - b.total_cost);
            if (costDiff > 1.0) {
                // If cost difference is more than $1, sort by cost
                return a.total_cost - b.total_cost;
            } else {
                // If cost difference is less than $1, sort by rating
                const aRating = a.rating || 0;
                const bRating = b.rating || 0;
                return bRating - aRating; // Higher rating first
            }
        });
        
        // Use all stations for display
        const displayStations = sortedStations;
        
        // Add user location marker
        if (result.location) {
            const [lat, lng] = result.location;
            const address = document.getElementById('locationType').value === 'address' ? 
                document.getElementById('address').value : null;
            this.addUserLocationMarker(lat, lng, address);
        }
        
        // Add station markers with a small delay to ensure map is ready
        if (displayStations.length > 0) {
            setTimeout(() => {
                this.addStationMarkers(displayStations, aiRecommendations);
            }, 500);
        }
        
        // Show map section
        const mapSection = document.getElementById('mapSection');
        mapSection.style.display = 'block';
        
        // Show map legend if stations are found
        if (displayStations.length > 0) {
            this.showMapLegend();
        }
        
        // Display stations
        const resultsSection = document.getElementById('resultsSection');
        const resultsContent = document.getElementById('resultsContent');
        
        if (displayStations.length > 0) {
            let stationsHtml = `
                <div class="row">
            `;
            
            displayStations.forEach((station, index) => {
                const cardClass = this.getStationCardClass(station, index, aiRecommendations);
                const isAIRecommended = aiRecommendations.some(rec => 
                    station.name.toLowerCase().includes(rec.toLowerCase()) ||
                    rec.toLowerCase().includes(station.name.toLowerCase())
                );
                const isRecommended = index === 0; // Only mark the top station as recommended
                
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
                                    ${(station.location?.address || station.address) ? `<div class="station-address"><i class="fas fa-map-marker-alt me-2"></i>${station.location?.address || station.address}</div>` : ''}
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
            
            // Smooth scroll to results (not analysis)
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
        
        // Display AI analysis (but don't auto-scroll to it)
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
                        ${this.formatMarkdown(result.analysis)}
                    </div>
                </div>
            `;
            analysisSection.style.display = 'block';
        }
    }

    formatMarkdown(text) {
        if (!text) return '';
        
        // Convert markdown to HTML
        let html = text
            // Convert **text** to <strong>text</strong>
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Convert *text* to <em>text</em>
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // Convert line breaks
            .replace(/\n/g, '<br>');
        
        // Handle tables
        const lines = text.split('\n');
        let inTable = false;
        let tableHtml = '';
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            
            if (line.includes('|') && line.trim().length > 0) {
                if (!inTable) {
                    inTable = true;
                    tableHtml = '<div class="table-responsive"><table class="table table-striped table-sm">';
                }
                
                // Check if this is a header separator line
                if (line.match(/^\s*\|[\s\-:|]+\|\s*$/)) {
                    continue; // Skip separator lines
                }
                
                const cells = line.split('|').map(cell => cell.trim()).filter(cell => cell.length > 0);
                const isHeader = i === 0 || (i > 0 && !lines[i-1].includes('|'));
                
                if (isHeader) {
                    tableHtml += '<thead><tr>';
                    cells.forEach(cell => {
                        tableHtml += `<th>${cell}</th>`;
                    });
                    tableHtml += '</tr></thead><tbody>';
                } else {
                    tableHtml += '<tr>';
                    cells.forEach(cell => {
                        tableHtml += `<td>${cell}</td>`;
                    });
                    tableHtml += '</tr>';
                }
            } else if (inTable) {
                inTable = false;
                tableHtml += '</tbody></table></div>';
                html = html.replace(line, tableHtml);
                tableHtml = '';
            }
        }
        
        if (inTable) {
            tableHtml += '</tbody></table></div>';
            html = html.replace(lines[lines.length - 1], tableHtml);
        }
        
        return html;
    }

    extractAIRecommendations(analysis) {
        if (!analysis) return [];
        
        // Try to extract station names from AI analysis
        const recommendations = [];
        const lines = analysis.split('\n');
        
        for (const line of lines) {
            // Look for patterns like "1. Station Name" or "Station Name -" or "Station Name:"
            const match = line.match(/^\d+\.\s*(.+?)(?:\s*[-:]\s*|$)/i) || 
                         line.match(/^(.+?)\s*[-:]\s*/i) ||
                         line.match(/^(.+?)\s*\(/i) ||
                         line.match(/\|\s*\d+\s*\|\s*(.+?)\s*\|\s*\$/i); // Match table format
            
            if (match) {
                const stationName = match[1].trim();
                if (stationName && stationName.length > 2 && !stationName.includes('Rank') && !stationName.includes('Name')) {
                    recommendations.push(stationName);
                }
            }
        }
        
        return recommendations.slice(0, 5); // Return top 5
    }

    getStationCardClass(station, index, aiRecommendations = []) {
        // Add special styling only for the top station
        if (index === 0) return 'recommended';
        return 'regular'; // Regular styling for all other stations
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
    window.app = new GasStationApp();
    
    // Initialize map after a short delay to ensure Google Maps API is loaded
    setTimeout(() => {
        window.app.initializeMap();
    }, 1000);
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