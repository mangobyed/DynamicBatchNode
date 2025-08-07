#!/bin/bash

# Setup script for Dynamic Image Batch Node repository
# This script helps you upload the files to GitHub

echo "🚀 Dynamic Image Batch Node - Repository Setup"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "__init__.py" ]; then
    echo "❌ Error: __init__.py not found. Please run this script from the node directory."
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo "📋 Files to upload:"

# List all files that should be uploaded
find . -type f \( \
    -name "*.py" -o \
    -name "*.js" -o \
    -name "*.md" -o \
    -name "LICENSE" -o \
    -name "*.txt" -o \
    -name "*.json" -o \
    -name ".gitignore" \
\) ! -path "./__pycache__/*" | sort

echo ""
echo "📝 Next steps to upload to GitHub:"
echo "1. Navigate to your repository: https://github.com/MoldenAI/DynamicBatchNode"
echo "2. Click 'uploading an existing file' or use git commands:"
echo ""
echo "   # Initialize git repository"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial release of Dynamic Image Batch Node'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/MoldenAI/DynamicBatchNode.git"
echo "   git push -u origin main"
echo ""
echo "3. Or upload files manually through GitHub web interface"
echo ""
echo "✅ Repository is ready for upload!"

# Make the script executable
chmod +x setup_repo.sh