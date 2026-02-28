"""
Lambda Handler: Script Generator
Generates YouTube and/or Reel scripts based on format parameter.
Automatically scores hooks on all outputs.
"""

import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lambdas.script_generator import generate_youtube_script, generate_reel_script, score_hook


def lambda_handler(event, context):
    """
    Lambda handler for script generation.
    
    Input event:
    {
        "userId": "string",
        "trend": {
            "title": "string",
            "description": "string",
            "context": "string"
        },
        "creator_profile": {
            "niche": "string",
            "tone": "string",
            "style": "string",
            "key_phrases": ["string", ...],
            "target_audience": "string"
        },
        "format": "youtube" | "reel" | "both",
        "language": "en" | "hi" | "ta" | "te" | "kn" (optional, default: "en")
    }
    
    Returns:
    {
        "statusCode": 200,
        "body": {
            "userId": "string",
            "format": "youtube" | "reel" | "both",
            "youtube_script": {...} OR
            "reel_script": {...} OR
            "youtube_script": {...},
            "reel_script": {...}
        }
    }
    """
    try:
        # Parse request body
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        user_id = body.get('userId')
        trend = body.get('trend', {})
        creator_profile = body.get('creator_profile', {})
        format_type = body.get('format', 'youtube')
        language = body.get('language', 'en')
        
        # Validate inputs
        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'userId is required'})
            }
        
        if not trend or not trend.get('title') or not trend.get('description'):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'trend with title and description is required'})
            }
        
        if not creator_profile or not creator_profile.get('niche'):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'creator_profile with niche is required'})
            }
        
        if format_type not in ['youtube', 'reel', 'both']:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'format must be "youtube", "reel", or "both"'})
            }
        
        # Prepare response
        response_body = {
            'userId': user_id,
            'format': format_type,
            'language': language
        }
        
        # Generate YouTube script if requested
        if format_type in ['youtube', 'both']:
            youtube_script = generate_youtube_script(creator_profile, trend)
            
            # Score the hook
            hook_score = score_hook(youtube_script['hook'], creator_profile['niche'])
            youtube_script['hook_score'] = hook_score
            
            response_body['youtube_script'] = youtube_script
        
        # Generate Reel script if requested
        if format_type in ['reel', 'both']:
            reel_script = generate_reel_script(creator_profile, trend)
            
            # Score the hook
            hook_score = score_hook(reel_script['hook'], creator_profile['niche'])
            reel_script['hook_score'] = hook_score
            
            response_body['reel_script'] = reel_script
        
        # Return success
        return {
            'statusCode': 200,
            'body': json.dumps(response_body)
        }
    
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Invalid JSON: {str(e)}'})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Script generation failed: {str(e)}'})
        }


if __name__ == "__main__":
    # Local test
    test_event = {
        'userId': 'creator_001',
        'trend': {
            'title': 'Bharat GenAI - India\'s AI Revolution',
            'description': 'How Indian creators are using AI to scale content',
            'context': 'Generative AI adoption in creator economy 2026'
        },
        'creator_profile': {
            'niche': 'AI and Machine Learning for Indian Entrepreneurs',
            'tone': 'Conversational, encouraging, tech-forward',
            'style': 'Narrative-driven with real examples',
            'key_phrases': ['honestly', 'build', 'future', 'opportunity'],
            'target_audience': 'Indian small business owners and creators'
        },
        'format': 'both',
        'language': 'en'
    }
    
    result = lambda_handler(test_event, None)
    print("[TEST] Script Generator Handler")
    print(f"Status: {result['statusCode']}")
    body = json.loads(result['body'])
    print(f"User ID: {body.get('userId')}")
    print(f"Format: {body.get('format')}")
    
    if 'youtube_script' in body:
        yt = body['youtube_script']
        print(f"YouTube Script: {yt['title'][:50]}...")
        print(f"  Hook Score: {yt.get('hook_score', {}).get('score', 'N/A')}/10")
    
    if 'reel_script' in body:
        reel = body['reel_script']
        print(f"Reel Script: {reel['title']}")
        print(f"  Hook Score: {reel.get('hook_score', {}).get('score', 'N/A')}/10")
