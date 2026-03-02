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
from lambdas.db.dynamo_client import get_all_trends
from lambdas.bedrock_client import call_claude


def predict_trend_trajectory(trend_title, trend_description, niche):
    """
    Use Claude to forecast if a trend is 'Rising', 'Peaking', or 'Falling' in a specific niche.
    Returns the trajectory and a novelty_score (1-100).
    """
    try:
        prompt = f"""You are an advanced AI Trend Forecaster for the '{niche}' creator economy. 

TREND: "{trend_title}"
CONTEXT: "{trend_description}"

TASK: Analyze this trend's current lifecycle stage and predict its trajectory.
1. Is this trend 'Rising' (early adoption, high novelty), 'Peaking' (mainstream, high competition), or 'Falling' (oversaturated, declining)?
2. Give it a novelty/freshness score from 1-100 (where 100 is completely untapped and fresh, 1 is overdone).

Respond ONLY with a JSON object in exactly this format:
{{
    "trajectory": "Rising",
    "novelty_score": 85,
    "forecast_reason": "Brief 1-sentence explanation of why it's at this stage."
}}"""
        
        response_text = call_claude(prompt, max_tokens=300)
        result = json.loads(response_text)
        return {
            'trajectory': result.get('trajectory', 'Rising'),
            'novelty_score': result.get('novelty_score', 50),
            'forecast_reason': result.get('forecast_reason', '')
        }
    except Exception as e:
        print(f"Trend prediction failed: {e}")
        return {'trajectory': 'Unknown', 'novelty_score': 50, 'forecast_reason': 'Could not forecast.'}


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
        
        # Fetch trends from DynamoDB (on best-effort basis)
        try:
            db_trends_result = get_all_trends(limit=50)
            if db_trends_result['success']:
                db_trends = db_trends_result['data']
                # Convert DB trend format to request format
                for db_trend in db_trends:
                    # Check if trend already in request list
                    trend_exists = any(t.get('trendId') == db_trend.get('trendId') for t in trends_list)
                    if not trend_exists:
                        trends_list.append({
                            'trendId': db_trend.get('trendId'),
                            'title': db_trend.get('title'),
                            'description': db_trend.get('description')
                        })
        except Exception:
            # DB fetch failed, continue with request trends only
            pass
        
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
            
            ranked_trends.append({
                'trendId': trend_id,
                'title': title,
                'description': description,
                'relevance_score': relevance_score
            })
        
        # Sort by relevance score (descending)
        ranked_trends.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Take top 5 and calculate AI Novelty for the best matches to save API tokens
        top_trends = ranked_trends[:5]
        
        # Assuming the creator has a valid niche we can extract, or default 'Creator Economy'
        creator_niche = 'Creator Economy' # We would ideally pull this from DB profile in production
        
        for trend in top_trends:
            forecast = predict_trend_trajectory(
                trend['title'], 
                trend['description'], 
                creator_niche
            )
            trend['trajectory'] = forecast['trajectory']
            trend['novelty_score'] = forecast['novelty_score']
            trend['forecast_reason'] = forecast['forecast_reason']
        
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
        import traceback
        traceback.print_exc()
        print(f"ERROR OUT: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Trend analysis failed: {str(e)}'})
        }


if __name__ == "__main__":
    # Local test
    import random
    
    # Needs to be mocked or relies on AWS credentials which are currently quarantined
    os.environ['MOCK_MODE'] = 'true'
    
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
        print(f"    AI FORECAST: {trend.get('trajectory', 'Unknown')} (Novelty: {trend.get('novelty_score', 0)})")
        print(f"    Reason: {trend.get('forecast_reason', '')}")
