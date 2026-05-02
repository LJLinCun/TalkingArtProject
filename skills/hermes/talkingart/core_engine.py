#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TalkingArtProject → Hermes Integration Core Engine

This module provides the core engine for integrating TalkingArtProject's prompt engineering framework
with Hermes Agent's skill system. It implements the 5-module workflow:
1. Keyword Expansion & Extraction
2. Intent Classification & Routing  
3. Archetype Matching
4. Style Parameter Mapping
5. Full Pipeline Execution (Orchestrator)

Usage:
    python talkingart_engine.py --mode <keyword_expander|intent_classifier|archetype_matcher|style_mapper|full_pipeline>
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Constants
TEST_DIR = r"D:/TalkingArtProject"
if not os.path.exists(TEST_DIR):
    TEST_DIR = "/mnt/d/TalkingArtProject"

class KeywordExpander:
    """Module 1: Extract and expand keywords from user input with confidence scoring."""
    
    def __init__(self, archetype_library_path: str = None):
        self.archetype_library_path = archetype_library_path or f"{TEST_DIR}/prompts/character/archetypes"
        # Preload archetype traits vocabulary
        self._traits_vocabulary = self._build_traits_vocabulary()
        
    def _build_traits_vocabulary(self) -> Dict[str, List[str]]:
        """Build vocabulary of trait keywords from all archetypes."""
        vocabulary = {}
        for archetype_file in Path(self.archetype_library_path).glob("*.yaml"):
            try:
                with open(archetype_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract personality_traits
                    if '"personality_traits"' in content or "'personality_traits'" in content:
                        # Simple extraction - in production use yaml parser
                        for trait in ["engineer", "craftsman", "scifi", "cyberpunk", 
                                     "steampunk", "victorian", "precision", "machines",
                                     "clockwork", "automaton", "industrial"]:
                            vocabulary[trait.lower()] = content
            except Exception as e:
                pass  # Graceful degradation
        return vocabulary
    
    def extract_and_expand(self, user_input: str) -> Dict:
        """
        Extract explicit entities and infer implicit attributes from user input.
        
        Args:
            user_input: Natural language text from user
            
        Returns:
            Dictionary with extracted_entities, expanded_options, recommended_expansion
        """
        # Step 1: Parse input for explicit keywords
        extracted = {
            "subject": [],
            "action": None,
            "style_terms": []
        }
        
        # Detect action verbs
        action_verbs = ["画", "设计", "生成", "创建", "制作", "描绘"]
        for verb in action_verbs:
            if verb in user_input:
                extracted["action"] = verb
                break
        
        # Extract style terms (simplified - in production use NLP)
        style_terms = ["赛博朋克", "蒸汽朋克", "科幻", "奇幻", "维多利亚", "哥特式"]
        for term in style_terms:
            if term in user_input:
                extracted["style_terms"].append(term)
        
        # Step 2: Infer implicit attributes
        inferred = {
            "age_range": None,
            "setting_type": None,
            "mood_keywords": []
        }
        
        # Simple inference rules based on style terms
        if "赛博朋克" in user_input:
            inferred["mood_keywords"] = ["霓虹灯", "未来感", "高科技"]
            extracted["subject"].append("future character")
        elif "蒸汽朋克" in user_input:
            inferred["mood_keywords"] = ["复古科技", "机械美学", "维多利亚风格"]
            extracted["subject"].append("industrial craftsman")
        
        # Step 3: Build expansion options
        expanded_options = {
            "age_range": ["25-40 岁", "45-60 岁"],
            "setting_type": ["室内工作室", "未来都市街道"]
        }
        
        # Step 4: Build recommendation
        if len(extracted["style_terms"]) == 0:
            recommended = f"建议补充风格描述，如：{', '.join(style_terms[:3])}"
        else:
            recommended = "已识别风格特征，可根据需要进一步细化设定"
        
        return {
            "extracted_entities": extracted,
            "inferred_attributes": inferred,
            "expanded_options": expanded_options,
            "recommended_expansion": recommended
        }


class IntentClassifier:
    """Module 2: Classify user intent into CHARACTER/TASK/STYLE/COMPOUND categories."""
    
    def __init__(self):
        self.intent_categories = [
            "CHARACTER",  # Designing/illustrating character/archetype
            "TASK",       # Executing computational/logic operations
            "STYLE",      # Applying visual style parameters to generation
            "COMPOUND"    # Multiple overlapping intents
        ]
        
    def classify_intent(self, user_input: str) -> Dict:
        """
        Classify intent categories and determine execution priority.
        
        Args:
            user_input: Natural language text from user
            
        Returns:
            Dictionary with detected_intents, dominant_intent, is_compound, recommended_action
        """
        # Step 1: Score each intent category (simplified - production uses ML model)
        scores = {}
        for category in self.intent_categories:
            if category == "CHARACTER":
                # Character-related keywords
                character_keywords = ["画", "设计", "角色", "人物", "形象"]
                score = sum(1 for kw in character_keywords if kw in user_input) / len(character_keywords)
            elif category == "TASK":
                # Task-related keywords  
                task_keywords = ["生成文档", "写代码", "分析数据", "执行任务", "处理"]
                score = sum(1 for kw in task_keywords if kw in user_input) / len(task_keywords)
            elif category == "STYLE":
                # Style-related keywords
                style_keywords = ["风格", "光影", "构图", "视觉效果"]
                score = sum(1 for kw in style_keywords if kw in user_input) / len(style_keywords)
            else:
                score = 0.5  # Default for COMPOUND
            
            scores[category] = round(min(score, 1.0), 2)  # Cap at 1.0 and round to 2 decimals
        
        # Step 2: Identify dominant intent
        max_score = max(scores.values())
        dominant_intent = None
        for category, score in scores.items():
            if abs(score - max_score) < 0.05:  # Within tolerance
                dominant_intent = category
                break
        
        # Step 3: Check for compound intent
        is_compound = sum(1 for s in scores.values() if s >= 0.6) >= 2
        
        # Step 4: Determine recommended action
        all_confidence_low = max(scores.values()) < 0.5
        if dominant_intent and not is_compound:
            recommended_action = f"execute_{dominant_intent.lower()}_module"
        elif is_compound:
            recommended_action = "spawn_parallel_subagents"
        else:
            recommended_action = "request_clarification"
        
        return {
            "detected_intents": scores,
            "dominant_intent": dominant_intent,
            "is_compound": is_compound,
            "all_confidence_low": all_confidence_low,
            "recommended_action": recommended_action
        }


class ArchetypeMatcher:
    """Module 3: Match user input to archetype library with similarity scoring."""
    
    def __init__(self, archetype_library_path: str = None):
        self.archetype_library_path = archetype_library_path or f"{TEST_DIR}/prompts/character/archetypes"
        # Preload archetype data
        self._archetypes_data = {}
        for archetype_file in Path(self.archetype_library_path).glob("*.yaml"):
            self._load_archetype(archetype_file)
    
    def _load_archetype(self, file_path: Path):
        """Load archetype data from YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                name = None
                for line in content.split('\n')[:10]:
                    if '"name":' in line or "'name':" in line:
                        # Extract name (simplified extraction)
                        parts = line.replace('{', '').replace('}', '').strip().split(',')
                        for part in parts:
                            if 'name:' in part.lower():
                                name = part.split(':')[1].strip().strip('"').strip("'")
                                break
                
            # Simple keyword extraction for matching
            keywords = []
            for trait in ["engineer", "craftsman", "clockwork", "cyberpunk", 
                         "steampunk", "scifi", "victorian", "precision"]:
                if trait.lower() in content.lower():
                    keywords.append(trait)
            
            self._archetypes_data[name or f"{file_path.stem}"] = {
                "keywords": keywords,
                "traits": keywords  # Simplified - production uses full trait vocabulary
            }
        except Exception as e:
            pass
    
    def match_archetype(self, user_input: str) -> Dict:
        """
        Match input to archetype library with similarity scoring.
        
        Args:
            user_input: Natural language text from user
            
        Returns:
            Dictionary with matched_archetypes[], recommendation
        """
        # Step 1: Extract keywords from user input (simplified)
        input_keywords = []
        for kw in ["engineer", "craftsman", "clockwork", "cyberpunk", 
                  "steampunk", "scifi", "victorian", "precision"]:
            if kw.lower() in user_input.lower():
                input_keywords.append(kw)
        
        # Step 2: Compute similarity scores
        matches = []
        for archetype_name, archetype_data in self._archetypes_data.items():
            keyword_overlap = len(set(input_keywords) & set(archetype_data["keywords"]))
            domain_relevance = len(set(input_keywords)) / max(len(input_keywords), 1)
            
            # similarity = (keyword_overlap * 0.6) + (domain_relevance * 0.4)
            similarity = keyword_overlap * 0.6 + domain_relevance * 0.4
            
            if similarity >= 0.4:  # Minimum threshold for matching
                matches.append({
                    "name": archetype_name,
                    "similarity_score": round(similarity, 3),
                    "keyword_overlap": keyword_overlap,
                    "domain_relevance": round(domain_relevance, 2)
                })
        
        # Step 3: Sort by similarity and select top matches
        matches.sort(key=lambda x: -x["similarity_score"])
        selected_matches = matches[:3]  # Maximum 3 recommendations
        
        # Step 4: Build recommendation
        if not selected_matches:
            recommendation = "未找到匹配的 Archetype，建议补充更明确的风格描述"
        else:
            best_match = selected_matches[0]
            gap_fillings = []
            for match in selected_matches:
                archetype_name = match["name"]
                if archetype_name in self._archetypes_data:
                    keywords_set = set(self._archetypes_data[archetype_name].get("keywords", []))
                    missing_keywords = set(input_keywords) - keywords_set
                    if missing_keywords:
                        gap_fillings.append(f"{match['name']}: 补充 {', '.join(list(missing_keywords)[:2])} 特征")
            
            recommendation = f"最佳匹配：{best_match['name']} (相似度：{best_match['similarity_score']:.3f})\n建议："
            if gap_fillings:
                recommendation += "\n- " + "\n- ".join(gap_fillings)
        
        return {
            "matched_archetypes": selected_matches,
            "recommendation": recommendation
        }


class StyleMapper:
    """Module 4: Map era/lighting/composition keywords to generation parameters."""
    
    def __init__(self):
        # Preload era mappings (simplified - production uses full database)
        self.era_mappings = {
            "赛博朋克": {"name": "Cyberpunk Era", "year_range": "2077+ AD",
                        "lighting_mood": "cinematic", "color_palette": ["#FF0040", "#00FFFF", "#1A1A2E"]},
            "蒸汽朋克": {"name": "Steampunk Era", "year_range": "1837-1901 AD",
                        "lighting_mood": "dramatic", "color_palette": ["#C4A56E", "#2D3E4B", "#8B0000"]},
            "维多利亚": {"name": "Victorian Era", "year_range": "1837-1901 AD",
                        "lighting_mood": "natural", "color_palette": ["#D4C5B0", "#2F4F4F", "#CD853F"]}
        }
    
    def map_style(self, user_input: str) -> Dict:
        """
        Map era/lighting/composition keywords to generation parameters.
        
        Args:
            user_input: Natural language text from user
            
        Returns:
            Dictionary with style_parameters{}, parameter_expansion[]
        """
        # Step 1: Detect era keywords in input
        detected_era = None
        for era_keyword in self.era_mappings.keys():
            if era_keyword in user_input:
                detected_era = era_keyword
                break
        
        # Step 2: Map to generation parameters
        style_params = {
            "era": {"name": "Unknown Era", "year_range": "N/A AD",
                   "lighting_mood": "natural", "color_palette": []},
            "parameter_expansion": []
        }
        
        if detected_era:
            era_data = self.era_mappings[detected_era]
            style_params["era"] = {
                "name": era_data["name"],
                "year_range": era_data["year_range"],
                "lighting_mood": era_data["lighting_mood"],
                "color_palette": era_data["color_palette"]
            }
        else:
            # Default parameters
            style_params["era"]["name"] = "Generic Setting"
            style_params["era"]["year_range"] = "Contemporary Era"
        
        # Step 3: Build parameter expansion explanations
        for era_keyword in self.era_mappings.keys():
            if era_keyword in user_input:
                era_data = self.era_mappings[era_keyword]
                style_params["parameter_expansion"].append({
                    "input_term": era_keyword,
                    "mapped_value": f"{era_data['name']} ({era_data['year_range']})",
                    "confidence": 0.95
                })
        
        return style_params


class TalkingArtPipeline:
    """
    Module 5: Full Pipeline Orchestrator - Execute complete TalkingArtProject workflow.
    
    Coordinates all 4 modules and implements the end-to-end execution flow:
    User Input → Keyword Expansion → Intent Classification → Archetype Matching
                → Style Mapping → Synthesis & Validation → Final Output
    """
    
    def __init__(self, archetype_library_path: str = None):
        self.keyword_expander = KeywordExpander(archetype_library_path)
        self.intent_classifier = IntentClassifier()
        self.archetype_matcher = ArchetypeMatcher(archetype_library_path)
        self.style_mapper = StyleMapper()
    
    def execute_pipeline(self, user_input: str) -> Dict:
        """
        Execute the complete TalkingArtProject workflow from user input to final output.
        
        Args:
            user_input: Natural language text from user
            
        Returns:
            Dictionary with generation_result, metadata (archetype_used, style_era, confidence)
        """
        # Step 1: Keyword Expansion & Extraction
        keyword_results = self.keyword_expander.extract_and_expand(user_input)
        
        # Step 2: Intent Classification & Routing
        intent_results = self.intent_classifier.classify_intent(user_input)
        
        if intent_results["all_confidence_low"]:
            return {
                "status": "CLARIFICATION_NEEDED",
                "message": f"置信度较低，建议补充信息：{keyword_results['recommended_expansion']}"
            }
        
        # Step 3: Archetype Matching
        archetype_results = self.archetype_matcher.match_archetype(user_input)
        best_archetype = None
        if archetype_results["matched_archetypes"]:
            best_archetype = archetype_results["matched_archetypes"][0]["name"]
        
        # Step 4: Style Parameter Mapping
        style_results = self.style_mapper.map_style(user_input)
        best_era = None
        if style_results["parameter_expansion"]:
            best_era = style_results["parameter_expansion"][0]["mapped_value"]
        
        # Step 5: Synthesis (simplified - production combines all results into final prompt)
        synthesis_result = {
            "status": "SUCCESS",
            "extracted_info": keyword_results,
            "intent_classification": intent_results,
            "archetype_match": archetype_results,
            "style_mapping": style_results
        }
        
        # Build metadata
        confidence_score = self._calculate_overall_confidence(keyword_results, intent_results)
        synthesis_result["metadata"] = {
            "best_archetype": best_archetype or "Unknown",
            "best_style_era": best_era or "Generic Setting",
            "confidence_score": round(confidence_score, 3),
            "is_compound_intent": intent_results["is_compound"],
            "recommended_action": intent_results["recommended_action"]
        }
        
        return synthesis_result
    
    def _calculate_overall_confidence(self, keyword_results: Dict, intent_results: Dict) -> float:
        """Calculate overall confidence score from intermediate results."""
        # Simplified calculation - production uses weighted combination of all scores
        max_intent_score = max(intent_results["detected_intents"].values())
        
        if len(keyword_results.get("extracted_entities", {}).get("style_terms", [])) >= 2:
            confidence = (max_intent_score * 0.6) + 0.4
        else:
            confidence = max_intent_score * 0.5
        
        return min(confidence, 1.0)


def main():
    """Command-line interface for testing TalkingArtProject → Hermes integration."""
    import argparse
    
    parser = argparse.ArgumentParser(description="TalkingArtProject → Hermes Integration Engine")
    parser.add_argument(
        "--mode", type=str, choices=["keyword_expander", "intent_classifier", 
                                      "archetype_matcher", "style_mapper", "full_pipeline"],
        default="full_pipeline",
        help="Execution mode (default: full_pipeline)"
    )
    parser.add_argument(
        "--input", type=str,
        required=True, 
        help="User input text to process"
    )
    
    args = parser.parse_args()
    
    # Select appropriate engine based on mode
    if args.mode == "full_pipeline":
        pipeline = TalkingArtPipeline()
        result = pipeline.execute_pipeline(args.input)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.mode == "keyword_expander":
        expander = KeywordExpander()
        result = expander.extract_and_expand(args.input)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.mode == "intent_classifier":
        classifier = IntentClassifier()
        result = classifier.classify_intent(args.input)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.mode == "archetype_matcher":
        matcher = ArchetypeMatcher()
        result = matcher.match_archetype(args.input)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.mode == "style_mapper":
        mapper = StyleMapper()
        result = mapper.map_style(args.input)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()