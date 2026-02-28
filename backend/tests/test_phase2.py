"""
Phase 2 Integration Test Suite
Tests all 3 Lambda handlers with mocked Phase 1 functions.
"""

import sys
import os
import json
import random
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# Mock all Phase 1 functions before importing handlers
import lambdas.embeddings
import lambdas.script_generator


# ============================================================================
# MOCK RESPONSES FOR PHASE 1 FUNCTIONS
# ============================================================================

def mock_embedding():
    """Generate a fake 1536-dimensional embedding vector."""
    return [random.uniform(0, 1) for _ in range(1536)]


def mock_style_dna_response():
    """Mock Style DNA extraction."""
    return {
        "niche": "AI and Machine Learning for Indian Entrepreneurs",
        "tone": "Conversational, encouraging, tech-forward",
        "style": "Narrative-driven with real examples",
        "key_phrases": ["honestly", "build from there", "future is AI-powered", "anyone can learn"],
        "target_audience": "Indian creators and small business owners aged 18-35"
    }


def mock_youtube_script_response():
    """Mock YouTube script."""
    return {
        "title": "How Indian Creators Are Making 10x More Money Using AI in 2026",
        "hook": "Imagine you could produce content 10x faster and earn 10x more money while doing it. That's exactly what's happening to Indian creators right now.",
        "section_1": "First, let's talk about what's actually happening in the creator economy right now.",
        "section_2": "So here's the real secret - it's not about being a technical genius.",
        "section_3": "Now let me walk you through the actual process I use every single day.",
        "conclusion": "The opportunity right now is absolutely massive.",
        "cta": "If you want the exact prompt templates I use, drop a comment below."
    }


def mock_reel_script_response():
    """Mock Reel script."""
    return {
        "title": "Indian Creators Making 10x More With AI",
        "hook": "Most creators in 2026 are still manually making content... but the smart ones are using AI.",
        "body": "ChatGPT and Claude aren't just tools, they're your secret weapons.",
        "cta": "Watch the full video on my channel - link in bio.",
        "hashtags": ["#AIForCreators", "#GenAI2026", "#CreatorEconomy", "#BharatAI", "#ContentCreation"]
    }


def mock_hook_score_response():
    """Mock hook scoring."""
    return {
        "score": 8,
        "feedback": "Strong hook that promises a specific benefit and creates urgency.",
        "alternatives": [
            "In 2026, the gap between AI-powered creators and everyone else is already insane",
            "Every creator who mastered AI in 2025 is now making 10x more in 2026",
            "The creators earning 10x more in 2026 all know one thing others don't"
        ]
    }


# ============================================================================
# TEST SETUP AND EXECUTION
# ============================================================================

def main():
    """Execute all Phase 2 integration tests."""
    print("\n" + ("="*80))
    print("TRENDSCRIBE PHASE 2 - INTEGRATION TEST SUITE")
    print("Lambda Handlers & API Logic")
    print("="*80)
    print("\nTest Mode: Mocked Phase 1 functions (no AWS needed)")
    print("\n" + ("="*80))
    
    try:
        with patch('lambdas.embeddings.extract_style_dna') as mock_extract_dna, \
             patch('lambdas.embeddings.generate_embedding') as mock_embedding_func, \
             patch('lambdas.embeddings.match_trend_to_creator') as mock_match_trend, \
             patch('lambdas.script_generator.generate_youtube_script') as mock_yt_script, \
             patch('lambdas.script_generator.generate_reel_script') as mock_reel_script, \
             patch('lambdas.script_generator.score_hook') as mock_score:
            
            # Configure mock responses
            mock_extract_dna.return_value = mock_style_dna_response()
            mock_embedding_func.return_value = mock_embedding()
            mock_match_trend.return_value = {'relevance_score': 0.75, 'is_relevant': True}
            mock_yt_script.return_value = mock_youtube_script_response()
            mock_reel_script.return_value = mock_reel_script_response()
            mock_score.return_value = mock_hook_score_response()
            
            # Import handlers after mocking Phase 1
            from lambdas.handlers.content_processor import lambda_handler as content_processor_handler
            from lambdas.handlers.trend_analyzer import lambda_handler as trend_analyzer_handler
            from lambdas.handlers.script_generator_handler import lambda_handler as script_gen_handler
            
            # ====================================================================
            # TEST 1: Content Processor Handler
            # ====================================================================
            print("\n\nTEST 1: CONTENT PROCESSOR HANDLER")
            print("-" * 80)
            print("Extracting Style DNA from creator content...")
            
            test_event_1 = {
                'userId': 'creator_001',
                'content_text': 'I make content about AI and machine learning for Indian entrepreneurs.'
            }
            
            result_1 = content_processor_handler(test_event_1, None)
            body_1 = json.loads(result_1['body'])
            
            assert result_1['statusCode'] == 200, f"Expected 200, got {result_1['statusCode']}"
            assert body_1['userId'] == 'creator_001', "User ID mismatch"
            assert 'style_dna' in body_1, "Style DNA missing"
            assert 'embedding' in body_1, "Embedding missing"
            assert len(body_1['embedding']) == 1536, "Embedding size incorrect"
            
            print("[PASS] Content Processor Handler")
            print(f"  - User ID: {body_1['userId']}")
            print(f"  - Style DNA Niche: {body_1['style_dna']['niche']}")
            print(f"  - Embedding Size: {len(body_1['embedding'])} dimensions")
            
            # ====================================================================
            # TEST 2: Trend Analyzer Handler
            # ====================================================================
            print("\n\nTEST 2: TREND ANALYZER HANDLER")
            print("-" * 80)
            print("Ranking trends for creator...")
            
            test_embedding = mock_embedding()
            test_event_2 = {
                'userId': 'creator_001',
                'creator_embedding': test_embedding,
                'trends_list': [
                    {
                        'trendId': 'trend_001',
                        'title': 'AI and Automation',
                        'description': 'How AI is automating content creation'
                    },
                    {
                        'trendId': 'trend_002',
                        'title': 'Cooking Tips',
                        'description': 'New cooking recipes and techniques'
                    },
                    {
                        'trendId': 'trend_003',
                        'title': 'Python Programming',
                        'description': 'Learning Python for automation'
                    }
                ]
            }
            
            result_2 = trend_analyzer_handler(test_event_2, None)
            body_2 = json.loads(result_2['body'])
            
            assert result_2['statusCode'] == 200, f"Expected 200, got {result_2['statusCode']}"
            assert body_2['userId'] == 'creator_001', "User ID mismatch"
            assert 'ranked_trends' in body_2, "Ranked trends missing"
            assert len(body_2['ranked_trends']) <= 5, "Should return max 5 trends"
            assert all('relevance_score' in t for t in body_2['ranked_trends']), "Missing relevance scores"
            assert all('novelty_score' in t for t in body_2['ranked_trends']), "Missing novelty scores"
            
            print("[PASS] Trend Analyzer Handler")
            print(f"  - User ID: {body_2['userId']}")
            print(f"  - Trends Ranked: {len(body_2['ranked_trends'])}")
            for i, trend in enumerate(body_2['ranked_trends'][:3], 1):
                print(f"    {i}. {trend['title']}: {trend['relevance_score']:.3f} relevance")
            
            # ====================================================================
            # TEST 3: Script Generator - YouTube Only
            # ====================================================================
            print("\n\nTEST 3: SCRIPT GENERATOR - YOUTUBE FORMAT")
            print("-" * 80)
            print("Generating YouTube long-form script...")
            
            test_event_3 = {
                'userId': 'creator_001',
                'trend': {
                    'title': 'Bharat GenAI',
                    'description': 'AI revolution in creator economy',
                    'context': '2026 trends'
                },
                'creator_profile': {
                    'niche': 'AI & ML for Indian Entrepreneurs',
                    'tone': 'Conversational, encouraging',
                    'style': 'Story-driven',
                    'key_phrases': ['honestly', 'future'],
                    'target_audience': 'Indian creators'
                },
                'format': 'youtube',
                'language': 'en'
            }
            
            result_3 = script_gen_handler(test_event_3, None)
            body_3 = json.loads(result_3['body'])
            
            assert result_3['statusCode'] == 200, f"Expected 200, got {result_3['statusCode']}"
            assert body_3['format'] == 'youtube', "Format should be youtube"
            assert 'youtube_script' in body_3, "YouTube script missing"
            assert body_3['youtube_script']['hook_score']['score'] == 8, "Hook score incorrect"
            assert 'reel_script' not in body_3, "Reel script should not be present for youtube format"
            
            print("[PASS] Script Generator - YouTube Format")
            print(f"  - Format: {body_3['format']}")
            print(f"  - YouTube Title: {body_3['youtube_script']['title'][:60]}...")
            print(f"  - Hook Score: {body_3['youtube_script']['hook_score']['score']}/10")
            
            # ====================================================================
            # TEST 4: Script Generator - Reel Only
            # ====================================================================
            print("\n\nTEST 4: SCRIPT GENERATOR - REEL FORMAT")
            print("-" * 80)
            print("Generating Reel short-form script...")
            
            test_event_4 = test_event_3.copy()
            test_event_4['format'] = 'reel'
            
            result_4 = script_gen_handler(test_event_4, None)
            body_4 = json.loads(result_4['body'])
            
            assert result_4['statusCode'] == 200, f"Expected 200, got {result_4['statusCode']}"
            assert body_4['format'] == 'reel', "Format should be reel"
            assert 'reel_script' in body_4, "Reel script missing"
            assert body_4['reel_script']['hook_score']['score'] == 8, "Hook score incorrect"
            assert 'youtube_script' not in body_4, "YouTube script should not be present for reel format"
            assert 'hashtags' in body_4['reel_script'], "Hashtags missing from reel"
            
            print("[PASS] Script Generator - Reel Format")
            print(f"  - Format: {body_4['format']}")
            print(f"  - Reel Title: {body_4['reel_script']['title']}")
            print(f"  - Hook Score: {body_4['reel_script']['hook_score']['score']}/10")
            print(f"  - Hashtags: {len(body_4['reel_script']['hashtags'])} tags")
            
            # ====================================================================
            # TEST 5: Script Generator - Both Formats
            # ====================================================================
            print("\n\nTEST 5: SCRIPT GENERATOR - BOTH FORMATS")
            print("-" * 80)
            print("Generating both YouTube and Reel scripts...")
            
            test_event_5 = test_event_3.copy()
            test_event_5['format'] = 'both'
            
            result_5 = script_gen_handler(test_event_5, None)
            body_5 = json.loads(result_5['body'])
            
            assert result_5['statusCode'] == 200, f"Expected 200, got {result_5['statusCode']}"
            assert body_5['format'] == 'both', "Format should be both"
            assert 'youtube_script' in body_5, "YouTube script missing"
            assert 'reel_script' in body_5, "Reel script missing"
            assert body_5['youtube_script']['hook_score']['score'] == 8, "YouTube hook score incorrect"
            assert body_5['reel_script']['hook_score']['score'] == 8, "Reel hook score incorrect"
            
            print("[PASS] Script Generator - Both Formats")
            print(f"  - Format: {body_5['format']}")
            print(f"  - YouTube Script Title: {body_5['youtube_script']['title'][:50]}...")
            print(f"  - Reel Script Title: {body_5['reel_script']['title']}")
            print(f"  - YouTube Hook Score: {body_5['youtube_script']['hook_score']['score']}/10")
            print(f"  - Reel Hook Score: {body_5['reel_script']['hook_score']['score']}/10")
            
            # ====================================================================
            # TEST SUMMARY
            # ====================================================================
            print("\n\n" + ("="*80))
            print("PHASE 2 INTEGRATION TEST REPORT")
            print("="*80)
            print(f"\nTests Passed: 5/5")
            print(f"  [PASS] Content Processor Handler")
            print(f"  [PASS] Trend Analyzer Handler")
            print(f"  [PASS] Script Generator - YouTube Format")
            print(f"  [PASS] Script Generator - Reel Format")
            print(f"  [PASS] Script Generator - Both Formats")
            print(f"\nHandler Coverage:")
            print(f"  - content_processor.lambda_handler() - Operational")
            print(f"  - trend_analyzer.lambda_handler() - Operational")
            print(f"  - script_generator_handler.lambda_handler() - Operational")
            print(f"\nAPI Features:")
            print(f"  - Content processing with Style DNA extraction")
            print(f"  - Trend ranking with relevance scoring")
            print(f"  - Unified script generation endpoint")
            print(f"  - Format-aware response structure")
            print(f"  - Hook scoring on all script outputs")
            print(f"  - Proper error handling and validation")
            print(f"\nStatus: All Phase 2 handlers validated and ready for API Gateway integration")
            print("="*80 + "\n")
    
    except Exception as e:
        print(f"\n\n[FAIL] TEST SUITE FAILED")
        print("="*80)
        print(f"Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        print("="*80 + "\n")
        raise


if __name__ == "__main__":
    main()
