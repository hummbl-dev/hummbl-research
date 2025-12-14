/**
 * Example Cloudflare Workers integration for enhanced HUMMBL API
 * 
 * This is a complete example showing how to integrate the enhanced
 * model context and relationship data into your API endpoint.
 * 
 * Usage:
 * 1. Copy this file to your Workers project
 * 2. Install dependencies: npm install
 * 3. Update the data path to point to enhanced-models-context.json
 * 4. Deploy: wrangler deploy
 */

// Option 1: Import from local file (if bundled with Workers)
// import enhancedModels from './validation/enhanced-models-context.json';

// Option 2: Fetch from GitHub (dynamic)
const ENHANCED_MODELS_URL = 'https://raw.githubusercontent.com/hummbl-dev/hummbl-research/main/validation/enhanced-models-context.json';

// Cache for enhanced models (in-memory, resets on worker restart)
let cachedModels = null;
let cacheTimestamp = 0;
const CACHE_TTL = 3600000; // 1 hour in milliseconds

async function getEnhancedModels() {
  const now = Date.now();
  
  // Return cached data if still valid
  if (cachedModels && (now - cacheTimestamp) < CACHE_TTL) {
    return cachedModels;
  }
  
  // Fetch fresh data
  try {
    const response = await fetch(ENHANCED_MODELS_URL);
    if (!response.ok) {
      throw new Error(`Failed to fetch: ${response.status}`);
    }
    
    const data = await response.json();
    cachedModels = data;
    cacheTimestamp = now;
    return data;
  } catch (error) {
    console.error('Error fetching enhanced models:', error);
    // Return cached data even if expired, or return error
    if (cachedModels) {
      return cachedModels;
    }
    throw error;
  }
}

/**
 * Transform model to API response format
 * Includes backward compatibility with existing API structure
 */
function transformModel(model) {
  return {
    // Existing fields (backward compatible)
    code: model.code,
    name: model.name,
    definition: model.definition || model.description?.substring(0, 80) || '',
    priority: model.priority,
    transformation: model.transformation,
    
    // New enhanced fields
    description: model.description,
    example: model.example,
    related_models: model.related_models || [],
    status: model.status,
    version: model.version,
    relationships: model.relationships || null
  };
}

/**
 * Filter models based on query parameters
 */
function filterModels(models, queryParams) {
  let filtered = models;
  
  // Filter by transformation
  if (queryParams.transformation) {
    filtered = filtered.filter(m => 
      m.transformation.toLowerCase() === queryParams.transformation.toLowerCase()
    );
  }
  
  // Filter by status
  if (queryParams.status) {
    filtered = filtered.filter(m => 
      m.status.toLowerCase() === queryParams.status.toLowerCase()
    );
  }
  
  // Filter by code (single model)
  if (queryParams.code) {
    filtered = filtered.filter(m => 
      m.code.toLowerCase() === queryParams.code.toLowerCase()
    );
  }
  
  // Search by name or description
  if (queryParams.search) {
    const searchTerm = queryParams.search.toLowerCase();
    filtered = filtered.filter(m => 
      m.name.toLowerCase().includes(searchTerm) ||
      (m.description && m.description.toLowerCase().includes(searchTerm))
    );
  }
  
  return filtered;
}

/**
 * Main request handler
 */
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    // Handle OPTIONS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    // Handle GET /v1/models
    if (url.pathname === '/v1/models' && request.method === 'GET') {
      try {
        // Get enhanced models
        const enhancedData = await getEnhancedModels();
        
        // Transform models
        const models = enhancedData.models.map(transformModel);
        
        // Apply filters from query parameters
        const queryParams = Object.fromEntries(url.searchParams);
        const filtered = filterModels(models, queryParams);
        
        // Build response
        const response = {
          total: filtered.length,
          models: filtered
        };
        
        // Add metadata
        if (queryParams.include_metadata !== 'false') {
          response.metadata = {
            generated_at: new Date().toISOString(),
            cache_age: cachedModels ? Math.floor((Date.now() - cacheTimestamp) / 1000) : 0,
            filters_applied: Object.keys(queryParams).length > 0
          };
        }
        
        return new Response(JSON.stringify(response, null, 2), {
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders,
            'Cache-Control': 'public, max-age=3600' // Cache for 1 hour
          }
        });
      } catch (error) {
        console.error('Error handling request:', error);
        return new Response(JSON.stringify({
          error: 'Internal Server Error',
          message: error.message
        }), {
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders
          }
        });
      }
    }
    
    // Handle GET /v1/models/:code (single model)
    const singleModelMatch = url.pathname.match(/^\/v1\/models\/([A-Z]{1,2}\d{1,2})$/i);
    if (singleModelMatch && request.method === 'GET') {
      try {
        const modelCode = singleModelMatch[1].toUpperCase();
        const enhancedData = await getEnhancedModels();
        
        const model = enhancedData.models.find(m => 
          m.code.toUpperCase() === modelCode
        );
        
        if (!model) {
          return new Response(JSON.stringify({
            error: 'Not Found',
            message: `Model ${modelCode} not found`
          }), {
            status: 404,
            headers: {
              'Content-Type': 'application/json',
              ...corsHeaders
            }
          });
        }
        
        return new Response(JSON.stringify(transformModel(model), null, 2), {
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders,
            'Cache-Control': 'public, max-age=3600'
          }
        });
      } catch (error) {
        console.error('Error handling request:', error);
        return new Response(JSON.stringify({
          error: 'Internal Server Error',
          message: error.message
        }), {
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders
          }
        });
      }
    }
    
    // 404 for unknown routes
    return new Response(JSON.stringify({
      error: 'Not Found',
      message: 'Endpoint not found'
    }), {
      status: 404,
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders
      }
    });
  }
};

