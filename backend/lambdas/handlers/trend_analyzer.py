"""
Lambda Handler: Trend Analyzer
Ranks trending topics for a creator based on semantic relevance.
"""

import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lambdas.embeddings import match_trend_to_creator, generate_embedding


def lambda_handler(event, context):
    """
    Lambda handler for trend analysis.
    
    Input event:
    {
        "userId": "string",
        "creator_embedding": [...],
        "trends_list": [
            {
                "trendId": "string",
                "title": "string",
                "description": "string"
            },
            ...
        ]
    }
    
    Returns:
    {
        "statusCode": 200,
        "body": {
            "userId": "string",
            "ranked_trends": [
                {
                    "trendId": "string",
                    "title": "string",
                    "description": "string",
                    "relevance_score": float,
                    "novelty_score": float
                },
                ...
            ]
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
        creator_embedding = body.get('creator_embedding')
        trends_list = body.get('trends_list', [])
        
        # Validate inputs
        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'userId is required'})
            }
        
        if not creator_embedding or len(creator_embedding) != 1536:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'creator_embedding must be a 1536-dimensional vector'})
            }
        
        if not trends_list or not isinstance(trends_list, list):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'trends_list is required and must be an array'})
            }
        
        # Rank trends by relevance
        ranked_trends = []
        
        for trend in trends_list:
            trend_id = trend.get('trendId')
            title = trend.get('title')
            description = trend.get('description')
            
            if not trend_id or not title or not description:
                continue
            
            # Match trend to creator
            match_result = match_trend_to_creator(
                " ".join([title, description]),  # Combine title and description
                description
            )
            
            relevance_score = match_result.get('relevance_score', 0)
            
            # Placeholder novelty score (to be calculated from trend data in Phase 3)
            novelty_score = 0.5
            
            ranked_trends.append({
                'trendId': trend_id,
                'title': title,
                'description': description,
                'relevance_score': relevance_score,
                'novelty_score': novelty_score
            })
        
        # Sort by relevance score (descending)
        ranked_trends.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Take top 5
        top_trends = ranked_trends[:5]
        
        # Return success
        return {
            'statusCode': 200,
            'body': json.dumps({
                'userId': user_id,
                'ranked_trends': top_trends
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
            'body': json.dumps({'error': f'Trend analysis failed: {str(e)}'})
        }


if __name__ == "__main__":
    # Local test
    import random
    
    test_embedding = [random.uniform(0, 1) for _ in range(1536)]
    
    test_event = {
        'userId': 'creator_001',
        'creator_embedding': test_embedding,
        'trends_list': [
            {
                'trendId': 'trend_001',
                'title': 'AI and Machine Learning',
                'description': 'The rise of generative AI tools and their impact on productivity'
            },
            {
                'trendId': 'trend_002',
                'title': 'Cooking at Home',
                'description': 'New recipes and cooking techniques for home chefs'
            },
            {
                'trendId': 'trend_003',
                'title': 'Python Programming',
                'description': 'Learning Python for AI and automation'
            }
        ]
    }
    
    result = lambda_handler(test_event, None)
    print("[TEST] Trend Analyzer Handler")
    print(f"Status: {result['statusCode']}")
    body = json.loads(result['body'])
    print(f"User ID: {body.get('userId')}")
    print(f"Top Trends Found: {len(body.get('ranked_trends', []))}")
    for trend in body.get('ranked_trends', [])[:3]:
        print(f"  - {trend['title']}: {trend['relevance_score']:.3f} relevance")
