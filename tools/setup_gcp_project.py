#!/usr/bin/env python3
"""
Interactive Google Cloud Project Setup Script

Guides you through setting up a GCP project for Vertex AI integration.

Usage:
    python tools/setup_gcp_project.py
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout + e.stderr, e.returncode

def check_gcloud_installed():
    """Check if gcloud CLI is installed."""
    output, code = run_command("gcloud --version", check=False)
    return code == 0, output

def check_authenticated():
    """Check if user is authenticated."""
    output, code = run_command("gcloud auth list", check=False)
    return code == 0 and "ACTIVE" in output, output

def list_projects():
    """List available GCP projects."""
    output, code = run_command("gcloud projects list --format='value(projectId)'", check=False)
    if code == 0:
        return [p.strip() for p in output.split('\n') if p.strip()]
    return []

def create_project(project_id, project_name):
    """Create a new GCP project."""
    cmd = f"gcloud projects create {project_id} --name='{project_name}'"
    output, code = run_command(cmd, check=False)
    return code == 0, output

def set_project(project_id):
    """Set the default project."""
    cmd = f"gcloud config set project {project_id}"
    output, code = run_command(cmd, check=False)
    return code == 0, output

def enable_api(project_id, api_name):
    """Enable a GCP API."""
    cmd = f"gcloud services enable {api_name} --project={project_id}"
    output, code = run_command(cmd, check=False)
    return code == 0, output

def check_billing(project_id):
    """Check if billing is enabled."""
    cmd = f"gcloud billing projects describe {project_id}"
    output, code = run_command(cmd, check=False)
    return "billingAccountName" in output, output

def main():
    print("=" * 60)
    print("GOOGLE CLOUD PROJECT SETUP FOR VERTEX AI")
    print("=" * 60)
    print()
    
    # Step 1: Check gcloud installation
    print("Step 1: Checking gcloud CLI installation...")
    installed, output = check_gcloud_installed()
    if not installed:
        print("❌ gcloud CLI not found!")
        print("\nPlease install Google Cloud SDK:")
        print("  macOS: brew install google-cloud-sdk")
        print("  Linux: curl https://sdk.cloud.google.com | bash")
        print("  Or visit: https://cloud.google.com/sdk/docs/install")
        sys.exit(1)
    print("✅ gcloud CLI installed")
    print(f"   {output.split(chr(10))[0]}")
    print()
    
    # Step 2: Check authentication
    print("Step 2: Checking authentication...")
    authenticated, output = check_authenticated()
    if not authenticated:
        print("❌ Not authenticated!")
        print("\nPlease run:")
        print("  gcloud auth login")
        print("  gcloud auth application-default login")
        response = input("\nWould you like to authenticate now? (y/n): ")
        if response.lower() == 'y':
            print("\nRunning: gcloud auth login")
            run_command("gcloud auth login", check=False)
            print("\nRunning: gcloud auth application-default login")
            run_command("gcloud auth application-default login", check=False)
            authenticated, _ = check_authenticated()
    
    if not authenticated:
        print("❌ Authentication failed. Please authenticate manually.")
        sys.exit(1)
    print("✅ Authenticated")
    print()
    
    # Step 3: Select or create project
    print("Step 3: Setting up project...")
    projects = list_projects()
    
    if projects:
        print(f"\nFound {len(projects)} existing project(s):")
        for i, proj in enumerate(projects, 1):
            print(f"  {i}. {proj}")
        print(f"  {len(projects) + 1}. Create new project")
        
        choice = input(f"\nSelect project (1-{len(projects) + 1}): ")
        try:
            idx = int(choice) - 1
            if idx < len(projects):
                project_id = projects[idx]
                print(f"✅ Using existing project: {project_id}")
            else:
                # Create new project
                project_id = input("Enter new project ID (must be globally unique): ").strip()
                project_name = input("Enter project name: ").strip() or "HUMMBL Vertex AI"
                print(f"\nCreating project: {project_id}...")
                success, output = create_project(project_id, project_name)
                if not success:
                    print(f"❌ Failed to create project: {output}")
                    sys.exit(1)
                print(f"✅ Project created: {project_id}")
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            sys.exit(1)
    else:
        # No projects, create new one
        print("No existing projects found.")
        project_id = input("Enter new project ID (must be globally unique): ").strip()
        project_name = input("Enter project name: ").strip() or "HUMMBL Vertex AI"
        print(f"\nCreating project: {project_id}...")
        success, output = create_project(project_id, project_name)
        if not success:
            print(f"❌ Failed to create project: {output}")
            sys.exit(1)
        print(f"✅ Project created: {project_id}")
    
    # Set as default
    print(f"\nSetting {project_id} as default project...")
    success, _ = set_project(project_id)
    if success:
        print("✅ Project set as default")
    else:
        print("⚠️  Warning: Could not set as default (continuing anyway)")
    
    # Set environment variable
    os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
    print(f"\n✅ Project ID set: {project_id}")
    print(f"   Add to your shell: export GOOGLE_CLOUD_PROJECT={project_id}")
    print()
    
    # Step 4: Check billing
    print("Step 4: Checking billing...")
    has_billing, _ = check_billing(project_id)
    if not has_billing:
        print("⚠️  Billing not enabled!")
        print("\nVertex AI requires billing to be enabled.")
        print("Please enable billing:")
        print(f"  1. Go to: https://console.cloud.google.com/billing")
        print(f"  2. Link a billing account to project: {project_id}")
        print("\nOr use CLI:")
        print("  gcloud billing accounts list")
        print("  gcloud billing projects link PROJECT-ID --billing-account=ACCOUNT-ID")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Setup paused. Enable billing and run again.")
            sys.exit(0)
    else:
        print("✅ Billing enabled")
    print()
    
    # Step 5: Enable APIs
    print("Step 5: Enabling required APIs...")
    apis = [
        "aiplatform.googleapis.com",  # Vertex AI
        "compute.googleapis.com",      # Compute (optional but useful)
    ]
    
    for api in apis:
        print(f"  Enabling {api}...")
        success, output = enable_api(project_id, api)
        if success:
            print(f"  ✅ {api} enabled")
        else:
            print(f"  ⚠️  {api}: {output}")
    print()
    
    # Step 6: Install Python packages
    print("Step 6: Checking Python packages...")
    try:
        import vertexai
        print("✅ Vertex AI packages installed")
    except ImportError:
        print("❌ Vertex AI packages not installed")
        print("\nInstalling packages...")
        success, output = run_command("pip install google-cloud-aiplatform vertexai", check=False)
        if success:
            print("✅ Packages installed")
        else:
            print(f"⚠️  Installation may have issues: {output}")
            print("   Try manually: pip install google-cloud-aiplatform vertexai")
    print()
    
    # Step 7: Test connection
    print("Step 7: Testing Vertex AI connection...")
    print("  (This will make a test API call)")
    response = input("  Run connection test? (y/n): ")
    if response.lower() == 'y':
        try:
            import vertexai
            from vertexai.preview.language_models import TextGenerationModel
            
            vertexai.init(project=project_id, location="us-central1")
            model = TextGenerationModel.from_pretrained("text-bison@001")
            test_response = model.predict(
                "Say 'HUMMBL setup successful' if you can read this.",
                max_output_tokens=20,
                temperature=0.1
            )
            print(f"  ✅ Connection successful!")
            print(f"  Response: {test_response.text}")
        except Exception as e:
            print(f"  ⚠️  Connection test failed: {e}")
            print("  This might be due to billing or API enablement delay.")
            print("  Try again in a few minutes.")
    else:
        print("  ⏭️  Skipped connection test")
    print()
    
    # Summary
    print("=" * 60)
    print("SETUP SUMMARY")
    print("=" * 60)
    print(f"Project ID: {project_id}")
    print(f"Environment Variable: export GOOGLE_CLOUD_PROJECT={project_id}")
    print()
    print("Next steps:")
    print("  1. Add to your shell config (~/.zshrc or ~/.bashrc):")
    print(f"     export GOOGLE_CLOUD_PROJECT={project_id}")
    print("  2. Test setup:")
    print("     python tools/vertex_ai_setup.py --check")
    print("     python tools/vertex_ai_setup.py --test")
    print("  3. Try enhanced SY19:")
    print("     python tools/sy19_vertex_ai.py 'test problem'")
    print()
    print("=" * 60)
    print("✅ Setup complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()

