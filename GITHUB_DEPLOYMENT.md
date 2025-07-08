# 🐙 GitHub Deployment Guide

Your Gas Station Recommendation App is ready to be deployed to GitHub! Here's how to get it online.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated deployment script
./github_deploy.sh
```

This script will:
- Ask for your GitHub username
- Set up the remote repository
- Push your code to GitHub
- Provide next steps

### Option 2: Manual Setup

1. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Name it: `gas-station-recommendation`
   - Make it public or private
   - Don't initialize with README (we already have one)

2. **Connect your local repository**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/gas-station-recommendation.git
   git branch -M main
   git push -u origin main
   ```

## 🌐 GitHub Pages Setup

### Static Landing Page

1. **Create gh-pages branch**:
   ```bash
   git checkout -b gh-pages
   cp -r deploy/github-pages/* .
   git add .
   git commit -m "Add GitHub Pages landing page"
   git push origin gh-pages
   ```

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: gh-pages
   - Save

3. **Your site will be available at**:
   `https://YOUR_USERNAME.github.io/gas-station-recommendation`

## 🔧 GitHub Actions Setup

### Automatic Deployment

Your repository includes GitHub Actions workflows for:
- ✅ Automated testing
- 🚀 Railway deployment
- 🎨 Render deployment
- 🐳 Docker image building

### Set up Secrets

1. **Go to your repository**:
   - Settings → Secrets and variables → Actions

2. **Add these secrets**:
   ```
   GOOGLE_MAPS_API_KEY=AIzaSyDjNxcwyJWryuErYs9dD6VPuyqPKmFgjjk
   CLAUDE_API_KEY=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
   RAILWAY_TOKEN=(get from Railway dashboard)
   RENDER_TOKEN=(get from Render dashboard)
   DOCKER_USERNAME=(your Docker Hub username)
   DOCKER_PASSWORD=(your Docker Hub password)
   ```

## 🚀 Cloud Deployment Options

### Railway (Recommended)

1. **Go to Railway**: https://railway.app
2. **Sign up with GitHub**
3. **New Project → Deploy from GitHub repo**
4. **Select your repository**
5. **Add environment variables**:
   ```
   GOOGLE_MAPS_API_KEY=AIzaSyDjNxcwyJWryuErYs9dD6VPuyqPKmFgjjk
   CLAUDE_API_KEY=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
   ```

### Render

1. **Go to Render**: https://render.com
2. **Sign up with GitHub**
3. **New → Web Service**
4. **Connect your repository**
5. **Configure**:
   - Name: `gas-station-reco`
   - Environment: `Python`
   - Build Command: `pip install -r gas_recommendation_app/requirements.txt`
   - Start Command: `cd gas_recommendation_app && gunicorn web_app:app`
6. **Add environment variables** (same as above)

### Docker Hub

1. **Build and push Docker image**:
   ```bash
   cd deploy
   docker build -t YOUR_USERNAME/gas-station-reco .
   docker push YOUR_USERNAME/gas-station-reco
   ```

2. **Deploy anywhere**:
   ```bash
   docker run -p 8080:8080 \
     -e GOOGLE_MAPS_API_KEY=your_key \
     -e CLAUDE_API_KEY=your_key \
     YOUR_USERNAME/gas-station-reco
   ```

## 📊 Repository Structure

```
gas-station-recommendation/
├── .github/workflows/          # GitHub Actions
├── gas_recommendation_app/     # Main application
├── deploy/                     # Deployment configs
├── dist/                       # Packaged app
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
└── github_deploy.sh           # Deployment script
```

## 🔑 Your API Keys

Your API keys are already configured in the deployment scripts:

- **Google Maps API Key**: `AIzaSyDjNxcwyJWryuErYs9dD6VPuyqPKmFgjjk`
- **Claude API Key**: `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`

## 🎯 What You Get

### GitHub Repository
- ✅ Complete source code
- ✅ Comprehensive documentation
- ✅ GitHub Actions workflows
- ✅ Multiple deployment options

### Live Applications
- 🌐 **Web App**: Deploy to Railway/Render for full functionality
- 📄 **Landing Page**: GitHub Pages for project showcase
- 🐳 **Docker Image**: Deploy anywhere with Docker

### Features Available
- 🚗 Find nearby gas stations
- 💰 Compare fuel prices (87, 89, 91)
- 🤖 AI-powered recommendations
- 📍 GPS and address geocoding
- 💡 Cost analysis with travel expenses

## 🚀 Next Steps

1. **Run the deployment script**:
   ```bash
   ./github_deploy.sh
   ```

2. **Choose your deployment platform**:
   - Railway (easiest)
   - Render (popular)
   - Docker (portable)

3. **Share your app**:
   - Web URL for users
   - GitHub repository for developers
   - Docker image for deployment

## 🎉 Success!

Once deployed, your Gas Station Recommendation App will be:
- 📱 Accessible from anywhere
- 🔄 Automatically updated
- 📊 Monitored and maintained
- 🌍 Available to users worldwide

---

**Need help?** Check the main README.md for detailed instructions! 