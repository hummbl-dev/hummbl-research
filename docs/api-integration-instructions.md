# API Integration Instructions

## Quick Start

If your API code is in a separate repository (e.g., `hummbl-api` or Cloudflare Workers project), follow these steps:

### Step 1: Get the Enhanced Data

The enhanced context is ready in:
```
validation/enhanced-models-context.json
```

This file contains all 120 models with:
- Full descriptions
- Examples
- Related models
- Status & version
- Relationship verification data

### Step 2: Choose Integration Method

**Option A: Static Import** (Recommended for Workers)
- Copy `enhanced-models-context.json` to your Workers project
- Import it in your Worker code
- Deploy

**Option B: Dynamic Fetch** (Recommended for flexibility)
- Fetch from GitHub raw URL
- Cache in memory (1 hour TTL)
- Auto-updates when you push changes

### Step 3: Update Your API Code

See `api-integration-example.js` for a complete working example.

Key changes:
1. Load enhanced models instead of basic models
2. Return all new fields in response
3. Keep `definition` field for backward compatibility

### Step 4: Test

```bash
# Test enhanced response
curl https://hummbl-api.hummbl.workers.dev/v1/models | jq '.models[0]'

# Verify relationship data
curl https://hummbl-api.hummbl.workers.dev/v1/models | jq '.models[] | select(.code == "SY19") | .relationships'
```

## If API Code is in This Repository

If the API code is actually in this repository (I didn't find it), I can:

1. **Locate the API code** - Search for Workers/API files
2. **Update it directly** - Modify the code to use enhanced context
3. **Test the changes** - Verify it works

## If API Code is External

If the API is in a separate repository or service:

1. **I can create**:
   - Complete integration code (see `api-integration-example.js`)
   - Step-by-step instructions
   - Migration guide

2. **You can**:
   - Copy the integration code to your API project
   - Update the data source path
   - Deploy

## What I Need to Know

To help you integrate, please tell me:

1. **Where is the API code?**
   - Separate repository?
   - Cloudflare Workers dashboard?
   - Different service?

2. **What's the current API structure?**
   - How does it currently load models?
   - What format does it return?

3. **How do you deploy?**
   - `wrangler deploy`?
   - GitHub Actions?
   - Manual upload?

Once I know this, I can provide exact integration steps or update the code directly if it's accessible.

