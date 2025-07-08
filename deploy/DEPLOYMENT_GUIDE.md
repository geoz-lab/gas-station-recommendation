# Gas Station Recommendation App - Deployment Guide

## 🚀 Quick Deploy Options

### 1. Heroku (Recommended for beginners)

**Prerequisites:**
- Heroku account
- Git installed
- Heroku CLI installed

**Steps:**
```bash
# Clone the repository
git clone https://github.com/yourusername/gas-station-recommendation.git
cd gas-station-recommendation

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set GOOGLE_MAPS_API_KEY=your_google_maps_api_key
heroku config:set CLAUDE_API_KEY=your_claude_api_key

# Deploy
git push heroku main

# Open the app
heroku open
```

### 2. Railway

**Prerequisites:**
- Railway account
- GitHub repository

**Steps:**
1. Fork this repository to your GitHub account
2. Go to [Railway](https://railway.app/)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your forked repository
5. Add environment variables in Railway dashboard:
   - `GOOGLE_MAPS_API_KEY`
   - `CLAUDE_API_KEY`
6. Deploy!

### 3. Render

**Prerequisites:**
- Render account
- GitHub repository

**Steps:**
1. Fork this repository to your GitHub account
2. Go to [Render](https://render.com/)
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name:** gas-station-recommendation
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn web_app:app`
6. Add environment variables
7. Deploy!

### 4. Docker

**Prerequisites:**
- Docker installed

**Steps:**
```bash
# Clone the repository
git clone https://github.com/yourusername/gas-station-recommendation.git
cd gas-station-recommendation

# Create .env file with your API keys
cp .env.template .env
# Edit .env with your actual API keys

# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t gas-app .
docker run -p 8080:8080 --env-file .env gas-app
```

### 5. Local Development

**Prerequisites:**
- Python 3.7+
- pip

**Steps:**
```bash
# Clone the repository
git clone https://github.com/yourusername/gas-station-recommendation.git
cd gas-station-recommendation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.template .env
# Edit .env with your actual API keys

# Run the app
python web_app.py
```

## 🔑 API Keys Setup

### Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable these APIs:
   - Places API
   - Geocoding API
   - Maps JavaScript API
4. Create credentials (API Key)
5. Restrict the key to your domain for security

### Claude API Key
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Create an API key
4. Copy the key to your environment variables

## 🌐 Domain Setup

### Custom Domain (Optional)
After deploying, you can set up a custom domain:

**Heroku:**
```bash
heroku domains:add yourdomain.com
```

**Railway/Render:**
- Add custom domain in the dashboard
- Update DNS records as instructed

## 📊 Monitoring

### Health Check
The app includes a health check endpoint at `/health` that returns:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### Logs
Monitor your app logs:
- **Heroku:** `heroku logs --tail`
- **Railway:** View in dashboard
- **Render:** View in dashboard
- **Docker:** `docker logs container_name`

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change the port in `web_app.py`
   - Or kill the process using the port

2. **API Key Errors**
   - Verify API keys are correct
   - Check API quotas and billing
   - Ensure APIs are enabled

3. **Import Errors**
   - Install missing dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **CORS Issues**
   - The app is configured for local development
   - For production, update CORS settings in `web_app.py`

### Performance Optimization

1. **Enable Caching**
   - Add Redis for session storage
   - Implement API response caching

2. **Database Integration**
   - Add PostgreSQL for user data
   - Store search history and preferences

3. **CDN Setup**
   - Serve static files from CDN
   - Optimize images and assets

## 📞 Support

If you encounter issues:
1. Check the logs for error messages
2. Verify all environment variables are set
3. Test API keys independently
4. Check the deployment platform's status

## 🔄 Updates

To update your deployed app:
1. Pull the latest changes: `git pull origin main`
2. Deploy again using your platform's method
3. Monitor logs for any issues

---
For more help, check the main README.md or open an issue on GitHub.
