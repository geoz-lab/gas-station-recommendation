#!/bin/bash

echo "📄 Deploying to GitHub Pages..."
echo "============================================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please run this from the deploy directory."
    exit 1
fi

# Create gh-pages branch
echo "🌿 Creating gh-pages branch..."
git checkout -b gh-pages

# Copy static files
echo "📁 Copying static files..."
cp -r github-pages/* .

# Add and commit
echo "📝 Committing changes..."
git add .
git commit -m "Deploy to GitHub Pages"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin gh-pages

# Switch back to main
git checkout main

echo "✅ Deployment complete!"
echo "🌐 Your landing page will be available at:"
echo "   https://[your-username].github.io/[your-repo-name]"
echo ""
echo "📋 Next steps:"
echo "1. Go to your GitHub repository"
echo "2. Go to Settings → Pages"
echo "3. Set source to 'gh-pages' branch"
echo "4. Your site will be published in a few minutes" 