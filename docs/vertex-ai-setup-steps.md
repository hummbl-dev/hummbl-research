# Vertex AI Setup - Step-by-Step Instructions

**Date:** 2025-12-05  
**Status:** Ready to execute

---

## Prerequisites Check ✅

- ✅ gcloud CLI installed (version 548.0.0)
- ⏳ Authentication needed
- ⏳ Project setup needed

---

## Step 1: Authenticate with Google Cloud

Run these commands in your terminal:

```bash
# Add gcloud to PATH (if not already there)
export PATH="/usr/local/Caskroom/gcloud-cli/548.0.0/google-cloud-sdk/bin:$PATH"

# Login to your Google account
gcloud auth login

# Set up application default credentials (for Python SDK)
gcloud auth application-default login
```

**What happens:**
- `gcloud auth login` will open a browser window for you to sign in
- `gcloud auth application-default login` will also open a browser for application credentials
- Both will authenticate you with Google Cloud

---

## Step 2: Create or Select a Project

**Option A: Create New Project (Recommended)**

```bash
# Create a new project (replace YOUR-UNIQUE-ID with something unique)
PROJECT_ID="hummbl-vertex-ai-$(date +%s)"
gcloud projects create $PROJECT_ID --name="HUMMBL Vertex AI"

# Set as default
gcloud config set project $PROJECT_ID

# Set environment variable
export GOOGLE_CLOUD_PROJECT=$PROJECT_ID
```

**Option B: Use Existing Project**

```bash
# List existing projects
gcloud projects list

# Set as default
gcloud config set project YOUR-PROJECT-ID

# Set environment variable
export GOOGLE_CLOUD_PROJECT=YOUR-PROJECT-ID
```

**Make it persistent:**
```bash
# Add to your shell config
echo 'export GOOGLE_CLOUD_PROJECT=YOUR-PROJECT-ID' >> ~/.zshrc
echo 'export PATH="/usr/local/Caskroom/gcloud-cli/548.0.0/google-cloud-sdk/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Step 3: Enable Billing

**Important:** Vertex AI requires billing to be enabled.

**Via Console (Recommended):**
1. Go to: https://console.cloud.google.com/billing
2. Create or select a billing account
3. Link it to your project

**Via CLI:**
```bash
# List billing accounts
gcloud billing accounts list

# Link billing account (replace ACCOUNT-ID)
gcloud billing projects link YOUR-PROJECT-ID --billing-account=ACCOUNT-ID
```

---

## Step 4: Enable Vertex AI API

```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com --project=$GOOGLE_CLOUD_PROJECT

# Verify
gcloud services list --enabled --project=$GOOGLE_CLOUD_PROJECT | grep aiplatform
```

---

## Step 5: Install Python Packages

```bash
# Install Vertex AI packages
pip install google-cloud-aiplatform vertexai

# Or install all requirements
pip install -r requirements.txt
```

---

## Step 6: Verify Setup

```bash
# Check configuration
python tools/vertex_ai_setup.py --check

# Test connection
python tools/vertex_ai_setup.py --test
```

---

## Step 7: Test Enhanced SY19

```bash
# Test with a simple problem
python tools/sy19_vertex_ai.py "test problem"

# Test on case study scenario
python tools/sy19_vertex_ai.py "multi-service AI system with bottlenecks"
```

---

## Quick Copy-Paste Setup

Run these commands in order:

```bash
# 1. Add gcloud to PATH
export PATH="/usr/local/Caskroom/gcloud-cli/548.0.0/google-cloud-sdk/bin:$PATH"

# 2. Authenticate
gcloud auth login
gcloud auth application-default login

# 3. Create project (or use existing)
PROJECT_ID="hummbl-vertex-ai-$(date +%s)"
gcloud projects create $PROJECT_ID --name="HUMMBL Vertex AI"
gcloud config set project $PROJECT_ID
export GOOGLE_CLOUD_PROJECT=$PROJECT_ID

# 4. Enable billing (via console: https://console.cloud.google.com/billing)
# Then link: gcloud billing projects link $PROJECT_ID --billing-account=ACCOUNT-ID

# 5. Enable API
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
**Solution:** Add to PATH:
```bash
export PATH="/usr/local/Caskroom/gcloud-cli/548.0.0/google-cloud-sdk/bin:$PATH"
```

### "Not authenticated"
**Solution:** Run authentication:
```bash
gcloud auth login
gcloud auth application-default login
```

### "API not enabled"
**Solution:** Enable the API:
```bash
gcloud services enable aiplatform.googleapis.com --project=$GOOGLE_CLOUD_PROJECT
```

### "Billing not enabled"
**Solution:** Enable billing via console or CLI (see Step 3)

---

**Ready to start? Begin with Step 1: Authentication**

