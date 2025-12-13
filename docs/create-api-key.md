# Creating Google Cloud API Key for Vertex AI

**Date:** 2025-12-05  
**Purpose:** Enable API key authentication for Generative AI API

---

## Quick Steps

### 1. Navigate to Credentials Page

Open in browser:
```
https://console.cloud.google.com/apis/credentials?project=hummbl-research
```

Or via command line:
```bash
open "https://console.cloud.google.com/apis/credentials?project=hummbl-research"
```

### 2. Create API Key

1. Click **"Create Credentials"** button (top of page)
2. Select **"API key"** from dropdown
3. Copy the generated API key (starts with `AIza...`)
4. **Important:** Click "Restrict key" to secure it

### 3. Restrict API Key (Recommended)

For security, restrict the key to only Generative AI API:

1. Click **"Restrict key"** after creation
2. Under **"API restrictions"**, select **"Restrict key"**
3. Check **"Generative Language API"** (or "Vertex AI API")
4. Click **"Save"**

### 4. Set Environment Variable

**Temporary (current session):**
```bash
export GOOGLE_API_KEY="AIzaSy..."
```

**Permanent (add to ~/.zshrc):**
```bash
echo 'export GOOGLE_API_KEY="AIzaSy..."' >> ~/.zshrc
source ~/.zshrc
```

### 5. Verify

```bash
echo $GOOGLE_API_KEY
```

Should display your API key.

---

## Alternative: Use Service Account

If you prefer service account authentication:

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=hummbl-research
2. Click **"Create Service Account"**
3. Name: `vertex-ai-service`
4. Grant role: **"Vertex AI User"**
5. Create key: **"Keys"** tab → **"Add Key"** → **"Create new key"** → **JSON**
6. Download JSON file
7. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"
   ```

---

## Testing API Key

After setting the API key, test it:

```bash
python tools/vertex_ai_setup.py --test
```

Or test with SY19:

```bash
python tools/sy19_vertex_ai.py "test problem" --top 5
```

---

## Security Notes

- **Never commit API keys to Git**
- **Restrict API keys** to specific APIs
- **Use service accounts** for production
- **Rotate keys** periodically
- **Monitor usage** in Cloud Console

---

## Troubleshooting

### API Key Not Working

1. Verify key is set: `echo $GOOGLE_API_KEY`
2. Check key restrictions in console
3. Ensure Generative AI API is enabled
4. Try regenerating the key

### Still Getting 404 Errors

- API key may need time to propagate (5-10 minutes)
- Check that key has access to Vertex AI API
- Verify project billing is enabled

---

## Next Steps

After creating the API key:

1. Set `GOOGLE_API_KEY` environment variable
2. Update code to use API key (if needed)
3. Test connection: `python tools/vertex_ai_setup.py --test`
4. Use SY19: `python tools/sy19_vertex_ai.py "problem"`

---

**Status:** Ready to create API key

