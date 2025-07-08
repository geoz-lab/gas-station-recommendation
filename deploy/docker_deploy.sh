#!/bin/bash

echo "🐳 Deploying with Docker..."
echo "============================================================"

# Create .env file with your API keys
echo "🔧 Creating .env file..."
cat > .env << EOF
GOOGLE_MAPS_API_KEY=AIzaSyDjNxcwyJWryuErYs9dD6VPuyqPKmFgjjk
CLAUDE_API_KEY=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
FLASK_ENV=production
PORT=8080
EOF

echo "✅ Created .env file"

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t gas-station-reco .

# Run container
echo "🚀 Starting container..."
docker run -d -p 8080:8080 --env-file .env --name gas-app gas-station-reco

echo "✅ Deployment complete!"
echo "🌐 Your app is available at: http://localhost:8080"
echo ""
echo "📋 Useful commands:"
echo "  Stop app: docker stop gas-app"
echo "  Start app: docker start gas-app"
echo "  View logs: docker logs gas-app"
echo "  Remove app: docker rm gas-app" 