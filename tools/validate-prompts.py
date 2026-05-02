# tools/validate-prompts.py
---
# TalkingArt Prompt Validator - Schema Validation & Analysis
schema_version: "1.0"
author: TalkingArtProject
license: MIT

import json
import yaml
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def load_schema(schema_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load TalkingArt Schema from YAML file.
    
    Args:
        schema_path: Path to template.yaml (default: prompts/character/template.yaml)
    
    Returns:
        Dictionary containing the prompt structure
    """
    default_schema = "prompts/character/template.yaml"
    schema_file = Path(schema_path) if schema_path else default_schema
    
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_file}")
        sys.exit(1)


def validate_prompt(prompt_dict: Dict[str, Any], schema_path: Optional[str] = None) -> tuple[bool, str]:
    """
    Validate prompt dictionary against TalkingArt Schema.
    
    Args:
        prompt_dict: Prompt to validate (filled template)
        schema_path: Path to schema file
    
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    try:
        # Load required fields
        schema = load_schema(schema_path)
        required_fields = ['subject', 'appearance']
        techniques = schema.get('techniques', [])
        negative_prompts = schema.get('negative_prompt', {}).get('default', [])
        
        # Check required fields exist
        missing = [f for f in required_fields if f not in prompt_dict]
        if missing:
            error_msg = f"Missing required fields: {missing}"
            return False, error_msg
        
        # Validate appearance structure
        appearance = prompt_dict.get('appearance', {})
        valid_appearance_keys = ['hair', 'eyes', 'clothing']
        extra_keys = [k for k in appearance.keys() if k not in valid_appearance_keys]
        
        if extra_keys:
            error_msg = f"Invalid appearance keys: {extra_keys}"
            return False, error_msg
        
        # Validate arrays contain strings only (no empty values)
        for key in ['hair', 'eyes', 'clothing']:
            value = appearance.get(key, [])
            if not all(isinstance(item, str) and item.strip() for item in value):
                error_msg = f"Field '{key}' must contain non-empty strings"
                return False, error_msg
        
        # Check techniques (optional but recommended)
        if prompt_dict.get('techniques') != techniques:
            warning = "Techniques do not match schema defaults. This may affect quality."
            # Log as warning or info depending on config
    except Exception as e:
        return False, f"Validation error: {str(e)}"
    
    return True, "Prompt validated successfully"


def analyze_impact(prompt_dict: Dict[str, Any]) -> Dict[str, list]:
    """
    Analyze prompt components and predict impact on generation.
    
    Args:
        prompt_dict: Validated prompt dictionary
    
    Returns:
        Dictionary with analysis results
    """
    appearance = prompt_dict.get('appearance', {})
    techniques = prompt_dict.get('techniques', [])
    
    # Count complexity factors
    hair_complexity = len(appearance.get('hair', [])) // 2  # Rough estimate of detail level
    eye_detail = len(appearance.get('eyes', []))
    clothing_layers = len(appearance.get('clothing', []))
    
    # Total detail score (higher = more detailed)
    total_detail = hair_complexity + eye_detail + len(techniques)
    
    return {
        'hair_complexity': min(hair_complexity, 5),  # Cap at 5
        'eye_detail': min(eye_detail, 3),
        'clothing_layers': clothing_layers,
        'total_detail_score': total_detail,
        'estimated_quality_tier': get_quality_tier(total_detail)
    }


def get_quality_tier(detail_score: int) -> str:
    """
    Map detail score to quality tier.
    
    Args:
        detail_score: From analyze_impact() function
    
    Returns:
        Quality tier string (basic, standard, high-fidelity)
    """
    if detail_score < 3:
        return "standard"
    elif detail_score < 6:
        return "high-fidelity"
    else:
        return "premium"


def generate_negative_prompt(model_type: str = "auto") -> list[str]:
    """
    Generate appropriate negative prompt based on model type.
    
    Args:
        model_type: 'anime', 'realistic', or 'auto'
    
    Returns:
        List of negative prompt keywords
    """
    models = {
        'anime': [
            '3d', 'photorealistic', 'cgi', 'pencil sketch',
            'ugly', 'duplicate', 'monochrome', 'bad anatomy'
        ],
        'realistic': [
            'anime style', 'cartoon', 'manga-influenced',
            'cel-shaded', 'pixel art', 'sketch'
        ]
    }
    
    if model_type == 'auto':
        # Default to anime for TalkingArt (SDXL/Niji)
        return models.get('anime') or []
    elif model_type in models:
        return models[model_type]
    else:
        print(f"Warning: Unknown model type '{model_type}', using defaults")
        return ['bad quality', 'lowres', 'blurry']


if __name__ == "__main__":
    # Example usage
    test_prompt = {
        "subject": "Cyberpunk Ninja",
        "age": 25,
        "appearance": {
            "hair": ["black", "short", "messy"],
            "eyes": ["slit pupils", "glowing blue"],
            "clothing": ["tactical vest", "neon accents"]
        },
        "techniques": [
            "masterpiece",
            "best quality"
        ]
    }
    
    is_valid, message = validate_prompt(test_prompt)
    print(f"Valid: {is_valid}")
    print(message)
    
    if is_valid:
        analysis = analyze_impact(test_prompt)
        print(f"Impact Analysis: {analysis}")
