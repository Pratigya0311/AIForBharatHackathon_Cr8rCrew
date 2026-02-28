"""
DynamoDB Client
Handles all interactions with DynamoDB tables for TrendScribe.
Supports MOCK_MODE for testing without AWS credentials.
"""

import os
import json
import boto3
from datetime import datetime, timedelta, timezone

# Configuration from environment variables
MOCK_MODE = os.getenv('MOCK_MODE', 'false').lower() == 'true'
REGION = os.getenv('AWS_REGION', 'us-east-1')
CREATOR_PROFILES_TABLE = os.getenv('CREATOR_PROFILES_TABLE', 'CreatorProfiles')
SCRIPTS_TABLE = os.getenv('SCRIPTS_TABLE', 'Scripts')
TRENDS_TABLE = os.getenv('TRENDS_TABLE', 'Trends')

# Mock storage (replaces DynamoDB in MOCK_MODE)
_MOCK_CREATOR_PROFILES = {}
_MOCK_SCRIPTS = {}
_MOCK_TRENDS = {}


# ============================================================================
# TABLE SCHEMAS
# ============================================================================

"""
CreatorProfiles Table:
  PK: userId
  Attributes:
    - style_dna: dict
    - embedding: list (1536 dimensions)
    - niche: string
    - language: string
    - createdAt: ISO timestamp

Scripts Table:
  PK: scriptId
  SK: userId
  Attributes:
    - trend: dict
    - format: string (youtube|reel|both)
    - youtube_script: dict (optional)
    - reel_script: dict (optional)
    - hook_scores: dict
    - language: string
    - createdAt: ISO timestamp

Trends Table:
  PK: trendId
  Attributes:
    - title: string
    - description: string
    - embedding: list (1536 dimensions)
    - createdAt: ISO timestamp
    - expiresAt: ISO timestamp (TTL for 48-hour auto-delete)
"""


# ============================================================================
# DYNAMODB CLIENT INITIALIZATION
# ============================================================================

def _get_dynamodb_client():
    """Get DynamoDB client or None if MOCK_MODE."""
    if MOCK_MODE:
        return None
    try:
        return boto3.resource('dynamodb', region_name=REGION)
    except Exception as e:
        return None


# ============================================================================
# CREATOR PROFILES TABLE OPERATIONS
# ============================================================================

def save_creator_profile(userId, style_dna, embedding, niche, language='en'):
    """
    Save or update creator profile.
    
    Args:
        userId: Unique creator identifier
        style_dna: Dict with niche, tone, style, key_phrases, target_audience
        embedding: 1536-dimensional embedding vector
        niche: Creator's content niche
        language: Content language (default: 'en')
    
    Returns:
        {success: bool, data: created_record, error: error_message}
    """
    try:
        record = {
            'userId': userId,
            'style_dna': json.dumps(style_dna),
            'embedding': embedding,
            'niche': niche,
            'language': language,
            'createdAt': datetime.now(timezone.utc).isoformat()
        }
        
        if MOCK_MODE:
            _MOCK_CREATOR_PROFILES[userId] = record
            return {'success': True, 'data': record, 'error': None}
        
        dynamodb = _get_dynamodb_client()
        if not dynamodb:
            raise Exception("Failed to connect to DynamoDB")
        
        table = dynamodb.Table(CREATOR_PROFILES_TABLE)
        table.put_item(Item=record)
        
        return {'success': True, 'data': record, 'error': None}
    
    except Exception as e:
        error_msg = f"Failed to save creator profile: {str(e)}"
        return {'success': False, 'data': None, 'error': error_msg}


def get_creator_profile(userId):
    """
    Retrieve creator profile by userId.
    
    Args:
        userId: Unique creator identifier
    
    Returns:
        {success: bool, data: creator_record, error: error_message}
    """
    try:
        if MOCK_MODE:
            profile = _MOCK_CREATOR_PROFILES.get(userId)
            if not profile:
                return {'success': False, 'data': None, 'error': 'Creator profile not found'}
            return {'success': True, 'data': profile, 'error': None}
        
        dynamodb = _get_dynamodb_client()
        if not dynamodb:
            raise Exception("Failed to connect to DynamoDB")
        
        table = dynamodb.Table(CREATOR_PROFILES_TABLE)
        response = table.get_item(Key={'userId': userId})
        
        if 'Item' not in response:
            return {'success': False, 'data': None, 'error': 'Creator profile not found'}
        
        return {'success': True, 'data': response['Item'], 'error': None}
    
    except Exception as e:
        error_msg = f"Failed to get creator profile: {str(e)}"
        return {'success': False, 'data': None, 'error': error_msg}


# ============================================================================
# SCRIPTS TABLE OPERATIONS
# ============================================================================

def save_script(userId, trend, format_type, youtube_script=None, reel_script=None, hook_scores=None, language='en'):
    """
    Save generated script(s).
    
    Args:
        userId: Creator ID
        trend: Trend dict {trendId, title, description}
        format_type: 'youtube' | 'reel' | 'both'
        youtube_script: YouTube script dict (optional)
        reel_script: Reel script dict (optional)
        hook_scores: Hook scoring dict {youtube_score, reel_score}
        language: Content language (default: 'en')
    
    Returns:
        {success: bool, data: script_record, error: error_message}
    """
    try:
        scriptId = f"script_{userId}_{datetime.now(timezone.utc).timestamp()}"
        
        record = {
            'scriptId': scriptId,
            'userId': userId,
            'trend': json.dumps(trend),
            'format': format_type,
            'language': language,
            'createdAt': datetime.now(timezone.utc).isoformat()
        }
        
        if youtube_script:
            record['youtube_script'] = json.dumps(youtube_script)
        if reel_script:
            record['reel_script'] = json.dumps(reel_script)
        if hook_scores:
            record['hook_scores'] = json.dumps(hook_scores)
        
        if MOCK_MODE:
            _MOCK_SCRIPTS[scriptId] = record
            return {'success': True, 'data': record, 'error': None}
        
        dynamodb = _get_dynamodb_client()
        if not dynamodb:
            raise Exception("Failed to connect to DynamoDB")
        
        table = dynamodb.Table(SCRIPTS_TABLE)
        table.put_item(Item=record)
        
        return {'success': True, 'data': record, 'error': None}
    
    except Exception as e:
        error_msg = f"Failed to save script: {str(e)}"
        return {'success': False, 'data': None, 'error': error_msg}


def get_scripts_by_user(userId, limit=10):
    """
    Retrieve last N scripts for a user (max 10).
    
    Args:
        userId: Creator ID
        limit: Max scripts to return (default: 10)
    
    Returns:
        {success: bool, data: scripts_list, error: error_message}
    """
    try:
        limit = min(limit, 10)  # Max 10 scripts
        
        if MOCK_MODE:
            user_scripts = [s for s in _MOCK_SCRIPTS.values() if s['userId'] == userId]
            user_scripts = sorted(user_scripts, key=lambda x: x['createdAt'], reverse=True)[:limit]
            return {'success': True, 'data': user_scripts, 'error': None}
        
        dynamodb = _get_dynamodb_client()
        if not dynamodb:
            raise Exception("Failed to connect to DynamoDB")
        
        table = dynamodb.Table(SCRIPTS_TABLE)
        response = table.query(
            KeyConditionExpression='userId = :userId',
            ExpressionAttributeValues={':userId': userId},
            Limit=limit,
            ScanIndexForward=False  # Most recent first
        )
        
        return {'success': True, 'data': response.get('Items', []), 'error': None}
    
    except Exception as e:
        error_msg = f"Failed to get scripts by user: {str(e)}"
        return {'success': False, 'data': None, 'error': error_msg}


# ============================================================================
# TRENDS TABLE OPERATIONS
# ============================================================================

def save_trend(trendId, title, description, embedding, ttl_hours=48):
    """
    Save trending topic with TTL for auto-expiration.
    
    Args:
        trendId: Unique trend identifier
        title: Trend title
        description: Trend description
        embedding: 1536-dimensional embedding vector
        ttl_hours: Hours until auto-delete (default: 48)
    
    Returns:
        {success: bool, data: trend_record, error: error_message}
    """
    try:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(hours=ttl_hours)
        
        record = {
            'trendId': trendId,
            'title': title,
            'description': description,
            'embedding': embedding,
            'createdAt': now.isoformat(),
            'expiresAt': expires_at.isoformat(),
            'ttl': int(expires_at.timestamp())  # Unix timestamp for DynamoDB TTL
        }
        
        if MOCK_MODE:
            _MOCK_TRENDS[trendId] = record
            return {'success': True, 'data': record, 'error': None}
        
        dynamodb = _get_dynamodb_client()
        if not dynamodb:
            raise Exception("Failed to connect to DynamoDB")
        
        table = dynamodb.Table(TRENDS_TABLE)
        table.put_item(Item=record)
        
        return {'success': True, 'data': record, 'error': None}
    
    except Exception as e:
        error_msg = f"Failed to save trend: {str(e)}"
        return {'success': False, 'data': None, 'error': error_msg}


def get_all_trends(limit=50):
    """
    Retrieve all active trends (including non-expired ones).
    
    Args:
        limit: Max trends to return (default: 50)
    
    Returns:
        {success: bool, data: trends_list, error: error_message}
    """
    try:
        if MOCK_MODE:
            now = datetime.now(timezone.utc).isoformat()
            active_trends = [t for t in _MOCK_TRENDS.values() if t['expiresAt'] > now]
            active_trends = sorted(active_trends, key=lambda x: x['createdAt'], reverse=True)[:limit]
            return {'success': True, 'data': active_trends, 'error': None}
        
        dynamodb = _get_dynamodb_client()
        if not dynamodb:
            raise Exception("Failed to connect to DynamoDB")
        
        table = dynamodb.Table(TRENDS_TABLE)
        response = table.scan(Limit=limit)
        
        now = datetime.now(timezone.utc).isoformat()
        active_items = [item for item in response.get('Items', []) if item.get('expiresAt', '') > now]
        
        return {'success': True, 'data': active_items, 'error': None}
    
    except Exception as e:
        error_msg = f"Failed to get trends: {str(e)}"
        return {'success': False, 'data': None, 'error': error_msg}


# ============================================================================
# LOCAL TEST BLOCK
# ============================================================================

if __name__ == "__main__":
    os.environ['MOCK_MODE'] = 'true'
    
    print("\nDynamoDB Client - Mock Mode Test")
    print("="*60)
    
    # Test save creator profile
    result = save_creator_profile(
        userId='test_creator_001',
        style_dna={'niche': 'AI', 'tone': 'Professional'},
        embedding=[0.1] * 1536,
        niche='AI and ML'
    )
    print(f"Save Creator Profile: {result['success']}")
    
    # Test get creator profile
    result = get_creator_profile('test_creator_001')
    print(f"Get Creator Profile: {result['success']}")
    
    # Test save script
    result = save_script(
        userId='test_creator_001',
        trend={'trendId': 'trend_001', 'title': 'AI Trends'},
        format_type='youtube',
        youtube_script={'title': 'Test', 'hook': 'Test hook'}
    )
    print(f"Save Script: {result['success']}")
    
    # Test get scripts by user
    result = get_scripts_by_user('test_creator_001')
    print(f"Get Scripts by User: {result['success']} (count: {len(result['data'])})")
    
    # Test save trend
    result = save_trend(
        trendId='trend_001',
        title='AI Trends',
        description='AI revolution',
        embedding=[0.2] * 1536
    )
    print(f"Save Trend: {result['success']}")
    
    # Test get all trends
    result = get_all_trends()
    print(f"Get All Trends: {result['success']} (count: {len(result['data'])})")
    
    print("="*60 + "\n")
