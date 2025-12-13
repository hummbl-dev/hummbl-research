# Vertex AI Setup Guide - Complete Walkthrough

**Date:** 2025-12-05  
**Platform:** macOS (can be adapted for Linux/Windows)

---

## Quick Start

Run the automated setup script:
```bash
python tools/setup_gcp_project.py
```

This will guide you through all steps interactively.

---

## Manual Setup (Step-by-Step)

### Step 1: Install Google Cloud SDK

**macOS (using Homebrew - Recommended):**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Google Cloud SDK
brew install google-cloud-sdk

# Initialize gcloud
gcloud init
```

**macOS (Manual Installation):**
```bash
# Download and install
curl https://sdk.cloud.google.com | bash

# Restart shell or source
exec -l $SHELL

# Initialize
gcloud init
```

**Verify Installation:**
```bash
gcloud --version
```

---

### Step 2: Authenticate

```bash
# Login to your Google account
gcloud auth login

# Set up application default credentials (for Python)
gcloud auth application-default login
```

This opens a browser for authentication.

---

### Step 3: Create or Select Project

**Option A: Create New Project (Recommended)**
```bash
# Create project (project ID must be globally unique)
gcloud projects create hummbl-vertex-ai-$(date +%s) \
    --name="HUMMBL Vertex AI"

# Or with custom ID
gcloud projects create YOUR-UNIQUE-PROJECT-ID \
    --name="HUMMBL Vertex AI"

# Set as default
gcloud config set project YOUR-PROJECT-ID
```

**Option B: Use Existing Project**
```bash
# List projects
gcloud projects list

# Set as default
gcloud config set project YOUR-PROJECT-ID
```

**Set Environment Variable:**
```bash
export GOOGLE_CLOUD_PROJECT=YOUR-PROJECT-ID

# Add to ~/.zshrc for persistence
echo 'export GOOGLE_CLOUD_PROJECT=YOUR-PROJECT-ID' >> ~/.zshrc
source ~/.zshrc
```

---

### Step 4: Enable Billing

**Important:** Vertex AI requires billing to be enabled.

1. **Via Console (Recommended):**
   - Go to: https://console.cloud.google.com/billing
   - Create or select a billing account
   - Link it to your project

2. **Via CLI:**
   ```bash
   # List billing accounts
   gcloud billing accounts list
   
   # Link billing account
   gcloud billing projects link YOUR-PROJECT-ID \
       --billing-account=BILLING-ACCOUNT-ID
   ```

---

### Step 5: Enable Vertex AI API

```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com \
    --project=YOUR-PROJECT-ID

# Verify
gcloud services list --enabled --project=YOUR-PROJECT-ID
```

---

### Step 6: Install Python Packages

```bash
# Install Vertex AI packages
pip install google-cloud-aiplatform vertexai

# Or install all requirements
pip install -r requirements.txt
```

---

### Step 7: Verify Setup

```bash
# Check configuration
python tools/vertex_ai_setup.py --check

# Test connection
python tools/vertex_ai_setup.py --test
```

---

## Complete Setup Commands (Copy-Paste)

**For new project:**
```bash
# 1. Install gcloud (if not installed)
brew install google-cloud-sdk

# 2. Authenticate
gcloud auth login
gcloud auth application-default login

# 3. Create project (replace YOUR-UNIQUE-ID with something unique)
PROJECT_ID="hummbl-vertex-ai-$(date +%s)"
gcloud projects create $PROJECT_ID --name="HUMMBL Vertex AI"
gcloud config set project $PROJECT_ID
export GOOGLE_CLOUD_PROJECT=$PROJECT_ID

# 4. Enable billing (via console: https://console.cloud.google.com/billing)
# Then link:
# gcloud billing projects link $PROJECT_ID --billing-account=ACCOUNT-ID

# 5. Enable APIs
gcloud services enable aiplatform.googleapis.com --project=$PROJECT_ID

# 6. Install packages
pip install google-cloud-aiplatform vertexai

# 7. Verify
python tools/vertex_ai_setup.py --check
python tools/vertex_ai_setup.py --test
```

---

## Troubleshooting

### "gcloud: command not found"
**Solution:** Install Google Cloud SDK (see Step 1)

### "Project not found"
**Solution:** 
```bash
gcloud projects list
gcloud config set project YOUR-PROJECT-ID
```

### "API not enabled"
**Solution:**
```bash
gcloud services enable aiplatform.googleapis.com --project=YOUR-PROJECT-ID
```

### "Billing not enabled"
**Solution:** Enable billing via console or CLI (see Step 4)

### "Permission denied"
**Solution:** Check IAM permissions or re-authenticate:
```bash
gcloud auth application-default login
```

---

## Next Steps After Setup

1. **Test Enhanced SY19:**
   ```bash
   python tools/sy19_vertex_ai.py "multi-service AI system with bottlenecks"
   ```

2. **Monitor Usage:**
   - Console: https://console.cloud.google.com/vertex-ai
   - Billing: https://console.cloud.google.com/billing

3. **Set Budget Alerts:**
   - Go to: https://console.cloud.google.com/billing/budgets
   - Create budget for your project

---

**Ready to start? Run:** `python tools/setup_gcp_project.py`

