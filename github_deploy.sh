#!/bin/bash

echo "🐙 Deploying to GitHub..."
echo "============================================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Please run 'git init' first."
    exit 1
fi

# Get repository name from user
echo "📝 Enter your GitHub username:"
read -r github_username

echo "📝 Enter your repository name (or press Enter for 'gas-station-recommendation'):"
read -r repo_name
repo_name=${repo_name:-gas-station-recommendation}

# Set up remote repository
echo "🔗 Setting up remote repository..."
git remote add origin "https://github.com/$github_username/$repo_name.git"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🌐 Your repository is now available at:"
echo "   https://github.com/$github_username/$repo_name"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://github.com/$github_username/$repo_name"
echo "2. Set up GitHub Pages (optional):"
echo "   - Go to Settings → Pages"
echo "   - Set source to 'gh-pages' branch"
echo "   - Your site will be at: https://$github_username.github.io/$repo_name"
echo ""
echo "3. Set up deployment secrets (for GitHub Actions):"
echo "   - Go to Settings → Secrets and variables → Actions"
echo "   - Add these secrets:"
echo "     - GOOGLE_MAPS_API_KEY: $GOOGLE_MAPS_API_KEY"
echo "     - CLAUDE_API_KEY: $CLAUDE_API_KEY"
echo "     - RAILWAY_TOKEN: (get from Railway dashboard)"
echo "     - RENDER_TOKEN: (get from Render dashboard)"
echo ""
echo "4. Deploy to cloud platforms:"
echo "   - Railway: Connect your GitHub repo to Railway"
echo "   - Render: Connect your GitHub repo to Render"
echo "   - Docker: Use the Docker deployment scripts"
echo ""
echo "🎉 Your Gas Station Recommendation App is now on GitHub!" 