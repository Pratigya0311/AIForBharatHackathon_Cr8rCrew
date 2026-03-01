"""
Embedding generation and similarity matching functions.
Uses Titan embeddings for Style DNA and trend matching.
"""

import numpy as np
import json
from .bedrock_client import call_titan, call_claude


def generate_embedding(text):
    """
    Generate a 1536-dimensional embedding vector for text using Titan.
    
    Args:
        text (str): Text to embed
    
    Returns:
        list: 1536-dimensional embedding vector
    
    Raises:
        Exception: If embedding generation fails
    """
    try:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        embedding = call_titan(text)
        return embedding
    except Exception as e:
        raise Exception(f"Embedding generation failed: {str(e)}")


def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1 (list): First vector (1536-dim)
        vec2 (list): Second vector (1536-dim)
    
    Returns:
        float: Cosine similarity score (0-1)
    
    Raises:
        Exception: If vectors are invalid
    """
    try:
        vec1 = np.array(vec1, dtype=np.float32)
        vec2 = np.array(vec2, dtype=np.float32)
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        # Ensure result is in 0-1 range
        return float(np.clip(similarity, 0, 1))
    
    except Exception as e:
        raise Exception(f"Cosine similarity calculation failed: {str(e)}")


def match_trend_to_creator(creator_text, trend_text):
    """
    Match a trending topic to creator's domain using embeddings and cosine similarity.
    
    Args:
        creator_text (str): Creator's sample content
        trend_text (str): Trending topic description
    
    Returns:
        dict: {
            'relevance_score': float (0-1),
            'is_relevant': bool (True if similarity > 0.6)
        }
    
    Raises:
        Exception: If matching fails
    """
    try:
        print("\n  Generating creator's Style DNA embedding...")
        creator_embedding = generate_embedding(creator_text)
        
        print("  Generating trend embedding...")
        trend_embedding = generate_embedding(trend_text)
        
        print("  Calculating cosine similarity...")
        score = cosine_similarity(creator_embedding, trend_embedding)
        
        is_relevant = score > 0.6  # Relevance threshold
        
        return {
            'relevance_score': round(score, 3),
            'is_relevant': is_relevant
        }
    
    except Exception as e:
        raise Exception(f"Trend-to-creator matching failed: {str(e)}")


def extract_style_dna(sample_content):
    """
    Extract creator's Style DNA (tone, style, personality) from sample content.
    Calls Claude to analyze the content and return a structured creator profile.
    
    Args:
        sample_content (str): Creator's past content samples (transcripts/blogs)
    
    Returns:
        dict: Creator profile with keys:
            - niche: Creator's niche (e.g., "AI/ML for Indian startups")
            - tone: Writing tone (e.g., "conversational, tech-forward")
            - style: Content style (e.g., "narrative-driven with examples")
            - key_phrases: List of phrases the creator often uses
            - target_audience: Who the creator speaks to
    
    Raises:
        Exception: If Claude API call fails or response cannot be parsed
    """
    try:
        system_prompt = """You are an AI content analyst specializing in creator profiles.
        Analyze the given sample content and extract the creator's Style DNA - their unique voice, tone, style, and personality.
        Return a JSON object with these keys (and nothing else):
        - niche: The creator's main topic area
        - tone: Descriptive tone (friendly, technical, casual, formal, etc.)
        - style: How they structure content (storytelling, educational, conversational, etc.)
        - key_phrases: List of 5 phrases they frequently use or would use
        - target_audience: Who they're speaking to
        Be specific and extract real patterns from the content."""
        
        prompt = f"""{system_prompt}

CREATOR'S SAMPLE CONTENT:
{sample_content}

Return ONLY valid JSON, no other text."""
        
        response_text = call_claude(prompt, max_tokens=500)
        
        # Parse JSON response
        profile = json.loads(response_text)
        return profile
    
    except json.JSONDecodeError as e:
        raise Exception(f"Claude returned invalid JSON for Style DNA: {str(e)}")
    except Exception as e:
        raise Exception(f"Style DNA extraction failed: {str(e)}")
