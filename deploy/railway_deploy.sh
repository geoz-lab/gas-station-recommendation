#!/bin/bash

echo "🚂 Deploying to Railway..."
echo "============================================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Initialize Railway project
echo "🚀 Initializing Railway project..."
railway init

# Set environment variables
echo "🔧 Setting environment variables..."
railway variables set GOOGLE_MAPS_API_KEY=AIzaSyDjNxcwyJWryuErYs9dD6VPuyqPKmFgjjk
railway variables set CLAUDE_API_KEY=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

# Deploy
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your app will be available at the URL shown above"
echo "📊 Monitor your app at: https://railway.app/dashboard" 