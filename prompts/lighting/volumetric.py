# prompts/lighting/volumetric.py
---
type: volumetric_effects
schema_version: "1.0"
author: TalkingArtProject

# Volumetric Lighting Effect Descriptions (prompts/lighting/volumetric.py)
def generate_volumetric_prompt(environment: str, particle_type: str = 'dust') -> dict:
    """
    Generate volumetric lighting effect for specific environment.
    
    Args:
        environment: Location context ('urban', 'industrial', 'natural')
        particle_type: Type of particles ('dust', 'rain', 'smoke', 'pollen')
    
    Returns:
        Dictionary with color_temp, particle_size, and description
    """
    
    # Environment-based temperature selection
    temp_lookup = {
        'urban': {'base': 4500, 'range': (3200, 6500)},
        'industrial': {'base': 3800, 'range': (2800, 5000)},
        'natural': {'base': 5500, 'range': (4000, 7000)}
    }
    
    # Particle characteristics
    particle_data = {
        'dust': {
            'size': 'fine',
            'color_cast': 'warm',
            'light_interaction: ['scattering', 'golden hour enhancement']
        },
        'rain': {
            'size': 'medium droplets',
            'color_cast': 'cool blue tint',
            'light_interaction: ['reflections', 'volumetric rays']
        }
    }
    
    return {
        'environment': environment,
        'particle_type': particle_type,
        'color_temperature': temp_lookup.get(environment, {}).get('base'),
        'description': f"{particle_data[particle_type]['size']} particles creating {particle_data[particle_type]['light_interaction'][0]} effects"
    }

# Volumetric Lighting Effect Descriptions (prompts/lighting/volumetric.py)
volumetric:
  rain_lightning:
    description: "Rain and lightning effects for cyberpunk atmospheres"
    color_temperature: "5600K daylight mixed with storm gray"
    particle_size: "Small droplets catching light from sources"
  
  dust_motes:
    description: "Dust particles visible in light beams"
    works_with: ["low-angle", "side lighting"]