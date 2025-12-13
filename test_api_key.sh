#!/bin/bash
# Quick test script for API key setup

echo "============================================================"
echo "TESTING API KEY SETUP"
echo "============================================================"

# Check if API key is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ GOOGLE_API_KEY not set"
    echo ""
    echo "Set it with:"
    echo "  export GOOGLE_API_KEY='your-key-here'"
    exit 1
fi

echo "✅ GOOGLE_API_KEY is set"
echo "   Key starts with: ${GOOGLE_API_KEY:0:10}..."
echo ""

# Test with Python
echo "Testing API key with Google Generative AI SDK..."
python3 << 'PYTHON_EOF'
import os
import sys

try:
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        sys.exit(1)
    
    # Configure
    genai.configure(api_key=api_key)
    
    # Test with a simple model
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(
        "Say 'API key test successful' if you can read this.",
        generation_config={"max_output_tokens": 20, "temperature": 0.1}
    )
    
    print("✅ API Key Test: SUCCESS")
    print(f"   Response: {response.text.strip()}")
    print("")
    print("🎉 Your API key is working!")
    
except ImportError:
    print("❌ google-generativeai not installed")
    print("   Install with: pip install google-generativeai")
    sys.exit(1)
except Exception as e:
    print(f"❌ API Key Test: FAILED")
    print(f"   Error: {e}")
    sys.exit(1)
PYTHON_EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "✅ API KEY SETUP COMPLETE!"
    echo "============================================================"
    echo ""
    echo "You can now use SY19 with API key:"
    echo "  python tools/sy19_vertex_ai.py 'problem description' --use-api-key"
    echo ""
else
    echo ""
    echo "============================================================"
    echo "❌ TEST FAILED"
    echo "============================================================"
    exit 1
fi

