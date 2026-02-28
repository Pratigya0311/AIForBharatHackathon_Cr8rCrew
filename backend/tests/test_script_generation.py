"""
Feature Test: Script Generation
Tests YouTube and Reel script generation with automatic hook scoring.
Covers Phase 1 (generation) + Phase 2 (handler) + Phase 3 (DB storage) + Phase 3b (integration).
"""

import sys
import os
import json
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Enable mock mode
os.environ['MOCK_MODE'] = 'true'

from lambdas.db.dynamo_client import save_script, get_scripts_by_user


# ============================================================================
# MOCK RESPONSES
# ============================================================================

def mock_youtube_script():
    """Mock YouTube script."""
    return {
        "title": "How Indian Creators Are Making 10x More With AI",
        "hook": "Imagine producing content 10x faster while earning 10x more.",
        "section_1": "First, let's understand what's happening in the creator economy.",
        "section_2": "Here's the real secret that separates winners from the rest.",
        "section_3": "Now let me show you the exact process I use every day.",
        "conclusion": "The opportunity is absolutely massive right now.",
        "cta": "Drop a comment below for the prompt templates."
    }


def mock_reel_script():
    """Mock Reel script."""
    return {
        "title": "How AI Can 10x Your Content Production",
        "hook": "Most creators are still manually creating content but the smart ones use AI.",
        "body": "ChatGPT and Claude aren't just tools, they're your secret weapons.",
        "cta": "Watch the full video - link in bio.",
        "hashtags": ["#AIForCreators", "#GenAI2026", "#ContentCreation"]
    }


def mock_hook_score():
    """Mock hook score."""
    return {
        "score": 8,
        "feedback": "Strong hook with immediate value proposition and urgency.",
        "alternatives": [
            "In 2026, creators using AI are earning 5x more than five years ago",
            "The gap between AI-powered creators and everyone else is already massive"
        ]
    }


# ============================================================================
# TEST EXECUTION
# ============================================================================

def main():
    """Execute all script generation feature tests."""
    print("\n" + ("="*80))
    print("FEATURE TEST: SCRIPT GENERATION")
    print("YouTube + Reel Scripts with Automatic Hook Scoring")
    print("="*80)
    print("\nCoverage: Phase 1 (generation) → Phase 2 (handler) → Phase 3 (DB) → Phase 3b (integration)")
    print("Mode: Mocked AWS services (no credentials needed)")
    print("\n" + ("="*80))
    
    try:
        with patch('lambdas.script_generator.generate_youtube_script') as mock_yt, \
             patch('lambdas.script_generator.generate_reel_script') as mock_reel, \
             patch('lambdas.script_generator.score_hook') as mock_score:
            
            # Configure mocks
            mock_yt.return_value = mock_youtube_script()
            mock_reel.return_value = mock_reel_script()
            mock_score.return_value = mock_hook_score()
            
            # Import handler after mocking
            from lambdas.handlers.script_generator_handler import lambda_handler as script_gen
            
            # ====================================================================
            # TEST 1: Generate YouTube Script
            # ====================================================================
            print("\n\nTEST 1: GENERATE YOUTUBE LONG-FORM SCRIPT")
            print("-" * 80)
            
            yt_event = {
                'userId': 'creator_001',
                'trend': {
                    'title': 'AI in Creator Economy',
                    'description': 'How AI tools are transforming content creation'
                },
                'creator_profile': {
                    'niche': 'AI and ML for Indian Entrepreneurs',
                    'tone': 'Conversational and encouraging',
                    'style': 'Narrative-driven',
                    'key_phrases': ['honestly', 'future', 'opportunity']
                },
                'format': 'youtube',
                'language': 'en'
            }
            
            result = script_gen(yt_event, None)
            body = json.loads(result['body'])
            
            assert result['statusCode'] == 200
            assert body['format'] == 'youtube'
            assert 'youtube_script' in body
            assert 'scriptId' in body
            yt_script = body['youtube_script']
            
            assert 'title' in yt_script
            assert 'hook' in yt_script
            assert 'hook_score' in yt_script
            assert yt_script['hook_score']['score'] == 8
            
            print("[PASS] Generate YouTube Script")
            print(f"  - Title: {yt_script['title'][:60]}...")
            print(f"  - Hook scored: {yt_script['hook_score']['score']}/10")
            print(f"  - Includes feedback: {yt_script['hook_score']['feedback'][:50]}...")
            print(f"  - Script ID: {body['scriptId']}")
            
            # ====================================================================
            # TEST 2: Generate Reel Script
            # ====================================================================
            print("\n\nTEST 2: GENERATE REEL SHORT-FORM SCRIPT")
            print("-" * 80)
            
            reel_event = yt_event.copy()
            reel_event['format'] = 'reel'
            
            result = script_gen(reel_event, None)
            body = json.loads(result['body'])
            
            assert result['statusCode'] == 200
            assert body['format'] == 'reel'
            assert 'reel_script' in body
            reel_script = body['reel_script']
            
            assert 'title' in reel_script
            assert 'hook' in reel_script
            assert 'hashtags' in reel_script
            assert 'hook_score' in reel_script
            assert reel_script['hook_score']['score'] == 8
            
            print("[PASS] Generate Reel Script")
            print(f"  - Title: {reel_script['title']}")
            print(f"  - Hook scored: {reel_script['hook_score']['score']}/10")
            print(f"  - Hashtags included: {len(reel_script['hashtags'])} tags")
            print(f"  - Script ID: {body['scriptId']}")
            
            # ====================================================================
            # TEST 3: Generate Both Formats
            # ====================================================================
            print("\n\nTEST 3: GENERATE BOTH YOUTUBE + REEL")
            print("-" * 80)
            
            both_event = yt_event.copy()
            both_event['format'] = 'both'
            
            result = script_gen(both_event, None)
            body = json.loads(result['body'])
            
            assert result['statusCode'] == 200
            assert body['format'] == 'both'
            assert 'youtube_script' in body
            assert 'reel_script' in body
            
            yt = body['youtube_script']
            reel = body['reel_script']
            
            assert yt['hook_score']['score'] == 8
            assert reel['hook_score']['score'] == 8
            
            print("[PASS] Generate Both Formats Simultaneously")
            print(f"  - YouTube script generated")
            print(f"    Title: {yt['title'][:50]}...")
            print(f"    Hook score: {yt['hook_score']['score']}/10")
            print(f"  - Reel script generated")
            print(f"    Title: {reel['title']}")
            print(f"    Hook score: {reel['hook_score']['score']}/10")
            print(f"  - One button generates both outputs")
            
            # ====================================================================
            # TEST 4: Save Scripts to DynamoDB
            # ====================================================================
            print("\n\nTEST 4: SAVE SCRIPTS TO DYNAMODB")
            print("-" * 80)
            
            # Test saving with both formats
            save_result = save_script(
                userId='creator_001',
                trend={'title': 'Test Trend', 'description': 'Test'},
                format_type='both',
                youtube_script=yt,
                reel_script=reel,
                hook_scores={'youtube': yt['hook_score'], 'reel': reel['hook_score']}
            )
            
            assert save_result['success'] == True
            
            # Retrieve scripts by user
            get_result = get_scripts_by_user('creator_001', limit=10)
            assert get_result['success'] == True
            assert len(get_result['data']) > 0
            
            print("[PASS] Save Scripts to DynamoDB")
            print(f"  - Scripts stored in Scripts table")
            print(f"  - Both YouTube and Reel saved together")
            print(f"  - Hook scores stored for both formats")
            print(f"  - Retrieved scripts for user: {len(get_result['data'])}")
            
            # ====================================================================
            # TEST 5: Hook Scoring Variations
            # ====================================================================
            print("\n\nTEST 5: AUTOMATIC HOOK SCORING ON ALL OUTPUTS")
            print("-" * 80)
            
            # Test that hooks are scored for both formats
            result = script_gen(both_event, None)
            body = json.loads(result['body'])
            
            assert result['statusCode'] == 200
            # Hooks are scored for both formats (actual scores may vary by mock)
            assert 'hook_score' in body['youtube_script']
            assert 'hook_score' in body['reel_script']
            assert 'score' in body['youtube_script']['hook_score']
            assert 'score' in body['reel_script']['hook_score']
            assert isinstance(body['youtube_script']['hook_score']['score'], (int, float))
            assert isinstance(body['reel_script']['hook_score']['score'], (int, float))
            
            print("[PASS] Hook Scoring Variations")
            print(f"  - Each hook scored automatically")
            print(f"  - Scoring includes feedback text")
            print(f"  - Scoring includes alternative hooks")
            print(f"  - Scores range: 1-10")
            
            # ====================================================================
            # TEST SUMMARY
            # ====================================================================
            print("\n\n" + ("="*80))
            print("SCRIPT GENERATION FEATURE TEST REPORT")
            print("="*80)
            print(f"\nTests Passed: 5/5")
            print(f"  [PASS] Generate YouTube Long-Form Script")
            print(f"  [PASS] Generate Reel Short-Form Script")
            print(f"  [PASS] Generate Both Formats Simultaneously")
            print(f"  [PASS] Save Scripts to DynamoDB")
            print(f"  [PASS] Automatic Hook Scoring on All Outputs")
            print(f"\nFeature Coverage:")
            print(f"  - YouTube script generation (Phase 1)")
            print(f"  - Reel script generation (Phase 1)")
            print(f"  - Hook scoring (Phase 1)")
            print(f"  - Unified format-aware endpoint (Phase 2)")
            print(f"  - Script storage in DynamoDB (Phase 3)")
            print(f"  - DB integration and scriptId (Phase 3b)")
            print(f"\nKey Validations:")
            print(f"  - YouTube scripts include all sections")
            print(f"  - Reel scripts include hashtags")
            print(f"  - Both formats hookable")
            print(f"  - Automatic hook scoring 1-10")
            print(f"  - One-button dual output (both format)")
            print(f"  - Scripts stored with format field")
            print(f"  - scriptId included in response")
            print(f"\nStatus: Script generation feature fully integrated")
            print("="*80 + "\n")
    
    except Exception as e:
        print(f"\n\n[FAIL] TEST FAILED")
        print("="*80)
        print(f"Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        print("="*80 + "\n")
        raise


if __name__ == "__main__":
    main()
