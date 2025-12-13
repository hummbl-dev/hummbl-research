#!/bin/bash
# Quick setup script for Vertex AI integration

set -e

echo "============================================================"
echo "VERTEX AI SETUP - QUICK START"
echo "============================================================"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found!"
    echo ""
    echo "Installing Google Cloud SDK..."
    
    # Check for Homebrew
    if command -v brew &> /dev/null; then
        echo "Using Homebrew to install..."
        brew install google-cloud-sdk
    else
        echo "Homebrew not found. Please install manually:"
        echo "  Visit: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
fi

echo "✅ gcloud CLI found"
echo ""

# Run Python setup script
echo "Running interactive setup script..."
python3 tools/setup_gcp_project.py

echo ""
echo "============================================================"
echo "Setup complete! Next steps:"
echo "============================================================"
echo "1. Test setup: python tools/vertex_ai_setup.py --test"
echo "2. Try enhanced SY19: python tools/sy19_vertex_ai.py 'test problem'"
echo "============================================================"
