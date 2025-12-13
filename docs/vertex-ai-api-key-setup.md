# Vertex AI API Key Setup - Quick Guide

**Date:** 2025-12-05  
**Status:** Code updated to support API key authentication ✅

---

## Why API Key?

Vertex AI SDK typically uses Application Default Credentials (ADC), but if you're getting 404 errors or need simpler authentication, you can use an API key with the Google Generative AI SDK instead.

---

## Quick Setup (3 Steps)

### 1. Create API Key

**Option A: Via Console (Recommended)**
1. Open: https://console.cloud.google.com/apis/credentials?project=hummbl-research
2. Click **"Create Credentials"** → **"API key"**
3. Copy the key (starts with `AIza...`)
4. **Restrict key** (recommended):
   - Click **"Restrict key"**
   - Under **"API restrictions"**, select **"Restrict key"**
   - Check **"Generative Language API"**
   - Click **"Save"**

**Option B: Via Command Line**
```bash
gcloud alpha services api-keys create \
  --display-name="HUMMBL Vertex AI Key" \
  --api-target=service=generativelanguage.googleapis.com
```

### 2. Set Environment Variable

**Temporary (current session):**
```bash
export GOOGLE_API_KEY="AIzaSy..."
```

**Permanent (add to ~/.zshrc):**
```bash
echo 'export GOOGLE_API_KEY="AIzaSy..."' >> ~/.zshrc
source ~/.zshrc
```

**Verify:**
```bash
echo $GOOGLE_API_KEY
```

### 3. Install SDK & Test

```bash
# Install Google Generative AI SDK
pip install google-generativeai

# Test with API key
python tools/sy19_vertex_ai.py "distributed system with bottlenecks" --use-api-key --top 5
```

---

## Usage

### With API Key (Google AI SDK)

```bash
# Use --use-api-key flag
python tools/sy19_vertex_ai.py "problem description" --use-api-key

# Or pass key directly
python tools/sy19_vertex_ai.py "problem" --use-api-key --api-key "AIzaSy..."
```

### Without API Key (Vertex AI SDK - Default)

```bash
# Uses Application Default Credentials
python tools/sy19_vertex_ai.py "problem description"

# Or disable LLM (keyword-based)
python tools/sy19_vertex_ai.py "problem" --no-llm
```

---

## Authentication Methods Comparison

| Method | SDK | Auth | Use Case |
|--------|-----|------|----------|
| **API Key** | `google-generativeai` | `GOOGLE_API_KEY` env var | Simple, quick setup |
| **ADC** | `vertexai` | `gcloud auth application-default login` | Production, service accounts |
| **Service Account** | `vertexai` | JSON key file | CI/CD, servers |

---

## Troubleshooting

### "GOOGLE_API_KEY environment variable not set"

**Solution:**
```bash
export GOOGLE_API_KEY="your-key-here"
```

### "Google Generative AI SDK not available"

**Solution:**
```bash
pip install google-generativeai
```

### API Key Not Working

1. Verify key is set: `echo $GOOGLE_API_KEY`
2. Check key restrictions in console
3. Ensure Generative Language API is enabled
4. Try regenerating the key

### Still Getting Errors

- API key may need time to propagate (5-10 minutes)
- Check that key has access to Generative Language API
- Verify project billing is enabled

---

## Security Best Practices

1. **Restrict API Keys**
   - Limit to specific APIs (Generative Language API)
   - Restrict to specific IPs (if possible)

2. **Never Commit Keys**
   - Use environment variables
   - Add to `.gitignore` if storing locally
   - Use secrets management for production

3. **Rotate Keys**
   - Rotate periodically
   - Revoke old keys when rotating

4. **Monitor Usage**
   - Check API usage in Cloud Console
   - Set up billing alerts

---

## Next Steps

After setting up the API key:

1. ✅ Test connection: `python tools/sy19_vertex_ai.py "test" --use-api-key`
2. ✅ Use in case studies
3. ✅ Integrate into workflows

---

**Status:** Ready to use with API key! 🚀

