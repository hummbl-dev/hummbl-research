# API Integration Code

This document provides the code and instructions to integrate enhanced context and relationship data into the `hummbl-api.hummbl.workers.dev/v1/models` endpoint.

## Overview

The enhanced API response should include:
- Full `description` field (200-700 chars)
- `example` field (usage examples)
- `related_models` array
- `status` and `version` fields
- `relationships` object (verification data)

## Data Source

The enhanced context is available in:
- **File**: `validation/enhanced-models-context.json`
- **Format**: JSON with `{ "total": 120, "models": [...] }`
- **Updated**: After model name fixes and relationship verification

## Cloudflare Workers Integration

### Option 1: Load from JSON File (Static)

If your Workers project can access the JSON file:

```javascript
// src/index.js or wrangler.toml
import enhancedModels from '../validation/enhanced-models-context.json';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname === '/v1/models') {
      // Return enhanced models with all context
      return new Response(JSON.stringify({
        total: enhancedModels.total,
        models: enhancedModels.models
      }), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### Option 2: Fetch from External Source (Dynamic)

If the JSON is hosted elsewhere or you want to update it dynamically:

```javascript
// src/index.js
const ENHANCED_MODELS_URL = 'https://raw.githubusercontent.com/hummbl-dev/hummbl-research/main/validation/enhanced-models-context.json';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname === '/v1/models') {
      // Fetch enhanced models
      const response = await fetch(ENHANCED_MODELS_URL);
      const enhancedModels = await response.json();
      
      return new Response(JSON.stringify(enhancedModels), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'public, max-age=3600' // Cache for 1 hour
        }
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### Option 3: Merge with Existing API (Backward Compatible)

If you want to keep the existing API structure and add new fields:

```javascript
// src/index.js
import enhancedModels from '../validation/enhanced-models-context.json';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname === '/v1/models') {
      // Transform to match current API format + add new fields
      const models = enhancedModels.models.map(model => ({
        // Existing fields (backward compatible)
        code: model.code,
        name: model.name,
        definition: model.definition, // Short summary (80 chars)
        priority: model.priority,
        transformation: model.transformation,
        
        // New enhanced fields
        description: model.description, // Full description (200-700 chars)
        example: model.example, // Usage example
        related_models: model.related_models, // Array of codes
        status: model.status, // draft/prototype/developed
        version: model.version, // Semantic version
        relationships: model.relationships // Relationship verification data
      }));
      
      return new Response(JSON.stringify({
        total: models.length,
        models: models
      }), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

## Response Format

### Enhanced Model Object

```json
{
  "code": "SY19",
  "name": "Meta-Model Selection",
  "transformation": "SY",
  "priority": 6,
  "definition": "SY19 is a meta-model that recommends which HUMMBL models...",
  "description": "SY19 is a meta-model that recommends which HUMMBL models to use for a given problem. It uses the relationship graph (367 relationships across 120 models)...",
  "example": "Problem: 'multi-service AI feature with bottlenecks and cascades'...",
  "related_models": ["SY01", "SY04", "DE06", "DE07"],
  "status": "prototype",
  "version": "0.1.0",
  "relationships": {
    "incoming_count": 4,
    "outgoing_count": 2,
    "total_count": 6,
    "by_type": {
      "SCAFFOLDS": 6
    },
    "strength": {
      "min": 0.8,
      "max": 1.0,
      "avg": 0.88
    },
    "verification": {
      "valid": true,
      "errors": []
    }
  }
}
```

## Deployment Steps

1. **Copy the enhanced context file** to your Workers project:
   ```bash
   cp validation/enhanced-models-context.json <your-workers-project>/data/
   ```

2. **Update your Workers code** using one of the options above

3. **Test locally**:
   ```bash
   wrangler dev
   ```

4. **Deploy**:
   ```bash
   wrangler deploy
   ```

## Response Size Considerations

- **Current**: ~80 chars per model × 120 models = ~9.6 KB
- **Enhanced**: ~500-1000 chars per model × 120 models = ~60-120 KB
- **Cloudflare Workers limit**: 100 MB (plenty of room)
- **Recommendation**: Add caching headers for better performance

## Field Usage Guide

### For API Consumers

- **`definition`**: Use for short summaries, tooltips, search results
- **`description`**: Use for full model documentation, detail views
- **`example`**: Use for tutorials, usage guides, demos
- **`related_models`**: Use for navigation, "see also" sections
- **`relationships`**: Use for graph visualization, SY19 integration, relationship analysis
- **`status`**: Use to filter by maturity (e.g., only show "developed" models)
- **`version`**: Use for versioning, change tracking

## Migration Strategy

### Phase 1: Add New Fields (Non-Breaking)
- Add new fields alongside existing ones
- Existing consumers continue to work
- New consumers can use enhanced fields

### Phase 2: Deprecate Old Fields (Optional)
- Mark `definition` as deprecated (but keep it)
- Encourage migration to `description`

### Phase 3: Version API (If Needed)
- Create `/v2/models` with enhanced fields only
- Keep `/v1/models` for backward compatibility

## Testing

Test the enhanced API:

```bash
# Test single model
curl https://hummbl-api.hummbl.workers.dev/v1/models | jq '.models[0]'

# Test relationship data
curl https://hummbl-api.hummbl.workers.dev/v1/models | jq '.models[] | select(.code == "SY19") | .relationships'

# Test response size
curl -s https://hummbl-api.hummbl.workers.dev/v1/models | wc -c
```

## Updating the Data

When model names or relationships change:

1. **Regenerate enhanced context**:
   ```bash
   python tools/extract_model_context.py
   ```

2. **Update the JSON file** in your Workers project

3. **Redeploy** (or use dynamic fetching from GitHub)

## Support

If you need help integrating this:
- Check `validation/enhanced-models-context.json` for the data structure
- See `docs/api-context-enhancement-proposal.md` for full proposal
- Use `tools/extract_model_context.py` to regenerate data

