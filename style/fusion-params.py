# style/fusion-params.py
---
# Style Fusion Engine - Parameterized Style Mixing
schema_version: "1.0"
author: TalkingArtProject

# Algorithm Definitions (Python functions)
def create_fusion(base_style: str, accent_style: str = None) -> dict:
    """
    Create a style fusion prompt with parameters.
    
    Args:
        base_style: Primary style (e.g., 'anime', 'watercolor')
        accent_style: Secondary style to blend in
    
    Returns:
        Dictionary containing:
            - fusion_name: Combined style name
            - techniques: List of technical descriptors
            - color_palette: Suggested colors
            - example_prompt: Generated prompt string
    """
    
    # Style token database (expand as needed)
    style_tokens = {
        'anime': {
            'features': ['manga-influenced', 'cel-shaded', 'character-focused'],
            'colors': ['#FF6B9D', '#4A5F7C', '#FFE5D9'],
            'negative': ['3d', 'photorealistic', 'cgi']
        },
        'watercolor': {
            'features': ['wet-on-wet', 'transparent layers', 'soft edges'],
            'colors': ['#E8F4F8', '#FFD1DC', '#6B90A6'],
            'negative': ['digital art', 'vector graphics']
        },
        'oil_paint': {
            'features': ['impasto texture', 'visible brush strokes', 'thick paint application'],
            'colors': ['#5C4033', '#8B7355', '#D2691E'],
            'negative': ['smooth gradients']
        },
        'pixel_art': {
            'features': ['retro 8-bit', 'dithering', 'limited palette'],
            'colors': ['#00FF7F', '#FF6347', '#9370DB'],
            'negative': ['high resolution', 'smooth']
        },
        'ink_sketch': {
            'features': ['cross-hatching', 'charcoal shading', 'line weight variation'],
            'colors': ['#1C1C1C', '#808080', '#FFFFFF'],
            'negative': ['color']
        }
    }
    
    base = style_tokens.get(base_style.lower()) or {'features': [base_style]}
    accent = style_tokens.get(accent_style) if accent_style else {}
    
    # Generate fusion techniques
    primary_techniques = base['features']
    secondary_techniques = accent['features'] if accent else []
    combined_techniques = primary_techniques + secondary_techniques[:2]  # Mix 2 from each
    
    return {
        'fusion_name': f"{base_style.capitalize()} Fusion",
        'techniques': combined_techniques,
        'color_palette': base['colors'] if accent else [base['colors'][0], '#FFFFFF', '#000000'],
        'example_prompt': create_example_prompt(base_style, accent_style)
    }

# Example prompt generator (simplified version of full implementation)
def create_example_prompt(base: str, accent: str = None) -> str:
    """Generate an example prompt for the fusion style."""
    base_keywords = {
        'anime': ['manga-influenced', 'cel-shaded'],
        'watercolor': ['wet-on-wet', 'transparent layers'],
        'oil_paint': ['impasto texture', 'visible brush strokes'],
        'pixel_art': ['retro 8-bit', 'dithering']
    }
    
    primary = base_keywords.get(base.lower(), [base])
    secondary = accent_keywords[accent.lower()] if accent else []
    
    return f"masterpiece, best quality, {primary[0]}, {secondary[0] if secondary else 'highly detailed'}"

# Color palette utilities (can be expanded with hex-to-rgb conversions)
def get_palette(base_style: str) -> list:
    """Return color palette for a given style."""
    return {
        'anime': ['#FF6B9D', '#4A5F7C', '#FFE5D9'],  # Hot pink, steel blue, peach
        'watercolor': ['#E8F4F8', '#FFD1DC', '#6B90A6'],
        'oil_paint': ['#5C4033', '#8B7355', '#D2691E'],
        'pixel_art': ['#00FF7F', '#FF6347', '#9370DB']
    }.get(base_style.lower(), ['#000000', '#FFFFFF', '#808080'])

# Usage examples:
if __name__ == "__main__":
    # Create anime + watercolor fusion
    result = create_fusion('anime', 'watercolor')
    print(f"Style: {result['fusion_name']}")
    print(f"Techniques: {result['techniques']}")
    print(f"Palette: {result['color_palette']}")
