#!/usr/bin/env python3
"""
Web Deployment Script for Gas Station Recommendation App
Prepares the app for deployment to various web hosting services
"""

import os
import sys
import shutil
import json
from pathlib import Path

class WebDeployer:
    def __init__(self):
        self.app_name = "gas-station-recommendation"
        self.deploy_dir = "deploy"
        
    def create_heroku_files(self):
        """Create files needed for Heroku deployment"""
        print("📦 Creating Heroku deployment files...")
        
        # Procfile for Heroku
        procfile_content = "web: gunicorn web_app:app"
        procfile_path = Path(self.deploy_dir) / "Procfile"
        procfile_path.parent.mkdir(exist_ok=True)
        
        with open(procfile_path, 'w') as f:
            f.write(procfile_content)
        print(f"  ✅ Created {procfile_path}")
        
        # Runtime.txt for Python version
        runtime_content = "python-3.11.0"
        runtime_path = Path(self.deploy_dir) / "runtime.txt"
        
        with open(runtime_path, 'w') as f:
            f.write(runtime_content)
        print(f"  ✅ Created {runtime_path}")
        
        # Requirements for Heroku
        requirements_content = '''flask>=2.0.0
requests>=2.25.0
anthropic>=0.7.0
geopy>=2.0.0
python-dotenv>=0.19.0
gunicorn>=20.1.0
'''
        req_path = Path(self.deploy_dir) / "requirements.txt"
        
        with open(req_path, 'w') as f:
            f.write(requirements_content)
        print(f"  ✅ Created {req_path}")
        
        return True
    
    def create_railway_files(self):
        """Create files needed for Railway deployment"""
        print("🚂 Creating Railway deployment files...")
        
        # Railway.json configuration
        railway_config = {
            "$schema": "https://railway.app/railway.schema.json",
            "build": {
                "builder": "NIXPACKS"
            },
            "deploy": {
                "startCommand": "gunicorn web_app:app",
                "healthcheckPath": "/health",
                "healthcheckTimeout": 100,
                "restartPolicyType": "ON_FAILURE",
                "restartPolicyMaxRetries": 10
            }
        }
        
        railway_path = Path(self.deploy_dir) / "railway.json"
        railway_path.parent.mkdir(exist_ok=True)
        
        with open(railway_path, 'w') as f:
            json.dump(railway_config, f, indent=2)
        print(f"  ✅ Created {railway_path}")
        
        return True
    
    def create_render_files(self):
        """Create files needed for Render deployment"""
        print("🎨 Creating Render deployment files...")
        
        # render.yaml configuration
        render_config = {
            "services": [
                {
                    "type": "web",
                    "name": self.app_name,
                    "env": "python",
                    "plan": "free",
                    "buildCommand": "pip install -r requirements.txt",
                    "startCommand": "gunicorn web_app:app",
                    "healthCheckPath": "/health",
                    "envVars": [
                        {
                            "key": "PYTHON_VERSION",
                            "value": "3.11.0"
                        }
                    ]
                }
            ]
        }
        
        render_path = Path(self.deploy_dir) / "render.yaml"
        render_path.parent.mkdir(exist_ok=True)
        
        with open(render_path, 'w') as f:
            json.dump(render_config, f, indent=2)
        print(f"  ✅ Created {render_path}")
        
        return True
    
    def create_docker_files(self):
        """Create Docker files for containerized deployment"""
        print("🐳 Creating Docker deployment files...")
        
        # Dockerfile
        dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=web_app.py
ENV FLASK_ENV=production
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD gunicorn --bind 0.0.0.0:8080 web_app:app
'''
        
        dockerfile_path = Path(self.deploy_dir) / "Dockerfile"
        dockerfile_path.parent.mkdir(exist_ok=True)
        
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        print(f"  ✅ Created {dockerfile_path}")
        
        # .dockerignore
        dockerignore_content = '''__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.env
.venv
venv/
ENV/
env/
.idea/
.vscode/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
'''
        
        dockerignore_path = Path(self.deploy_dir) / ".dockerignore"
        
        with open(dockerignore_path, 'w') as f:
            f.write(dockerignore_content)
        print(f"  ✅ Created {dockerignore_path}")
        
        # docker-compose.yml
        compose_content = '''version: '3.8'

services:
  gas-app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - FLASK_ENV=production
      - PORT=8080
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
'''
        
        compose_path = Path(self.deploy_dir) / "docker-compose.yml"
        
        with open(compose_path, 'w') as f:
            f.write(compose_content)
        print(f"  ✅ Created {compose_path}")
        
        return True
    
    def create_github_pages_files(self):
        """Create files for GitHub Pages static deployment"""
        print("📄 Creating GitHub Pages files...")
        
        # Note: GitHub Pages is for static sites, so we'll create a landing page
        # that explains how to deploy the full app
        
        index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gas Station Recommendation App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 0;
        }
        .feature-card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .deploy-section {
            background-color: #f8f9fa;
            padding: 80px 0;
        }
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container text-center">
            <h1 class="display-3 mb-4">
                <i class="fas fa-gas-pump me-3"></i>
                Gas Station Recommendation App
            </h1>
            <p class="lead mb-5">AI-powered gas station finder with real-time pricing and smart recommendations</p>
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <div class="text-center">
                                <i class="fas fa-map-marker-alt fa-3x mb-3"></i>
                                <h5>Find Nearby Stations</h5>
                                <p>Locate gas stations near you or any address</p>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3">
                            <div class="text-center">
                                <i class="fas fa-robot fa-3x mb-3"></i>
                                <h5>AI Recommendations</h5>
                                <p>Get smart suggestions based on cost and convenience</p>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3">
                            <div class="text-center">
                                <i class="fas fa-dollar-sign fa-3x mb-3"></i>
                                <h5>Price Comparison</h5>
                                <p>Compare prices across different fuel grades</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="py-5">
        <div class="container">
            <h2 class="text-center mb-5">Key Features</h2>
            <div class="row">
                <div class="col-lg-4 mb-4">
                    <div class="card feature-card h-100">
                        <div class="card-body text-center">
                            <i class="fas fa-location-arrow fa-3x text-primary mb-3"></i>
                            <h5 class="card-title">Current Location</h5>
                            <p class="card-text">Use your GPS location or enter any address to find nearby gas stations.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card feature-card h-100">
                        <div class="card-body text-center">
                            <i class="fas fa-gas-pump fa-3x text-success mb-3"></i>
                            <h5 class="card-title">Multiple Fuel Grades</h5>
                            <p class="card-text">Compare prices for Regular (87), Mid-Grade (89), and Premium (91) fuel.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card feature-card h-100">
                        <div class="card-body text-center">
                            <i class="fas fa-calculator fa-3x text-warning mb-3"></i>
                            <h5 class="card-title">Cost Analysis</h5>
                            <p class="card-text">Calculate total costs including fuel and travel expenses.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Deployment Section -->
    <section class="deploy-section">
        <div class="container">
            <h2 class="text-center mb-5">Deploy Your Own Instance</h2>
            <div class="row">
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-header bg-primary text-white">
                            <h5><i class="fas fa-rocket me-2"></i>Quick Deploy</h5>
                        </div>
                        <div class="card-body">
                            <h6>Deploy to Heroku:</h6>
                            <pre><code>git clone https://github.com/yourusername/gas-station-recommendation.git
cd gas-station-recommendation
heroku create your-app-name
heroku config:set GOOGLE_MAPS_API_KEY=your_key
heroku config:set CLAUDE_API_KEY=your_key
git push heroku main</code></pre>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-header bg-success text-white">
                            <h5><i class="fas fa-docker me-2"></i>Docker Deploy</h5>
                        </div>
                        <div class="card-body">
                            <h6>Deploy with Docker:</h6>
                            <pre><code>git clone https://github.com/yourusername/gas-station-recommendation.git
cd gas-station-recommendation
docker build -t gas-app .
docker run -p 8080:8080 gas-app</code></pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Setup Section -->
    <section class="py-5">
        <div class="container">
            <h2 class="text-center mb-5">Setup Requirements</h2>
            <div class="row">
                <div class="col-md-6">
                    <h5><i class="fas fa-key me-2"></i>API Keys Required</h5>
                    <ul class="list-unstyled">
                        <li><strong>Google Maps API:</strong> For gas station locations and geocoding</li>
                        <li><strong>Claude API:</strong> For AI-powered recommendations</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h5><i class="fas fa-code me-2"></i>Technologies Used</h5>
                    <ul class="list-unstyled">
                        <li><strong>Backend:</strong> Python Flask</li>
                        <li><strong>Frontend:</strong> HTML, CSS, JavaScript</li>
                        <li><strong>APIs:</strong> Google Maps, Claude AI</li>
                        <li><strong>Styling:</strong> Bootstrap 5</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4">
        <div class="container text-center">
            <p>&copy; 2024 Gas Station Recommendation App. Built with ❤️ using Python and Flask.</p>
            <p>
                <a href="https://github.com/yourusername/gas-station-recommendation" class="text-white me-3">
                    <i class="fab fa-github"></i> GitHub
                </a>
                <a href="#" class="text-white">
                    <i class="fas fa-book"></i> Documentation
                </a>
            </p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
        
        pages_path = Path(self.deploy_dir) / "github-pages"
        pages_path.mkdir(exist_ok=True)
        
        index_path = pages_path / "index.html"
        with open(index_path, 'w') as f:
            f.write(index_html)
        print(f"  ✅ Created {index_path}")
        
        return True
    
    def create_env_template(self):
        """Create environment variables template"""
        print("🔧 Creating environment template...")
        
        env_template = '''# Gas Station Recommendation App Environment Variables
# Copy this file to .env and fill in your actual API keys

# Google Maps API Key (required for gas station locations)
# Get from: https://console.cloud.google.com/
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Claude API Key (required for AI recommendations)
# Get from: https://console.anthropic.com/
CLAUDE_API_KEY=your_claude_api_key_here

# Flask Configuration
FLASK_ENV=production
FLASK_APP=web_app.py
PORT=8080

# Optional: Database URL (if using a database)
# DATABASE_URL=postgresql://user:pass@host:port/db

# Optional: Secret key for sessions
SECRET_KEY=your_secret_key_here
'''
        
        env_path = Path(self.deploy_dir) / ".env.template"
        env_path.parent.mkdir(exist_ok=True)
        
        with open(env_path, 'w') as f:
            f.write(env_template)
        print(f"  ✅ Created {env_path}")
        
        return True
    
    def create_deployment_guide(self):
        """Create comprehensive deployment guide"""
        print("📚 Creating deployment guide...")
        
        guide_content = '''# Gas Station Recommendation App - Deployment Guide

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
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

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
'''
        
        guide_path = Path(self.deploy_dir) / "DEPLOYMENT_GUIDE.md"
        guide_path.parent.mkdir(exist_ok=True)
        
        with open(guide_path, 'w') as f:
            f.write(guide_content)
        print(f"  ✅ Created {guide_path}")
        
        return True
    
    def copy_app_files(self):
        """Copy the app files to deployment directory"""
        app_dir = Path("gas_recommendation_app")
        deploy_app_dir = Path(self.deploy_dir) / "gas_recommendation_app"
        
        if not app_dir.exists():
            print(f"❌ App directory not found: {app_dir}")
            return False
        
        # Create deploy directory
        deploy_app_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all app files
        print(f"📁 Copying app files to {deploy_app_dir}...")
        
        # Files to copy
        files_to_copy = [
            "web_app.py",
            "config.py",
            "main.py",
            "requirements.txt",
            "README.md"
        ]
        
        # Directories to copy
        dirs_to_copy = [
            "services",
            "models", 
            "utils",
            "static",
            "templates"
        ]
        
        # Copy files
        for file_name in files_to_copy:
            src = app_dir / file_name
            dst = deploy_app_dir / file_name
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  ✅ Copied {file_name}")
        
        # Copy directories
        for dir_name in dirs_to_copy:
            src = app_dir / dir_name
            dst = deploy_app_dir / dir_name
            if src.exists():
                shutil.copytree(src, dst, dirs_exist_ok=True)
                print(f"  ✅ Copied {dir_name}/")
        
        return True
    
    def deploy(self, platforms=None):
        """Create deployment files for specified platforms"""
        if platforms is None:
            platforms = ['heroku', 'railway', 'render', 'docker', 'github-pages']
        
        print("🚀 Creating Web Deployment Package...")
        print("=" * 60)
        
        # Create deployment directory
        deploy_path = Path(self.deploy_dir)
        deploy_path.mkdir(exist_ok=True)
        
        # Copy app files
        if not self.copy_app_files():
            return False
        
        # Create platform-specific files
        if 'heroku' in platforms:
            self.create_heroku_files()
        
        if 'railway' in platforms:
            self.create_railway_files()
        
        if 'render' in platforms:
            self.create_render_files()
        
        if 'docker' in platforms:
            self.create_docker_files()
        
        if 'github-pages' in platforms:
            self.create_github_pages_files()
        
        # Create common files
        self.create_env_template()
        self.create_deployment_guide()
        
        print("\n🎉 Web deployment package created successfully!")
        print(f"📁 Deployment files: {Path.cwd() / self.deploy_dir}")
        print("\n🚀 Next steps:")
        print("1. Choose your deployment platform")
        print("2. Follow the DEPLOYMENT_GUIDE.md instructions")
        print("3. Set up your API keys")
        print("4. Deploy!")
        
        return True

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create web deployment package')
    parser.add_argument('--platforms', nargs='+', 
                       choices=['heroku', 'railway', 'render', 'docker', 'github-pages'],
                       default=['heroku', 'railway', 'render', 'docker', 'github-pages'],
                       help='Platforms to create deployment files for')
    
    args = parser.parse_args()
    
    deployer = WebDeployer()
    success = deployer.deploy(args.platforms)
    
    if success:
        print("\n✅ Web deployment package created successfully!")
    else:
        print("\n❌ Web deployment package creation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 