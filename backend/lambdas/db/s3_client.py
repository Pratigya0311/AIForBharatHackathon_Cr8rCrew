"""
S3 Client
Handles all interactions with S3 bucket for TrendScribe.
Stores creator content and generated scripts.
Supports MOCK_MODE for testing without AWS credentials.
"""

import os
import json
import boto3
from io import BytesIO

# Configuration from environment variables
MOCK_MODE = os.getenv('MOCK_MODE', 'false').lower() == 'true'
REGION = os.getenv('AWS_REGION', 'us-east-1')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'trendscribe-data')

# Mock storage (replaces S3 in MOCK_MODE)
_MOCK_S3_STORAGE = {}


# ============================================================================
# S3 CLIENT INITIALIZATION
# ============================================================================

def _get_s3_client():
    """Get S3 client or None if MOCK_MODE."""
    if MOCK_MODE:
        return None
    try:
        return boto3.client('s3', region_name=REGION)
    except Exception as e:
        return None


# ============================================================================
# BUCKET STRUCTURE REFERENCE
# ============================================================================

"""
users/{userId}/content/{contentId}.txt
  - Raw creator content/samples

users/{userId}/scripts/{scriptId}.json
  - Generated scripts with metadata
"""


# ============================================================================
# CONTENT OPERATIONS
# ============================================================================

def upload_content(userId, contentId, text):
    """
    Upload creator content sample to S3.
    
    Args:
        userId: Creator ID
        contentId: Unique content identifier
        text: Content text
    
    Returns:
        {success: bool, data: {key, size}, error: error_message}
    """
    try:
        key = f"users/{userId}/content/{contentId}.txt"
        
        if MOCK_MODE:
            _MOCK_S3_STORAGE[key] = text.encode('utf-8')
            return {
                'success': True,
                'data': {'key': key, 'size': len(text.encode('utf-8'))},
                'error': None
            }
        
        s3_client = _get_s3_client()
        if not s3_client:
            raise Exception("Failed to connect to S3")
        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=text.encode('utf-8'),
            ContentType='text/plain'
        )
        
        return {
            'success': True,
            'data': {'key': key, 'size': len(text.encode('utf-8'))},
            'error': None
        }
    
    except Exception as e:
        error_msg = f"Failed to upload content: {str(e)}"
        return {'success': False, 'data': None, 'error': error_msg}


def get_content(userId, contentId):
    """
    Retrieve creator content from S3.
    
    Args:
        userId: Creator ID
        contentId: Unique content identifier
    
    Returns:
        {success: bool, data: {key, text}, error: error_message}
    """
    try:
        key = f"users/{userId}/content/{contentId}.txt"
        
        if MOCK_MODE:
            if key not in _MOCK_S3_STORAGE:
                return {'success': False, 'data': None, 'error': 'Content not found'}
            
            text = _MOCK_S3_STORAGE[key].decode('utf-8')
            return {
                'success': True,
                'data': {'key': key, 'text': text},
                'error': None
            }
        
        s3_client = _get_s3_client()
        if not s3_client:
            raise Exception("Failed to connect to S3")
        
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
        text = response['Body'].read().decode('utf-8')
        
        return {
            'success': True,
            'data': {'key': key, 'text': text},
            'error': None
        }
    
    except Exception as e:
        error_msg = f"Failed to get content: {str(e)}"
        return {'success': False, 'data': None, 'error': error_msg}


# ============================================================================
# SCRIPT OPERATIONS
# ============================================================================

def save_script(userId, scriptId, script_data):
    """
    Save generated script JSON to S3.
    
    Args:
        userId: Creator ID
        scriptId: Unique script identifier
        script_data: Script dict {format, youtube_script, reel_script, etc}
    
    Returns:
        {success: bool, data: {key, size}, error: error_message}
    """
    try:
        key = f"users/{userId}/scripts/{scriptId}.json"
        json_data = json.dumps(script_data, indent=2)
        
        if MOCK_MODE:
            _MOCK_S3_STORAGE[key] = json_data.encode('utf-8')
            return {
                'success': True,
                'data': {'key': key, 'size': len(json_data.encode('utf-8'))},
                'error': None
            }
        
        s3_client = _get_s3_client()
        if not s3_client:
            raise Exception("Failed to connect to S3")
        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json_data.encode('utf-8'),
            ContentType='application/json'
        )
        
        return {
            'success': True,
            'data': {'key': key, 'size': len(json_data.encode('utf-8'))},
            'error': None
        }
    
    except Exception as e:
        error_msg = f"Failed to save script: {str(e)}"
        return {'success': False, 'data': None, 'error': error_msg}


def get_script(userId, scriptId):
    """
    Retrieve generated script from S3.
    
    Args:
        userId: Creator ID
        scriptId: Unique script identifier
    
    Returns:
        {success: bool, data: {key, script}, error: error_message}
    """
    try:
        key = f"users/{userId}/scripts/{scriptId}.json"
        
        if MOCK_MODE:
            if key not in _MOCK_S3_STORAGE:
                return {'success': False, 'data': None, 'error': 'Script not found'}
            
            json_data = _MOCK_S3_STORAGE[key].decode('utf-8')
            script_data = json.loads(json_data)
            return {
                'success': True,
                'data': {'key': key, 'script': script_data},
                'error': None
            }
        
        s3_client = _get_s3_client()
        if not s3_client:
            raise Exception("Failed to connect to S3")
        
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
        json_data = response['Body'].read().decode('utf-8')
        script_data = json.loads(json_data)
        
        return {
            'success': True,
            'data': {'key': key, 'script': script_data},
            'error': None
        }
    
    except Exception as e:
        error_msg = f"Failed to get script: {str(e)}"
        return {'success': False, 'data': None, 'error': error_msg}


# ============================================================================
# LOCAL TEST BLOCK
# ============================================================================

if __name__ == "__main__":
    os.environ['MOCK_MODE'] = 'true'
    
    print("\nS3 Client - Mock Mode Test")
    print("="*60)
    
    # Test upload content
    result = upload_content('creator_001', 'content_001', 'Sample creator content here')
    print(f"Upload Content: {result['success']}")
    
    # Test get content
    result = get_content('creator_001', 'content_001')
    print(f"Get Content: {result['success']}")
    
    # Test save script
    result = save_script(
        'creator_001',
        'script_001',
        {
            'format': 'youtube',
            'title': 'Test Script',
            'hook': 'Catchy hook here'
        }
    )
    print(f"Save Script: {result['success']}")
    
    # Test get script
    result = get_script('creator_001', 'script_001')
    print(f"Get Script: {result['success']}")
    
    print("="*60 + "\n")
