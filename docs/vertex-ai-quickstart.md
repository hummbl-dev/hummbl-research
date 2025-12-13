# Vertex AI Integration - Quick Start

**Date:** 2025-12-05  
**Status:** Tools created, ready for setup

---

## Quick Setup

### 1. Install Dependencies

```bash
pip install google-cloud-aiplatform vertexai
```

### 2. Set Up Authentication

**Option A: Application Default Credentials (Recommended)**
```bash
gcloud auth application-default login
```

**Option B: Service Account Key**
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### 3. Set GCP Project

```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
# or
gcloud config set project your-project-id
```

### 4. Enable Vertex AI API

```bash
gcloud services enable aiplatform.googleapis.com
```

### 5. Verify Setup

```bash
python tools/vertex_ai_setup.py --check
python tools/vertex_ai_setup.py --test
```

---

## Usage

### Enhanced SY19 with Vertex AI

```bash
# Use Vertex AI for primary model detection
python tools/sy19_vertex_ai.py "multi-service AI system with bottlenecks"

# Use specific model
python tools/sy19_vertex_ai.py "problem" --model gemini-pro

# Disable LLM (fallback to keyword matching)
python tools/sy19_vertex_ai.py "problem" --no-llm

# Save to file
python tools/sy19_vertex_ai.py "problem" --output recommendations.md
```

---

## What's Enhanced

### SY19 Improvements:
1. **Better Primary Detection:** LLM understands problem context semantically
2. **Explanation Generation:** AI-generated explanations for recommendations
3. **Contextual Understanding:** Handles complex, nuanced problem descriptions
4. **Multi-language Support:** Can process problems in different languages

---

## Next Steps

See `docs/vertex-ai-integration-plan.md` for:
- Full integration plan
- Additional use cases
- Implementation phases
- Cost considerations

---

**Status:** Ready for setup and testing

