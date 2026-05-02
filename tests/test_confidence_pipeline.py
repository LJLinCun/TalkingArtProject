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


def validate_prompt(prompt_dict):
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


def analyze_impact(prompt_dict):
    """Analyze prompt components."""
    appearance = prompt_dict.get('appearance', {})
    techniques = prompt_dict.get('techniques', [])
    hair_complexity = len(appearance.get('hair', [])) // 2
    eye_detail = len(appearance.get('eyes', []))
    clothing_layers = len(appearance.get('clothing', []))
    total_detail = hair_complexity + eye_detail + len(techniques)
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


def generate_negative_prompt(model_type="auto"):
    """Generate negative prompts."""
    models = {
        'anime': ['3d', 'photorealistic', 'cgi', 'pencil sketch', 'ugly', 'duplicate', 'monochrome', 'bad anatomy'],
        'realistic': ['anime style', 'cartoon', 'manga-influenced', 'cel-shaded', 'pixel art', 'sketch']
    }
    if model_type == 'auto':
        return models.get('anime') or []
    elif model_type in models:
        return models[model_type]
    else:
        print("Warning: Unknown model type, using defaults")
        return ['bad quality', 'lowres', 'blurry']


# Test fixtures
@pytest.fixture
def sample_prompt():
    """Return a sample prompt for testing."""
    return {
        'subject': '测试人物',
        'appearance': {
            'hair': ['黑色短发'],
            'eyes': ['蓝色'],
            'clothing': ['白色衬衫']
        }
    }


@pytest.fixture
def invalid_prompt():
    """Return an invalid prompt for error handling tests."""
    return {
        'subject': '测试人物'
        # missing 'appearance' field
    }


# Helper scoring functions
EXPECTED_MIN_CONFIDENCE = 0.6
quality_tiers = ['standard', 'high-fidelity', 'premium']


def _calculate_appearance_score(prompt_data):
    appearance = prompt_data.get('appearance', {})
    required_sections = ['hair', 'eyes', 'clothing', 'skin_tone']
    present = sum(1 for section in required_sections if section in appearance and len(appearance[section]) > 0)
    completeness = present / len(required_sections) if required_sections else 0
    total_elements = sum(len(v) for v in appearance.values())
    detail_bonus = min(total_elements * 0.02, 0.2)
    return round(min(completeness + detail_bonus, 1.5), 4)


def _calculate_techniques_score(prompt_data):
    techniques = prompt_data.get('techniques', [])
    base_score = len(techniques) / 2.0
    quality_keywords = ['masterpiece', 'best quality']
    tech_bonus = sum(1 for t in techniques if t.lower() in quality_keywords)
    bonus = min(tech_bonus * 0.25, 0.3)
    return round(min(base_score + bonus, 1.4), 4)


def _calculate_setting_score(prompt_data):
    setting = prompt_data.get('setting', {})
    mood = prompt_data.get('mood', {})
    env_score = 0.5 if all(k in setting for k in ['environment', 'location']) else 0.25
    atmosphere = mood.get('atmosphere', [])
    emotion = mood.get('emotion', [])
    detail_score = min(len(atmosphere) * 0.1 + len(emotion) * 0.05, 0.4)
    return round(env_score + detail_score, 4)


# Test cases - parameterized tests
@pytest.mark.parametrize("prompt_data, expected_result", [
    # Valid prompts with all required fields
    ({
        'subject': '人物',
        'appearance': {
            'hair': ['黑色短发'],
            'eyes': ['蓝色'],
            'clothing': ['白色衬衫']
        }
    }, True),
    ({
        'subject': '人物',
        'age': 25,
        'appearance': {
            'hair': ['金色长发'],
            'eyes': ['绿色', '双眼皮'],
            'clothing': ['红色连衣裙'],
            'skin_tone': ['白皙']
        }
    }, True),
])
def test_validate_prompt_valid(prompt_data, expected_result):
    """Test validate_prompt with valid prompts."""
    is_valid, msg = validate_prompt(prompt_data)
    assert is_valid == expected_result


@pytest.mark.parametrize("prompt_data", [
    ({'subject': '人物'}, False),  # missing appearance
    ({'appearance': {'hair': ['黑色']}}, False),  # missing subject
])
def test_validate_prompt_invalid(prompt_data):
    """Test validate_prompt with invalid prompts."""
    is_valid, msg = validate_prompt(prompt_data)
    assert not is_valid


@pytest.mark.parametrize("prompt_data, expected_tier", [
    # Low detail - standard tier (0 complexity + 0 + 0 + 0 = 0 < 3)
    ({
        'subject': '简单',
        'appearance': {
            'hair': [],
            'eyes': [],
            'clothing': []
        },
        'techniques': []
    }, 'standard'),
    # Medium detail - high-fidelity tier (1 complexity + 1 + 1 + 1 = 4, 3 <= 4 < 6)
    ({
        'subject': '中等',
        'appearance': {
            'hair': ['黑色短发', '发夹'],  # 2 items -> 1 complexity
            'eyes': ['蓝色', '双眼皮'],  # 2 items
            'clothing': ['白色衬衫']  # 1 item
        },
        'techniques': ['masterpiece']  # 1 technique
    }, 'high-fidelity'),
])
def test_analyze_impact(prompt_data, expected_tier):
    """Test analyze_impact tier classification."""
    result = analyze_impact(prompt_data)
    assert result['estimated_quality_tier'] == expected_tier


@pytest.mark.parametrize("prompt_data, min_confidence", [
    # Prompt 1 - Cyberpunk old craftsman (high confidence expected)
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
            'environment': {'type': '赛博朋克都市', 'time_of_day': '夜晚', 'weather': '酸雨'},
            'location': {
                'landmark': '霓虹灯广告牌林立的后巷',
                'urban_or_rural': '高度城市化',
                'specific_details': '全息广告、蒸汽管道'
            }
        },
        'mood': {
            'atmosphere': ['冷色调', '蓝紫色调', '霓虹光影'],
            'emotion': ['机械义肢轻敲工作台', '专注的神情', '手持全息图纸']
        },
        'techniques': ['masterpiece', 'best quality', 'highly detailed', 'intricate details', 'cyberpunk style']
    }, 0.9),
])
def test_confidence_threshold(prompt_data, min_confidence):
    """Test that prompt achieves minimum confidence threshold."""
    appearance_score = _calculate_appearance_score(prompt_data)
    techniques_score = _calculate_techniques_score(prompt_data)
    setting_score = _calculate_setting_score(prompt_data)
    raw_confidence = (appearance_score * 0.35 + techniques_score * 0.40 + setting_score * 0.25)
    assert raw_confidence >= min_confidence, f"Confidence {raw_confidence:.4f} below threshold {min_confidence}"


@pytest.mark.parametrize("model_type", ['anime', 'realistic', 'auto'])
def test_generate_negative_prompt(model_type):
    """Test negative prompt generation for different model types."""
    negative = generate_negative_prompt(model_type)
    assert isinstance(negative, list) and len(negative) > 0
    for keyword in negative:
        assert isinstance(keyword, str) and keyword.strip()


# Full integration test with sample prompts
@pytest.mark.parametrize("prompt_data", [
    # Prompt 1 - Cyberpunk old craftsman
    {
        'subject': '老工匠',
        'age': 70,
        'appearance': {
            'hair': ['银白色，凌乱，胡须', '护目镜', '发夹'],
            'eyes': ['发光青色瞳孔', '机械义眼', '深邃', '专注'],
            'clothing': ['赛博朋克工装夹克', '霓虹灯条装饰', '多层战术背心', '全息投影手套'],
            'skin_tone': ['古铜色', '机械臂植入', '纹身']
        },
        'setting': {
            'environment': {'type': '赛博朋克都市', 'time_of_day': '夜晚', 'weather': '酸雨'},
            'location': {
                'landmark': '霓虹灯广告牌林立的后巷',
                'urban_or_rural': '高度城市化',
                'specific_details': '全息广告、蒸汽管道'
            }
        },
        'mood': {
            'atmosphere': ['冷色调', '蓝紫色调', '霓虹光影'],
            'emotion': ['机械义肢轻敲工作台', '专注的神情', '手持全息图纸']
        },
        'techniques': ['masterpiece', 'best quality', 'highly detailed', 'intricate details', 'cyberpunk style']
    },
    # Prompt 2 - Steampunk girl
    {
        'subject': '少女',
        'age': 18,
        'appearance': {
            'hair': ['金色卷发', '复古盘发', '头纱', '装饰发带'],
            'eyes': ['深褐色', '明亮', '好奇', '睫毛膏'],
            'clothing': ['维多利亚风格束腰', '齿轮装饰领结', '蕾丝长裙', '皮革腰带'],
            'skin_tone': ['白皙', '玫瑰色腮红', '珍珠项链']
        },
        'setting': {
            'environment': {'type': '蒸汽朋克工坊', 'time_of_day': '黄昏', 'weather': '薄雾'},
            'location': {
                'landmark': '齿轮与黄铜装饰的阁楼工作室',
                'urban_or_rural': '历史城区',
                'specific_details': '机械装置、蒸汽管道'
            }
        },
        'mood': {
            'atmosphere': ['暖色调', '琥珀色', '烛光氛围'],
            'emotion': ['摆弄齿轮装置', '微笑', '手持怀表']
        },
        'techniques': ['masterpiece', 'best quality', 'highly detailed', 'intricate details', 'steampunk style']
    },
])
def test_full_prompt_analysis(prompt_data):
    """Full integration test for prompt analysis pipeline."""
    # Validate schema
    is_valid, _ = validate_prompt(prompt_data)
    assert is_valid, f"Schema validation failed: {prompt_data.get('subject')}"

    # Analyze impact
    impact = analyze_impact(prompt_data)
    assert 'estimated_quality_tier' in impact

    # Check confidence threshold
    appearance_score = _calculate_appearance_score(prompt_data)
    techniques_score = _calculate_techniques_score(prompt_data)
    setting_score = _calculate_setting_score(prompt_data)
    raw_confidence = (appearance_score * 0.35 + techniques_score * 0.40 + setting_score * 0.25)
    assert raw_confidence >= EXPECTED_MIN_CONFIDENCE, f"Confidence {raw_confidence:.4f} below threshold"
