#!/usr/bin/env python3
"""
SY19 Enhanced with Vertex AI

Enhanced version of SY19 that uses Vertex AI for better primary model detection
and recommendation explanations.

Usage:
    python tools/sy19_vertex_ai.py "problem description"
    python tools/sy19_vertex_ai.py "problem" --model gemini-pro
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import re

# Import base SY19 recommender
sys.path.insert(0, str(Path(__file__).parent))
from sy19_recommend import SY19Recommender

# Import ModelLoader for loading model descriptions
try:
    from validate_relationships import ModelLoader
except ImportError:
    # Fallback if validate_relationships not available
    class ModelLoader:
        def __init__(self, models_dir=None):
            self.cache = {}
        def load_model(self, model_code):
            return None

try:
    import vertexai
    try:
        from vertexai.generative_models import GenerativeModel
        USE_GENERATIVE_MODEL = True
    except ImportError:
        from vertexai.preview.language_models import TextGenerationModel
        USE_GENERATIVE_MODEL = False
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    USE_GENERATIVE_MODEL = False
    print("Warning: Vertex AI not available. Install with: pip install vertexai", file=sys.stderr)

# Try Google Generative AI SDK (uses API keys)
try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False


class SY19VertexAIRecommender(SY19Recommender):
    """Enhanced SY19 recommender with Vertex AI for better primary detection."""
    
    def __init__(
        self,
        relationships_json: str,
        vertex_ai_model: str = "gemini-2.0-flash",
        project_id: Optional[str] = None,
        location: str = "us-central1",
        use_api_key: bool = False,
        api_key: Optional[str] = None
    ):
        """Initialize with Vertex AI support.
        
        Args:
            relationships_json: Path to relationships JSON file
            vertex_ai_model: Model name (e.g., "gemini-1.5-flash")
            project_id: GCP project ID (defaults to GOOGLE_CLOUD_PROJECT env var)
            location: GCP region (default: us-central1)
            use_api_key: If True, use Google AI SDK with API key instead of Vertex AI
            api_key: API key for Google AI SDK (defaults to GOOGLE_API_KEY env var)
        """
        super().__init__(relationships_json)
        
        self.use_api_key = use_api_key
        self.vertex_ai_model = vertex_ai_model
        
        # Load model descriptions
        self.model_loader = ModelLoader()
        self.model_cache = {}
        
        if use_api_key:
            # Use Google AI SDK with API key
            if not GOOGLE_AI_AVAILABLE:
                raise ImportError("Google Generative AI SDK not installed. Install with: pip install google-generativeai")
            
            api_key = api_key or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set. Set it or pass api_key parameter.")
            
            genai.configure(api_key=api_key)
            self.llm = genai.GenerativeModel(vertex_ai_model)
            self.use_google_ai_sdk = True
            self.use_generative_api = False  # Different API structure
        else:
            # Use Vertex AI SDK with Application Default Credentials
            if not VERTEX_AI_AVAILABLE:
                raise ImportError("Vertex AI packages not installed. Install with: pip install vertexai")
            
            # Initialize Vertex AI
            self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
            if not self.project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
            
            vertexai.init(project=self.project_id, location=location)
            
            # Use GenerativeModel API for Gemini models
            if USE_GENERATIVE_MODEL:
                self.llm = GenerativeModel(vertex_ai_model)
                self.use_generative_api = True
            else:
                # Fallback to TextGenerationModel for older models
                self.llm = TextGenerationModel.from_pretrained(vertex_ai_model)
                self.use_generative_api = False
            
            self.use_google_ai_sdk = False
    
    def _detect_primaries_llm(self, problem_text: str) -> List[str]:
        """Use Vertex AI to detect primary models from problem description with few-shot examples."""
        
        # Few-shot examples from case studies
        examples = """
Examples:
Problem: "Multi-service AI system with bottlenecks and cascades"
Primaries: DE07, DE06, P02
Reasoning: DE07 (Bottlenecks) and DE06 (Failure Modes) for breakdown, P02 (Stakeholder Mapping) for context

Problem: "Distributed system experiencing latency spikes and timeouts"
Primaries: DE07, DE06, SY04
Reasoning: DE07 (Bottlenecks) to find where work piles up, DE06 (Failure Modes) to understand failure patterns, SY04 (Cascade Analysis) to trace propagation

Problem: "Planning a complex project with unclear dependencies"
Primaries: DE01, P01, CO01
Reasoning: DE01 (Root Cause Analysis) to break down, P01 (First Principles) to strip assumptions, CO01 (Composition) to understand dependencies
"""
        
        prompt = f"""You are an expert in the HUMMBL framework, which has 120 mental models organized into 6 transformations:

P (Perspective) - 20 models: P01-P20 - Perspective shifts, stakeholder mapping, reframing
IN (Inversion) - 20 models: IN01-IN20 - Failure modes, premortems, adversarial thinking
CO (Composition) - 20 models: CO01-CO20 - Composing systems, pipelines, architectures
DE (Decomposition) - 20 models: DE01-DE20 - Breaking down problems, finding bottlenecks, analyzing failures
RE (Recursion) - 20 models: RE01-RE20 - Iterative refinement, feedback loops, recursive patterns
SY (Synthesis) - 20 models: SY01-SY20 - System thinking, cascades, meta-analysis

{examples}

Given this engineering problem: "{problem_text}"

Which 3 HUMMBL mental models are most directly relevant as starting points?

Return ONLY a comma-separated list of 3 model codes (e.g., "DE07, IN02, SY01").
Do not include explanations or other text."""

        try:
            if self.use_google_ai_sdk:
                # Use Google AI SDK (API key based)
                response = self.llm.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 50,
                        "temperature": 0.2
                    }
                )
                text = response.text.strip()
            elif self.use_generative_api:
                # Use Vertex AI GenerativeModel API
                response = self.llm.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 50,
                        "temperature": 0.2
                    }
                )
                text = response.text.strip()
            else:
                # Use Vertex AI TextGenerationModel API
                response = self.llm.predict(
                    prompt,
                    max_output_tokens=50,
                    temperature=0.2
                )
                text = response.text.strip()
            
            # Extract model codes from response
            # Remove quotes if present
            text = text.strip('"\'')
            
            # Extract model codes (format: DE07, IN02, SY01)
            model_codes = re.findall(r'([A-Z]{1,2}\d{1,2})', text)
            
            # Validate codes exist
            valid_codes = [code for code in model_codes if code in self.all_models]
            
            return valid_codes[:3]  # Return top 3
            
        except Exception as e:
            print(f"Warning: Vertex AI detection failed: {e}", file=sys.stderr)
            print("Falling back to keyword-based detection", file=sys.stderr)
            return self._detect_primaries_from_text(problem_text)
    
    def recommend_models(
        self,
        problem_text: str,
        primaries: Optional[List[str]] = None,
        top_k: int = 7,
        max_hops: int = 2,
        use_llm: bool = True
    ) -> List[Dict]:
        """
        Recommend models with optional Vertex AI enhancement.
        
        Args:
            problem_text: Problem description
            primaries: Optional explicit primaries (overrides detection)
            top_k: Number of recommendations
            max_hops: Maximum graph distance
            use_llm: Use Vertex AI for primary detection (default: True)
        """
        # Detect primaries using LLM if requested
        if primaries is None and use_llm:
            primaries = self._detect_primaries_llm(problem_text)
        
        # Fall back to parent class method
        return super().recommend_models(
            problem_text=problem_text,
            primaries=primaries,
            top_k=top_k,
            max_hops=max_hops
        )
    
    def explain_recommendation(self, model_code: str, problem_text: str, relationships: Optional[List[Dict]] = None) -> str:
        """Use Vertex AI to generate explanation for why a model is recommended."""
        # Get model info
        model_info = self._get_model_info(model_code)
        if not model_info:
            return f"Model {model_code} recommended based on relationship graph."
        
        # Get relationship context
        rel_context = ""
        if relationships:
            rel_descriptions = []
            for rel in relationships[:3]:  # Top 3 relationships
                rel_type = rel.get('type', '')
                from_model = rel.get('from', '')
                to_model = rel.get('to', '')
                strength = rel.get('strength', 0)
                if to_model == model_code:
                    rel_descriptions.append(f"{from_model} → {model_code} ({rel_type}, strength={strength:.2f})")
            if rel_descriptions:
                rel_context = f"\nConnected via: {', '.join(rel_descriptions)}"
        
        prompt = f"""Given this problem: "{problem_text}"

HUMMBL Model: {model_code} - {model_info.get('name', 'Unknown')}
Description: {model_info.get('description', 'No description')[:200]}{rel_context}

Explain in 2-3 sentences why this model is relevant to the problem. Reference specific aspects of the problem and how the model addresses them."""

        try:
            if self.use_google_ai_sdk:
                # Use Google AI SDK (API key based)
                response = self.llm.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 150,
                        "temperature": 0.3
                    }
                )
                return response.text.strip()
            elif self.use_generative_api:
                # Use Vertex AI GenerativeModel API
                response = self.llm.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 150,
                        "temperature": 0.3
                    }
                )
                return response.text.strip()
            else:
                # Use Vertex AI TextGenerationModel API
                response = self.llm.predict(
                    prompt,
                    max_output_tokens=150,
                    temperature=0.3
                )
                return response.text.strip()
        except Exception as e:
            return f"Model {model_code} recommended based on relationship graph analysis."
    
    def _get_model_info(self, model_code: str) -> Optional[Dict]:
        """Get model information from model files."""
        if model_code in self.model_cache:
            return self.model_cache[model_code]
        
        model_info = self.model_loader.load_model(model_code)
        if model_info:
            self.model_cache[model_code] = model_info
            return model_info
        
        # Fallback to basic info
        return {
            'code': model_code,
            'name': f"Model {model_code}",
            'description': "Model description not available"
        }
    
    def suggest_sequence(self, problem_text: str, recommended_models: List[str], max_length: int = 8) -> List[str]:
        """Use Vertex AI to suggest an operator sequence from recommended models."""
        if not recommended_models:
            return []
        
        # Get model info for context
        model_descriptions = []
        for model_code in recommended_models[:10]:  # Top 10 for context
            model_info = self._get_model_info(model_code)
            name = model_info.get('name', model_code)
            desc = model_info.get('description', '')[:100]
            model_descriptions.append(f"{model_code} ({name}): {desc}")
        
        models_context = "\n".join(model_descriptions)
        
        prompt = f"""Given this problem: "{problem_text}"

And these recommended HUMMBL models:
{models_context}

Suggest an optimal operator sequence (3-{max_length} models) that would effectively address this problem.

Consider:
- Start with decomposition (DE) or perspective (P) models to understand the problem
- Use inversion (IN) models to identify failure modes
- Apply composition (CO) models to design solutions
- Use recursion (RE) models for iterative refinement
- End with synthesis (SY) models to integrate insights

Return ONLY a comma-separated list of model codes in suggested order (e.g., "P02, DE07, DE06, CO03, SY01").
Do not include explanations."""
        
        try:
            if self.use_google_ai_sdk:
                response = self.llm.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 100,
                        "temperature": 0.3
                    }
                )
                text = response.text.strip()
            elif self.use_generative_api:
                response = self.llm.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 100,
                        "temperature": 0.3
                    }
                )
                text = response.text.strip()
            else:
                response = self.llm.predict(
                    prompt,
                    max_output_tokens=100,
                    temperature=0.3
                )
                text = response.text.strip()
            
            # Extract model codes
            text = text.strip('"\'')
            model_codes = re.findall(r'([A-Z]{1,2}\d{1,2})', text)
            
            # Validate and filter to recommended models
            valid_sequence = [code for code in model_codes if code in recommended_models]
            
            # Limit length
            return valid_sequence[:max_length]
            
        except Exception as e:
            print(f"Warning: Sequence suggestion failed: {e}", file=sys.stderr)
            # Fallback: return recommended models in order
            return recommended_models[:max_length]


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SY19 Enhanced with Vertex AI - Recommend HUMMBL models"
    )
    parser.add_argument(
        "problem",
        help="Problem description in natural language"
    )
    parser.add_argument(
        "--primaries", "-p",
        nargs="+",
        help="Explicit primary models (overrides LLM detection)"
    )
    parser.add_argument(
        "--top", "-k",
        type=int,
        default=7,
        help="Number of recommendations (default: 7)"
    )
    parser.add_argument(
        "--relationships", "-r",
        default="data/relationships.json",
        help="Path to relationships.json (default: data/relationships.json)"
    )
    parser.add_argument(
        "--model",
        default="gemini-2.0-flash",
        help="Vertex AI model to use (default: gemini-2.0-flash). Options: gemini-2.0-flash, gemini-2.5-flash, gemini-flash-latest, gemini-pro-latest"
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Disable LLM and use keyword-based detection"
    )
    parser.add_argument(
        "--use-api-key",
        action="store_true",
        help="Use Google AI SDK with API key instead of Vertex AI (requires GOOGLE_API_KEY env var)"
    )
    parser.add_argument(
        "--api-key",
        help="API key for Google AI SDK (defaults to GOOGLE_API_KEY env var)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for recommendations"
    )
    
    args = parser.parse_args()
    
    # Check availability based on authentication method
    if args.use_api_key:
        if not GOOGLE_AI_AVAILABLE:
            print("Error: Google Generative AI SDK not available. Install with: pip install google-generativeai", file=sys.stderr)
            sys.exit(1)
    else:
        if not VERTEX_AI_AVAILABLE:
            print("Error: Vertex AI not available. Install with: pip install vertexai", file=sys.stderr)
            sys.exit(1)
    
    try:
        # Create enhanced recommender
        recommender = SY19VertexAIRecommender(
            relationships_json=args.relationships,
            vertex_ai_model=args.model,
            use_api_key=args.use_api_key,
            api_key=args.api_key
        )
        
        # Get recommendations
        recommendations = recommender.recommend_models(
            problem_text=args.problem,
            primaries=args.primaries,
            top_k=args.top,
            use_llm=not args.no_llm
        )
        
        # Get recommended model codes
        recommended_model_codes = [rec['model'] for rec in recommendations]
        
        # Suggest sequence if LLM is enabled
        suggested_sequence = []
        if not args.no_llm and recommended_model_codes:
            try:
                suggested_sequence = recommender.suggest_sequence(
                    args.problem,
                    recommended_model_codes,
                    max_length=8
                )
            except Exception as e:
                print(f"Warning: Could not generate sequence suggestion: {e}", file=sys.stderr)
        
        # Format output
        lines = [
            f"# SY19 Model Recommendations (Vertex AI Enhanced)",
            f"",
            f"**Problem:** {args.problem}",
            f"**Model:** {args.model}",
            f"",
        ]
        
        # Add suggested sequence if available
        if suggested_sequence:
            sequence_str = " → ".join(suggested_sequence)
            lines.append(f"## Suggested Operator Sequence")
            lines.append(f"")
            lines.append(f"`{sequence_str}`")
            lines.append(f"")
        
        lines.extend([
            f"## Recommended Models (Top {len(recommendations)})",
            f"",
        ])
        
        for i, rec in enumerate(recommendations, 1):
            primary_tag = " 🔹 Primary" if rec['is_primary'] else ""
            lines.append(f"{i}. **{rec['model']}** (score: {rec['score']:.3f}){primary_tag}")
            lines.append(f"   - Centrality: {rec['centrality']} connections")
            
            # Add LLM explanation if available
            if not args.no_llm:
                # Get relationships for this model
                model_rels = [r for r in recommender.relationships 
                            if r['to'] == rec['model'] or r['from'] == rec['model']]
                explanation = recommender.explain_recommendation(
                    rec['model'], 
                    args.problem,
                    relationships=model_rels[:3]  # Top 3 relationships
                )
                lines.append(f"   - Why: {explanation}")
            elif rec['reasons']:
                lines.append(f"   - Why: {rec['reasons'][0]}")
            
            lines.append("")
        
        output = "\n".join(lines)
        
        # Write or print
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✓ Recommendations written to: {args.output}")
        else:
            print(output)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

