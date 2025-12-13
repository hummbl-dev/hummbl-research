# Vertex AI Model Access Issue

**Date:** 2025-12-05  
**Status:** Models not accessible - troubleshooting

---

## Issue

Vertex AI models (text-bison, gemini-1.5-flash, gemini-pro) are returning 404 errors:
```
404 Publisher Model `projects/hummbl-research/locations/us-central1/publishers/google/models/MODEL-NAME` was not found or your project does not have access to it.
```

---

## Possible Causes

1. **Billing Not Enabled**
   - Vertex AI requires billing to be enabled
   - Check: https://console.cloud.google.com/billing

2. **Model Access Permissions**
   - Some models may require specific permissions
   - Check IAM roles for Vertex AI User

3. **Region Availability**
   - Models may not be available in all regions
   - Try different regions (us-central1, us-east1, us-west1)

4. **API Enablement**
   - Generative AI API may need to be enabled separately
   - Check: `gcloud services list --enabled`

5. **Model Deprecation**
   - text-bison@001 may be deprecated
   - Use newer models (gemini-1.5-flash, gemini-1.5-pro)

---

## Troubleshooting Steps

### 1. Verify Billing

```bash
gcloud billing projects describe hummbl-research
```

If no billing account, enable via console:
- https://console.cloud.google.com/billing

### 2. Check IAM Permissions

```bash
gcloud projects get-iam-policy hummbl-research
```

Ensure you have:
- `roles/aiplatform.user` or
- `roles/vertexai.user`

### 3. Enable All Required APIs

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com
gcloud services enable cloudaicompanion.googleapis.com
```

### 4. Try Different Regions

Models may be available in different regions. Try:
- us-central1 (default)
- us-east1
- us-west1
- europe-west1

### 5. Use Vertex AI Studio

Check model availability via console:
- https://console.cloud.google.com/vertex-ai/studio

---

## Workaround: Use Keyword-Based SY19

Until model access is resolved, SY19 will automatically fall back to keyword-based detection:

```bash
# This will work (falls back to keywords)
python tools/sy19_vertex_ai.py "problem description" --no-llm

# Or use base SY19
python tools/sy19_recommend.py "problem description"
```

---

## Next Steps

1. **Enable Billing** (if not already enabled)
2. **Check Model Availability** in Vertex AI Studio console
3. **Verify IAM Permissions**
4. **Try Different Regions**
5. **Contact Google Cloud Support** if issue persists

---

**Status:** Setup complete, model access needs resolution

