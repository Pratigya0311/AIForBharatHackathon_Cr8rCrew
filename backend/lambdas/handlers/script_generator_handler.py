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
from lambdas.db.dynamo_client import save_script, get_creator_profile
from lambdas.db.s3_client import save_script as save_script_s3


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
        "language": "en" | "hi" | "ta" | "te" | "kn" (optional, default: "en"),
        "options": {
            "length": "string (e.g., '5-8 minutes')",
            "tone": "string (e.g., 'humorous', 'professional')",
            "structure": "string (e.g., 'tutorial', 'review')"
        }
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
        options = body.get('options', {})
        
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
        
        # Fetch creator profile from DynamoDB and merge (on best-effort basis)
        try:
            db_profile_result = get_creator_profile(user_id)
            if db_profile_result['success']:
                db_profile = db_profile_result['data']
                # Merge profiles: DB takes priority for style_dna and embedding
                if 'style_dna' in db_profile and db_profile['style_dna']:
                    import json as json_module
                    db_style_dna = json_module.loads(db_profile['style_dna']) if isinstance(db_profile['style_dna'], str) else db_profile['style_dna']
                    creator_profile['style_dna'] = db_style_dna
                if 'embedding' in db_profile and db_profile['embedding']:
                    creator_profile['embedding'] = db_profile['embedding']
                if 'niche' in db_profile:
                    creator_profile['niche'] = db_profile['niche']
                if 'tone' not in creator_profile and db_profile.get('tone'):
                    creator_profile['tone'] = db_profile['tone']
        except Exception:
            # DB fetch failed, use request profile only
            pass
        
        # Prepare response
        script_id = f"script_{user_id}_{int(__import__('time').time())}"
        response_body = {
            'userId': user_id,
            'format': format_type,
            'language': language,
            'scriptId': script_id
        }
        
        # Generate YouTube script if requested
        if format_type in ['youtube', 'both']:
            youtube_script = generate_youtube_script(creator_profile, trend, language, options)
            
            # Score the hook
            hook_score = score_hook(youtube_script['hook'], creator_profile['niche'])
            youtube_script['hook_score'] = hook_score
            
            response_body['youtube_script'] = youtube_script
        
        # Generate Reel script if requested
        if format_type in ['reel', 'both']:
            reel_script = generate_reel_script(creator_profile, trend, language, options)
            
            # Score the hook
            hook_score = score_hook(reel_script['hook'], creator_profile['niche'])
            reel_script['hook_score'] = hook_score
            
            response_body['reel_script'] = reel_script
        
        # Save scripts to DynamoDB and S3 (on best-effort basis)
        try:
            hook_scores = {}
            if 'youtube_script' in response_body:
                hook_scores['youtube'] = response_body['youtube_script'].get('hook_score')
            if 'reel_script' in response_body:
                hook_scores['reel'] = response_body['reel_script'].get('hook_score')
            
            # Save to DynamoDB
            db_result = save_script(
                userId=user_id,
                trend=trend,
                format_type=format_type,
                youtube_script=response_body.get('youtube_script'),
                reel_script=response_body.get('reel_script'),
                hook_scores=hook_scores,
                language=language
            )
            
            # Save full JSON backup to S3
            if db_result['success']:
                s3_result = save_script_s3(user_id, script_id, response_body)
        except Exception:
            # DB save failed, but return scripts anyway
            pass
        
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
        print(f"ERROR: {e}")
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
        'language': 'en',
        'options': {
            'length': 'short and punchy',
            'tone': 'highly enthusiastic',
            'structure': 'educational tutorial'
        }
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
