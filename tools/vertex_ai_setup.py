#!/usr/bin/env python3
"""
Vertex AI Studio Setup and Configuration

Sets up Vertex AI for HUMMBL framework integration.

Usage:
    python tools/vertex_ai_setup.py --check
    python tools/vertex_ai_setup.py --test
"""

import argparse
import os
import sys
from pathlib import Path

def check_vertex_ai_available():
    """Check if Vertex AI packages are installed."""
    try:
        import vertexai
        from vertexai.preview.language_models import TextGenerationModel
        return True, "Vertex AI packages installed"
    except ImportError as e:
        return False, f"Vertex AI packages not installed: {e}"

def check_credentials():
    """Check if Google Cloud credentials are configured."""
    # Check for service account key
    if os.path.exists(os.path.expanduser("~/.config/gcloud/application_default_credentials.json")):
        return True, "Application default credentials found"
    
    # Check for service account key file
    service_account_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if service_account_key and os.path.exists(service_account_key):
        return True, f"Service account key found: {service_account_key}"
    
    # Check for GCP project
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        return True, f"GCP project set: {project_id}"
    
    return False, "No credentials found. Set GOOGLE_APPLICATION_CREDENTIALS or run 'gcloud auth application-default login'"

def test_vertex_ai_connection():
    """Test Vertex AI connection with a simple query."""
    try:
        import vertexai
        
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            return False, "GOOGLE_CLOUD_PROJECT environment variable not set"
        
        vertexai.init(project=project_id, location="us-central1")
        
        # Try GenerativeModel API first (for Gemini models)
        try:
            from vertexai.generative_models import GenerativeModel
            model = GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                "What is the HUMMBL framework? Answer in one sentence.",
                generation_config={
                    "max_output_tokens": 100,
                    "temperature": 0.2
                }
            )
            return True, f"Connection successful. Response: {response.text[:100]}"
        except (ImportError, Exception):
            # Fallback to TextGenerationModel
            from vertexai.preview.language_models import TextGenerationModel
            model = TextGenerationModel.from_pretrained("text-bison@001")
            response = model.predict(
                "What is the HUMMBL framework? Answer in one sentence.",
                max_output_tokens=100,
                temperature=0.2
            )
            return True, f"Connection successful. Response: {response.text[:100]}"
    except Exception as e:
        return False, f"Connection failed: {e}"

def print_setup_instructions():
    """Print setup instructions for Vertex AI."""
    print("=" * 60)
    print("VERTEX AI SETUP INSTRUCTIONS")
    print("=" * 60)
    print("\n1. Install Vertex AI packages:")
    print("   pip install google-cloud-aiplatform vertexai")
    print("\n2. Set up Google Cloud authentication:")
    print("   Option A: Application Default Credentials")
    print("   gcloud auth application-default login")
    print("\n   Option B: Service Account Key")
    print("   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json")
    print("\n3. Set GCP project:")
    print("   export GOOGLE_CLOUD_PROJECT=your-project-id")
    print("   gcloud config set project your-project-id")
    print("\n4. Enable Vertex AI API:")
    print("   gcloud services enable aiplatform.googleapis.com")
    print("\n5. Test connection:")
    print("   python tools/vertex_ai_setup.py --test")
    print("\n" + "=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description="Vertex AI setup and configuration checker"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if Vertex AI is properly configured"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test Vertex AI connection"
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Print setup instructions"
    )
    
    args = parser.parse_args()
    
    if args.setup:
        print_setup_instructions()
        return
    
    if args.check:
        print("Checking Vertex AI configuration...")
        print("-" * 60)
        
        # Check packages
        available, message = check_vertex_ai_available()
        status = "✅" if available else "❌"
        print(f"{status} Packages: {message}")
        
        # Check credentials
        has_creds, cred_message = check_credentials()
        status = "✅" if has_creds else "❌"
        print(f"{status} Credentials: {cred_message}")
        
        if available and has_creds:
            print("\n✅ Vertex AI is configured and ready to use!")
        else:
            print("\n❌ Vertex AI is not fully configured.")
            print("Run with --setup to see setup instructions.")
        
        return
    
    if args.test:
        print("Testing Vertex AI connection...")
        print("-" * 60)
        
        # Check packages first
        available, _ = check_vertex_ai_available()
        if not available:
            print("❌ Vertex AI packages not installed.")
            print("Install with: pip install google-cloud-aiplatform vertexai")
            sys.exit(1)
        
        # Test connection
        success, message = test_vertex_ai_connection()
        status = "✅" if success else "❌"
        print(f"{status} Connection: {message}")
        
        if success:
            print("\n✅ Vertex AI is working correctly!")
        else:
            print("\n❌ Connection test failed.")
            print("Run with --setup to see setup instructions.")
        
        return
    
    # Default: show setup instructions
    print_setup_instructions()

if __name__ == "__main__":
    main()

