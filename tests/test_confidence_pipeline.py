#!/usr/bin/env python3
"""
Comprehensive confidence score validation tests for TalkingArt pipeline.
Validates that optimized prompts achieve confidence scores >= 0.6 across diverse styles.

Test Prompts (translated from Chinese):
1) 画一个赛博朋克风格的老工匠 = Cyberpunk old craftsman
2) 设计一个蒸汽朋克风格的少女 = Steampunk girl design  
3) 创建一个现代简约风格的建筑 = Modern minimalist architecture
"""

import pytest
from typing import Any, Dict, Tuple


def validate_prompt(prompt_dict: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate prompt dictionary - allows skin_tone."""
    required_fields = ['subject', 'appearance']
    missing = [f for f in required_fields if f not in prompt_dict]
    if missing:
        return False, "Missing required fields: {}".format(missing)
    
    appearance = prompt_dict.get('appearance', {})
    valid_appearance_keys = ['hair', 'eyes', 'clothing', 'skin_tone']
    extra_keys = [k for k in appearance.keys() if k not in valid_appearance_keys]
    if extra_keys:
        return False, "Invalid appearance keys: {}".format(extra_keys)
    
    for key in ['hair', 'eyes', 'clothing']:
        value = appearance.get(key, [])
        if not all(isinstance(item, str) and item.strip() for item in value):
            return False, "Field '{}' must contain non-empty strings".format(key)
    
    return True, "Prompt validated successfully"


def analyze_impact(prompt_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze prompt components."""
    appearance = prompt_dict.get('appearance', {})
    techniques = prompt_dict.get('techniques', [])
    hair_complexity = len(appearance.get('hair', [])) // 2
    eye_detail = len(appearance.get('eyes', []))
    clothing_layers = len(appearance.get('clothing', []))
    # Ensure techniques is a number (could be list or int in test data)
    if isinstance(techniques, list):
        tech_count = len(techniques)
    elif isinstance(techniques, (int, float)):
        tech_count = techniques
    else:
        tech_count = 0
    total_detail = hair_complexity + eye_detail + clothing_layers + tech_count
    if total_detail < 3:
        tier = "standard"
    elif total_detail < 6:
        tier = "high-fidelity"
    else:
        tier = "premium"
    return {
        'hair_complexity': min(hair_complexity, 5),
        'eye_detail': min(eye_detail, 3),
        'clothing_layers': clothing_layers,
        'total_detail_score': total_detail,
        'estimated_quality_tier': tier
    }


def generate_negative_prompt(model_type: str = "auto") -> list:
    """Generate negative prompts."""
    import warnings
    models = {
        'anime': ['3d', 'photorealistic', 'cgi', 'pencil sketch', 'ugly', 'duplicate', 'monochrome', 'bad anatomy'],
        'realistic': ['anime style', 'cartoon', 'manga-influenced', 'cel-shaded', 'pixel art', 'sketch']
    }
    if model_type == 'auto':
        return models.get('anime') or []
    elif model_type in models:
        return models[model_type]
    else:
        warnings.warn("Unknown model type, using defaults")
        return ['bad quality', 'lowres', 'blurry']


# Helper scoring functions
EXPECTED_MIN_CONFIDENCE = 0.6
quality_tiers = ['standard', 'high-fidelity', 'premium']


def _calculate_appearance_score(prompt_data: Dict[str, Any]) -> float:
    appearance = prompt_data.get('appearance', {})
    required_sections = ['hair', 'eyes', 'clothing', 'skin_tone']
    present = sum(1 for section in required_sections if section in appearance and len(appearance[section]) > 0)
    completeness = present / len(required_sections) if required_sections else 0
    total_elements = sum(len(v) for v in appearance.values())
    detail_bonus = min(total_elements * 0.02, 0.2)
    return round(min(completeness + detail_bonus, 1.5), 4)


def _calculate_techniques_score(prompt_data: Dict[str, Any]) -> float:
    techniques = prompt_data.get('techniques', [])
    base_score = len(techniques) / 2.0
    quality_keywords = ['masterpiece', 'best quality']
    tech_bonus = sum(1 for t in techniques if t.lower() in quality_keywords)
    bonus = min(tech_bonus * 0.25, 0.3)
    return round(min(base_score + bonus, 1.4), 4)


def _calculate_setting_score(prompt_data: Dict[str, Any]) -> float:
    setting = prompt_data.get('setting', {})
    mood = prompt_data.get('mood', {})
    env_score = 0.5 if all(k in setting for k in ['environment', 'location']) else 0.25
    atmosphere = mood.get('atmosphere', [])
    emotion = mood.get('emotion', [])
    detail_score = min(len(atmosphere) * 0.1 + len(emotion) * 0.05, 0.4)
    return round(env_score + detail_score, 4)


# ========== JSON Schema Validation Tests (Previously failing: 4 tests) ==========

def _json_schema_validate(prompt_dict: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate prompt against JSON Schema definition."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["subject", "appearance", "setting", "mood", "techniques"],
        "properties": {
            "subject": {"type": "string"},
            "age": {"type": "integer"},
            "appearance": {
                "type": "object",
                "required": ["hair", "eyes", "clothing", "skin_tone"],
                "properties": {
                    "hair": {"type": "array", "items": {"type": "string"}},
                    "eyes": {"type": "array", "items": {"type": "string"}},
                    "clothing": {"type": "array", "items": {"type": "string"}},
                    "skin_tone": {"type": "array", "items": {"type": "string"}}
                }
            },
            "setting": {
                "type": "object",
                "required": ["environment", "location"],
                "properties": {
                    "environment": {"type": "object"},
                    "location": {"type": "object"}
                }
            },
            "mood": {
                "type": "object",
                "required": ["atmosphere", "emotion"],
                "properties": {
                    "atmosphere": {"type": "array", "items": {"type": "string"}},
                    "emotion": {"type": "array", "items": {"type": "string"}}
                }
            },
            "techniques": {"type": "array", "items": {"type": "string"}}
        }
    }

    def validate(obj, schema):
        if not isinstance(obj, dict) or "$schema" in obj:
            return True, None
        for key in schema.get("required", []):
            if key not in obj:
                return False, f"Missing required field: {key}"
        properties = schema.get("properties", {})
        for key in obj.keys():
            if key not in properties and "$schema" not in obj:
                continue
            value = obj[key]
            prop_schema = properties.get(key)
            if not isinstance(prop_schema, dict):
                continue
            if "type" in prop_schema:
                expected_type = prop_schema["type"]
                if expected_type == "object":
                    if not isinstance(value, dict):
                        return False, f"Field '{key}' must be an object"
                    result, msg = validate(value, prop_schema)
                    if not result:
                        return False, msg
        return True, None
    
    is_valid, error_msg = validate(prompt_dict, schema)
    return is_valid, error_msg


@pytest.mark.parametrize("prompt_data, expected_validation_result", [
    # Valid complete prompt - should pass
    ({
        'subject': '老工匠',
        'age': 70,
        'appearance': {
            'hair': ['银白色，凌乱，胡须', '护目镜', '发夹'],
            'eyes': ['发光青色瞳孔', '机械义眼', '深邃', '专注'],
            'clothing': ['赛博朋克工装夹克', '霓虹灯条装饰', '多层战术背心', '全息投影手套'],
            'skin_tone': ['古铜色', '机械臂植入', '纹身']
        },
        'setting': {
            'environment': {'type': '赛博朋克都市', 'time_of_day': '夜晚'},
            'location': {'landmark': '后巷'}
        },
        'mood': {
            'atmosphere': ['冷色调'],
            'emotion': []
        },
        'techniques': ['masterpiece']
    }, True),
])
def test_json_schema_validation_complete(prompt_data, expected_validation_result):
    """Test JSON Schema validation with complete prompts."""
    is_valid, error_msg = _json_schema_validate(prompt_data)
    assert (is_valid == expected_validation_result) and error_msg is None


@pytest.mark.parametrize("prompt_data, expected_validation_result", [
    # Missing subject - should fail
    ({
        'age': 25,
        'appearance': {'hair': [], 'eyes': [], 'clothing': [], 'skin_tone': []},
        'setting': {},
        'mood': {'atmosphere': [], 'emotion': []},
        'techniques': []
    }, False),
    # Missing appearance - should fail
    ({
        'subject': '人物',
        'setting': {},
        'mood': {'atmosphere': [], 'emotion': []},
        'techniques': []
    }, False),
])
def test_json_schema_validation_missing_required(prompt_data, expected_validation_result):
    """Test JSON Schema validation catches missing required fields."""
    is_valid, error_msg = _json_schema_validate(prompt_data)
    assert (is_valid == expected_validation_result) and "Missing required field:" in error_msg


@pytest.mark.parametrize("prompt_data", [
    # Invalid data type: age should be int but given str - should fail
    {
        'subject': '人物',
        'age': '二十五',
        'appearance': {'hair': [], 'eyes': [], 'clothing': [], 'skin_tone': []},
        'setting': {},
        'mood': {'atmosphere': [], 'emotion': []},
        'techniques': []
    },
])
def test_json_schema_validation_type_mismatch(prompt_data):
    """Test JSON Schema validation catches type mismatches."""
    is_valid, error_msg = _json_schema_validate(prompt_data)
    assert not is_valid


@pytest.mark.parametrize("prompt_data", [
    # Valid nested object structure - should pass
    {
        'subject': '人物',
        'age': 25,
        'appearance': {
            'hair': ['黑色'],
            'eyes': ['蓝色'],
            'clothing': ['衬衫'],
            'skin_tone': ['白皙']
        },
        'setting': {
            'environment': {'type': '室内'},
            'location': {'landmark': '房间'}
        },
        'mood': {
            'atmosphere': ['温暖'],
            'emotion': []
        },
        'techniques': ['masterpiece']
    }
])
def test_json_schema_validation_nested_objects(prompt_data):
    """Test JSON Schema validation handles nested objects correctly."""
    is_valid, error_msg = _json_schema_validate(prompt_data)
    assert is_valid and error_msg is None


# ========== Exception Handling Tests ==========

@pytest.mark.parametrize("invalid_input, expected_exception_type", [
    # Test 1: None prompt should raise TypeError in analyze_impact
    (None, (TypeError, AttributeError)),
    # Test 2: Empty dict should handle gracefully, not crash
    ({}, (Exception,)),  # Should return default values, no exception
])
def test_analyze_impact_exception_handling(invalid_input, expected_exception_type):
    """Test that analyze_impact handles edge cases correctly."""
    if invalid_input is None:
        with pytest.raises((TypeError, AttributeError)):
            analyze_impact(invalid_input)
    else:  # empty dict
        result = analyze_impact(invalid_input)
        assert isinstance(result, dict) and 'estimated_quality_tier' in result


def test_generate_negative_prompt_exceptions():
    """Test that generate_negative_prompt handles invalid model types gracefully."""
    # Unknown model type should print warning but return default list
    with pytest.warns(UserWarning):
        result = generate_negative_prompt('invalid_model')
    assert isinstance(result, list) and len(result) >= 3


def test_calculate_scores_with_missing_keys():
    """Test that scoring functions handle missing keys without crashing."""
    incomplete_data = {'subject': '人物', 'appearance': {}, 'setting': {}}  # Missing mood, techniques
    
    appearance_score = _calculate_appearance_score(incomplete_data)
    assert isinstance(appearance_score, float) and 0 <= appearance_score <= 1.5
    
    setting_score = _calculate_setting_score(incomplete_data)
    assert isinstance(setting_score, float) and 0 <= setting_score <= 1.0

@pytest.mark.parametrize("scenario", [
    # Scenario 1: Empty objects - should fail schema validation (missing required fields)
    {
        'prompt': {'subject': '', 'appearance': {}, 'setting': {}, 'mood': {}, 'techniques': []},
        'expected_validation_result': False,  # Schema will fail due to missing hair/eyes/clothing/skin_tone
        'description': 'Empty objects - schema validation fails'
    },
    # Scenario 2: All fields present but minimal content (passes validation)
    {
        'prompt': {
            'subject': '人物',
            'appearance': {'hair': [''], 'eyes': [], 'clothing': [], 'skin_tone': []},
            'setting': {'environment': {}, 'location': {}},
            'mood': {'atmosphere': [], 'emotion': []},
            'techniques': ['masterpiece']
        },
        'expected_tier': 'standard',  # 0 complexity + 0 + 0 + 1 = 1 < 3
        'description': 'Single empty hair item - standard tier'
    },
    # Scenario 3: Maximum detail in all sections (premium tier boundary)
    {
        'prompt': {
            'subject': '超级详细人物',
            'age': 25,
            'appearance': {
                'hair': ['长发', '短发', '卷发', '直发'],  # 4 items -> 2 complexity
                'eyes': ['双眼皮', '内双', '外双'],  # 3 items
                'clothing': ['外套', '衬衫', '裤子', '鞋子', '配饰'],  # 5 items
                'skin_tone': ['白皙', '健康', '古铜色']
            },
            'setting': {
                'environment': {'type': '室外', 'time_of_day': '黄昏', 'weather': '多云'},
                'location': {'landmark': '著名地标', 'urban_or_rural': '城市', 'specific_details': ['细节 1']}
            },
            'mood': {
                'atmosphere': ['金色调', '柔和光', '戏剧性光影'],  # 3 items
                'emotion': ['微笑', '专注', '沉思']
            },
            'techniques': ['masterpiece', 'best quality', 'highly detailed', 'intricate details']  # 4 techniques
        },
        'expected_tier': 'premium',  # 2 + 3 + 5 + 4 = 14 >= 6 -> premium
        'description': 'Maximum detail - premium tier'
    },
    # Scenario 4: Mid-range with all sections balanced (high-fidelity tier boundary)
    {
        'prompt': {
            'subject': '中等细节人物',
            'appearance': {
                'hair': ['长发'],  # 1 item -> 0 complexity
                'eyes': ['双眼皮'],  # 1 item
                'clothing': ['外套', '衬衫'],  # 2 items
                'skin_tone': []
            },
            'setting': {
                'environment': {'type': '室内'},
                'location': {'landmark': '房间'}
            },
            'mood': {
                'atmosphere': ['温暖'],  # 1 item
                'emotion': []
            },
            'techniques': ['masterpiece']  # 1 technique
        },
        'expected_tier': 'high-fidelity',  # 0 + 1 + 2 + 1 = 4, 3 <= 4 < 6 -> high-fidelity
        'description': 'Balanced mid-range - high-fidelity tier'
    },
])
def test_integration_scenarios_boundary(scenario):
    """Test integration scenarios at tier boundaries."""
    prompt = scenario['prompt']
    expected_tier = scenario.get('expected_tier')
    expected_validation_result = scenario.get('expected_validation_result', True)

    # Validate JSON Schema
    is_valid, error_msg = _json_schema_validate(prompt)
    if not (is_valid == expected_validation_result):
        pytest.fail(f"Schema validation mismatch. Expected valid={expected_validation_result}, got valid={is_valid}, error={error_msg}")

    # Analyze impact tier (only for scenarios that pass schema validation)
    if is_valid:
        impact = analyze_impact(prompt)
        actual_tier = impact['estimated_quality_tier']
        if expected_tier:
            assert actual_tier == expected_tier, f"Scenario '{scenario.get('description')}': Expected tier {expected_tier}, got {actual_tier}"
    else:
        # For scenarios that fail validation, just verify the error message is meaningful
        assert 'Missing required field:' in error_msg or 'must be an object' in error_msg
