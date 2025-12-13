#!/bin/bash
# Helper script to set API key

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

if [ $# -eq 0 ]; then
    # Interactive mode
    echo "============================================================"
    echo "SET API KEY HELPER"
    echo "============================================================"
    echo ""
    echo "Usage:"
    echo "  ./set_api_key.sh 'your-api-key-here'"
    echo ""
    echo "Or run interactively (will prompt for key):"
    echo "  ./set_api_key.sh"
    echo ""
    read -p "Paste your API key (starts with 'AIza'): " -s API_KEY
    echo ""
else
    # Non-interactive mode - key provided as argument
    API_KEY="$1"
fi

if [ -z "$API_KEY" ]; then
    echo "❌ No API key provided"
    exit 1
fi

# Validate format
if [[ ! "$API_KEY" =~ ^AIza ]]; then
    echo "⚠️  Warning: API key doesn't start with 'AIza'"
    echo "   Are you sure this is correct? (y/n)"
    if [ $# -eq 0 ]; then
        read -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Cancelled."
            exit 1
        fi
    fi
fi

# Set for current session
export GOOGLE_API_KEY="$API_KEY"
echo "✅ API key set for current session"

# Ask if they want to save permanently (only in interactive mode)
if [ $# -eq 0 ]; then
    echo ""
    read -p "Save to ~/.zshrc for future sessions? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Remove old entry if exists
        if grep -q "GOOGLE_API_KEY" ~/.zshrc 2>/dev/null; then
            sed -i.bak '/export GOOGLE_API_KEY/d' ~/.zshrc
        fi
        
        # Add new entry
        echo "export GOOGLE_API_KEY=\"$API_KEY\"" >> ~/.zshrc
        echo "✅ API key saved to ~/.zshrc"
        echo "   (Backup saved as ~/.zshrc.bak)"
    fi
fi

echo ""
echo "============================================================"
echo "API KEY SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "Testing API key..."
echo ""

# Quick test
python3 << 'PYTHON_EOF'
import os
import sys

try:
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(
        "Say 'test successful' if you can read this.",
        generation_config={"max_output_tokens": 10, "temperature": 0.1}
    )
    
    print("✅ API Key Test: SUCCESS")
    print(f"   Response: {response.text.strip()}")
    print("")
    print("🎉 Your API key is working! You can now use:")
    print("   python tools/sy19_vertex_ai.py 'problem' --use-api-key")
    
except ImportError:
    print("❌ google-generativeai not installed")
    print("   Install with: pip install google-generativeai")
    sys.exit(1)
except Exception as e:
    print(f"❌ API Key Test: FAILED")
    print(f"   Error: {e}")
    print("")
    print("Please check:")
    print("  1. API key is correct")
    print("  2. Generative Language API is enabled")
    print("  3. API key has proper permissions")
    sys.exit(1)
PYTHON_EOF
