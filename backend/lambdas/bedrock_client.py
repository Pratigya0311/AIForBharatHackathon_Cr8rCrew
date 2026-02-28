"""
Shared Bedrock boto3 client setup and reusable API calls.
Handles authentication via environment variables:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION
"""

import boto3
import os
import json

# Initialize Bedrock client with credentials from environment
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)


def call_claude(prompt, max_tokens=2000):
    """
    Call Claude 3 Sonnet via Bedrock with a prompt.
    
    Args:
        prompt (str): The input prompt for Claude
        max_tokens (int): Maximum tokens in response (default 2000)
    
    Returns:
        str: Claude's response text
    
    Raises:
        Exception: If Bedrock API call fails
    """
    try:
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-06-01",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
    
    except Exception as e:
        raise Exception(f"Claude API call failed: {str(e)}")


def call_titan(text):
    """
    Call Titan Embeddings V1 via Bedrock to generate embeddings.
    
    Args:
        text (str): The text to embed
    
    Returns:
        list: 1536-dimensional embedding vector
    
    Raises:
        Exception: If Bedrock API call fails
    """
    try:
        model_id = "amazon.titan-embed-text-v1"
        
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({"inputText": text})
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        return response_body['embedding']
    
    except Exception as e:
        raise Exception(f"Titan Embeddings API call failed: {str(e)}")
