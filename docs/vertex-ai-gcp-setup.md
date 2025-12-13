# Google Cloud Project Setup for Vertex AI

**Date:** 2025-12-05  
**Purpose:** Complete setup guide for Vertex AI integration with HUMMBL

---

## Prerequisites

- Google Cloud account (or create one at https://cloud.google.com)
- `gcloud` CLI installed (or install from https://cloud.google.com/sdk/docs/install)
- Billing account (required for Vertex AI API usage)

---

## Step-by-Step Setup

### Step 1: Install Google Cloud SDK

**macOS:**
```bash
# Using Homebrew
brew install google-cloud-sdk

# Or download from:
# https://cloud.google.com/sdk/docs/install
```

**Linux:**
```bash
# Download and install
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Windows:**
Download installer from: https://cloud.google.com/sdk/docs/install

**Verify installation:**
```bash
gcloud --version
```

---

### Step 2: Authenticate with Google Cloud

```bash
# Login to your Google account
gcloud auth login

# Set up application default credentials (for Python SDK)
gcloud auth application-default login
```

This will open a browser window for authentication.

---

### Step 3: Create or Select a Project

**Option A: Create New Project**
```bash
# Create a new project
gcloud projects create hummbl-vertex-ai \
    --name="HUMMBL Vertex AI" \
    --set-as-default

# Or use a specific project ID (must be globally unique)
gcloud projects create YOUR-PROJECT-ID \
    --name="HUMMBL Vertex AI"
```

**Option B: Use Existing Project**
```bash
# List existing projects
gcloud projects list

# Set as default
gcloud config set project YOUR-PROJECT-ID
```

**Set Project ID:**
```bash
export GOOGLE_CLOUD_PROJECT=YOUR-PROJECT-ID
# Or add to ~/.bashrc or ~/.zshrc for persistence
```

---

### Step 4: Enable Billing

**Important:** Vertex AI API requires a billing account.

1. Go to: https://console.cloud.google.com/billing
2. Link a billing account to your project
3. Or use the CLI:
```bash
gcloud billing accounts list
gcloud billing projects link YOUR-PROJECT-ID \
    --billing-account=BILLING-ACCOUNT-ID
```

---

### Step 5: Enable Required APIs

```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Enable other useful APIs
gcloud services enable compute.googleapis.com
gcloud services enable storage.googleapis.com

# Verify enabled services
gcloud services list --enabled
```

---

### Step 6: Set Up Authentication

**For Local Development (Recommended):**
```bash
# Application Default Credentials (ADC)
gcloud auth application-default login
```

**For Service Account (Production/CI/CD):**
```bash
# Create service account
gcloud iam service-accounts create hummbl-vertex-ai \
    --display-name="HUMMBL Vertex AI Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR-PROJECT-ID \
    --member="serviceAccount:hummbl-vertex-ai@YOUR-PROJECT-ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create and download key
gcloud iam service-accounts keys create ~/hummbl-vertex-ai-key.json \
    --iam-account=hummbl-vertex-ai@YOUR-PROJECT-ID.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS=~/hummbl-vertex-ai-key.json
```

---

### Step 7: Install Python Dependencies

```bash
# Install Vertex AI packages
pip install google-cloud-aiplatform vertexai

# Or install all requirements
pip install -r requirements.txt
```

---

### Step 8: Configure Environment Variables

**Create `.env` file (optional):**
```bash
# .env file
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1
VERTEX_AI_MODEL=text-bison@001
```

**Or set in shell:**
```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_REGION=us-central1
```

**Add to `~/.bashrc` or `~/.zshrc` for persistence:**
```bash
echo 'export GOOGLE_CLOUD_PROJECT=your-project-id' >> ~/.zshrc
echo 'export GOOGLE_CLOUD_REGION=us-central1' >> ~/.zshrc
source ~/.zshrc
```

---

### Step 9: Verify Setup

```bash
# Check configuration
python tools/vertex_ai_setup.py --check

# Test connection
python tools/vertex_ai_setup.py --test
```

---

## Quick Setup Script

Run the automated setup script:

```bash
python tools/setup_gcp_project.py
```

This will guide you through the setup interactively.

---

## Cost Considerations

**Vertex AI Pricing (approximate):**
- Text Generation (text-bison): ~$0.0005 per 1K characters
- Gemini Pro: Different pricing model
- Free tier: Limited free usage per month

**Cost Optimization:**
- Use appropriate model sizes
- Cache common queries
- Monitor usage in Cloud Console
- Set up billing alerts

**Set Budget Alerts:**
1. Go to: https://console.cloud.google.com/billing/budgets
2. Create budget for your project
3. Set alert thresholds

---

## Troubleshooting

### Issue: "Project not found"
**Solution:** Verify project ID and ensure it exists:
```bash
gcloud projects list
gcloud config set project YOUR-PROJECT-ID
```

### Issue: "API not enabled"
**Solution:** Enable the API:
```bash
gcloud services enable aiplatform.googleapis.com
```

### Issue: "Permission denied"
**Solution:** Check IAM permissions:
```bash
gcloud projects get-iam-policy YOUR-PROJECT-ID
```

### Issue: "Billing not enabled"
**Solution:** Link billing account:
```bash
gcloud billing accounts list
gcloud billing projects link YOUR-PROJECT-ID --billing-account=ACCOUNT-ID
```

### Issue: "Authentication failed"
**Solution:** Re-authenticate:
```bash
gcloud auth application-default login
```

---

## Next Steps

After setup is complete:

1. **Test SY19 with Vertex AI:**
   ```bash
   python tools/sy19_vertex_ai.py "test problem"
   ```

2. **Run on case study scenarios:**
   ```bash
   python tools/sy19_vertex_ai.py "multi-service AI system with bottlenecks"
   ```

3. **Monitor usage:**
   - Check Cloud Console: https://console.cloud.google.com/vertex-ai
   - Monitor costs: https://console.cloud.google.com/billing

---

## Security Best Practices

1. **Never commit credentials:**
   - Add `*.json` (service account keys) to `.gitignore`
   - Use environment variables for sensitive data

2. **Use least privilege:**
   - Grant only necessary IAM roles
   - Use service accounts for production

3. **Rotate credentials:**
   - Regularly rotate service account keys
   - Use short-lived tokens when possible

4. **Monitor access:**
   - Review IAM policies regularly
   - Enable audit logs

---

**Status:** Ready for setup

