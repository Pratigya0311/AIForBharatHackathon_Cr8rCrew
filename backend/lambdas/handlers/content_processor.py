"""
Lambda Handler: Content Processor
Extracts creator's Style DNA and embeddings from sample content.
"""

import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lambdas.embeddings import extract_style_dna, generate_embedding


def lambda_handler(event, context):
    """
    Lambda handler for content processing.
    
    Input event:
    {
        "userId": "string",
        "content_text": "string"
    }
    
    Returns:
    {
        "statusCode": 200,
        "body": {
            "userId": "string",
            "style_dna": {...},
            "embedding": [...]
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
        content_text = body.get('content_text')
        
        # Validate inputs
        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'userId is required'})
            }
        
        if not content_text or not content_text.strip():
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'content_text is required and cannot be empty'})
            }
        
        # Extract Style DNA
        style_dna = extract_style_dna(content_text)
        
        # Generate embedding
        embedding = generate_embedding(content_text)
        
        # Return success
        return {
            'statusCode': 200,
            'body': json.dumps({
                'userId': user_id,
                'style_dna': style_dna,
                'embedding': embedding
            })
        }
    
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Invalid JSON: {str(e)}'})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Content processing failed: {str(e)}'})
        }


if __name__ == "__main__":
    # Local test
    test_event = {
        'userId': 'creator_001',
        'content_text': """
        Hey everyone! I've been diving deep into AI and machine learning lately.
        These tools can absolutely transform how Indian businesses grow.
        The future is AI-powered, and creators who understand this now will lead in 2026.
        """
    }
    
    result = lambda_handler(test_event, None)
    print("[TEST] Content Processor Handler")
    print(f"Status: {result['statusCode']}")
    body = json.loads(result['body'])
    print(f"User ID: {body.get('userId')}")
    print(f"Style DNA Keys: {list(body.get('style_dna', {}).keys())}")
    print(f"Embedding Size: {len(body.get('embedding', []))}")
