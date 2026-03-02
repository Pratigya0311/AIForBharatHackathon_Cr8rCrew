"""
Script generation functions for YouTube and Reels.
Uses Claude to generate personalized video scripts based on creator's Style DNA and trends.
"""

import json
from .bedrock_client import call_claude


def generate_youtube_script(creator_profile, trend, language_code="en", options=None):
    """
    Generate a long-form YouTube script based on creator's profile, trend, and customizations.
    
    Args:
        creator_profile (dict): Creator's Style DNA with keys: niche, tone, style, key_phrases, target_audience
        trend (dict): Trend data with keys: title, description, context
        language_code (str): Language code (e.g. 'en', 'hi', 'ta')
        options (dict): Customization options: length, tone, structure
    
    Returns:
        dict: Script structure with keys:
            - title: Video title
            - hook: 30-second hook to grab attention
            - section_1: First main section (2-3 min)
            - section_2: Second main section (2-3 min)
            - section_3: Third main section (2-3 min)
            - conclusion: Closing remarks
            - cta: Call-to-action
    
    Raises:
        Exception: If script generation fails
    """
    try:
        prompt_template = """You are a world-class YouTube script writer specializing in Indian creator content.

CREATOR'S VOICE & STYLE:
- Niche: {niche}
- Tone: {tone}
- Style: {style}
- Key phrases they use: {key_phrases}
- Target audience: {target_audience}

TRENDING TOPIC:
- Title: {trend_title}
- Description: {trend_description}
- Context: {trend_context}

TARGET LANGUAGE: {target_language}

TASK: Write a YouTube video script ({video_length}) that:
1. Opens with a compelling 30-second hook
2. Is structured as a "{video_structure}" video
3. Has main sections (adjusted for {video_length})
4. Ends with a strong conclusion and CTA
5. Uses the creator's actual voice and tone throughout ({target_tone})
6. Includes specific examples relevant to the trend
7. Sounds human and natural, NOT like AI
8. Integrates [VISUAL: ...] cues throughout the script for B-roll, Text-on-Screen, and Editor notes

Format your response as a JSON object with these EXACT keys:
{{
    "title": "Video title here",
    "viral_title_ideas": ["Clickable Title 1", "Curiosity Title 2", "SEO-optimized Title 3"],
    "thumbnail_ideas": ["Visual description + Text for Thumbnail 1", "Thumbnail idea 2", "Thumbnail idea 3"],
    "hook": "30-second hook...",
    "section_1": "First section content...",
    "section_2": "Second section content...",
    "section_3": "Third section content...",
    "conclusion": "Closing remarks...",
    "cta": "Call-to-action..."
}}

Return ONLY the JSON object, no other text."""
        
        lang_map = {'en': 'English', 'hi': 'Hindi / Hinglish (natural spoken)', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada', 'mr': 'Marathi'}
        target_lang = lang_map.get(language_code.lower(), 'English')
        
        options = options or {}
        target_tone = options.get('tone', creator_profile.get('tone', 'Conversational'))
        video_length = options.get('length', '8-12 minutes')
        video_structure = options.get('structure', 'educational')
        
        prompt = prompt_template.format(
            niche=creator_profile.get('niche', 'Not specified'),
            tone=target_tone,
            style=creator_profile.get('style', 'Narrative-driven'),
            key_phrases=', '.join(creator_profile.get('key_phrases', [])),
            target_audience=creator_profile.get('target_audience', 'Tech enthusiasts'),
            trend_title=trend.get('title', 'New Trend'),
            trend_description=trend.get('description', ''),
            trend_context=trend.get('context', ''),
            target_language=target_lang,
            video_length=video_length,
            video_structure=video_structure,
            target_tone=target_tone
        )
        
        response_text = call_claude(prompt, max_tokens=3000)
        script = json.loads(response_text)
        return script
    
    except json.JSONDecodeError as e:
        raise Exception(f"Claude returned invalid JSON for YouTube script: {str(e)}")
    except Exception as e:
        raise Exception(f"YouTube script generation failed: {str(e)}")


def generate_reel_script(creator_profile, trend, language_code="en", options=None):
    """
    Generate a short-form Reel/Instagram script based on creator's profile, trend, and customizations.
    
    Args:
        creator_profile (dict): Creator's Style DNA with keys: niche, tone, style, key_phrases, target_audience
        trend (dict): Trend data with keys: title, description, context
        language_code (str): Language code (e.g. 'en', 'hi', 'ta')
        options (dict): Customization options: length, tone, structure
    
    Returns:
        dict: Reel script structure with keys:
            - title: Reel title/hook
            - hook: Explosive first 3 seconds
            - body: Main content (15-20 sec)
            - cta: Call-to-action with hook to full video
            - hashtags: Relevant hashtags
    
    Raises:
        Exception: If script generation fails
    """
    try:
        prompt_template = """You are a viral Reel/Short-form content expert for Indian creators.

CREATOR'S VOICE & STYLE:
- Niche: {niche}
- Tone: {tone}
- Style: {style}
- Key phrases they use: {key_phrases}
- Target audience: {target_audience}

TRENDING TOPIC:
- Title: {trend_title}
- Description: {trend_description}

TARGET LANGUAGE: {target_language}

TASK: Write a Reel/Instagram Short script ({video_length}) that:
1. Starts with a HOOK that makes people stop scrolling (first 3 seconds are CRITICAL)
2. Is structured as a "{video_structure}" video
3. Uses the creator's requested tone ({target_tone})
4. Ends with a CTA that drives engagement or links to full video
5. Includes 5 relevant hashtags
6. Is punchy, memorable, and shareable
7. Integrates [VISUAL: ...] cues (e.g. TEXT ON SCREEN, POP-UP GRAPHICS, B-ROLL) directly into the script body

Format your response as a JSON object with these EXACT keys:
{{
    "title": "Reel title/main hook",
    "viral_title_ideas": ["Viral Title 1", "Curiosity Title 2", "Shareable Title 3"],
    "hook": "First 3 seconds (the stopper)...",
    "body": "Main content (15-20 sec)...",
    "cta": "Call-to-action to drive engagement...",
    "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3", "#hashtag4", "#hashtag5"]
}}

Return ONLY the JSON object, no other text."""
        
        lang_map = {'en': 'English', 'hi': 'Hindi / Hinglish (natural spoken)', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada', 'mr': 'Marathi'}
        target_lang = lang_map.get(language_code.lower(), 'English')
        
        options = options or {}
        target_tone = options.get('tone', creator_profile.get('tone', 'Conversational'))
        video_length = options.get('length', '30-60 seconds')
        video_structure = options.get('structure', 'entertainment/value-driven')

        prompt = prompt_template.format(
            niche=creator_profile.get('niche', 'Not specified'),
            tone=target_tone,
            style=creator_profile.get('style', 'Quick-paced'),
            key_phrases=', '.join(creator_profile.get('key_phrases', [])),
            target_audience=creator_profile.get('target_audience', 'Tech enthusiasts'),
            trend_title=trend.get('title', 'New Trend'),
            trend_description=trend.get('description', ''),
            target_language=target_lang,
            video_length=video_length,
            video_structure=video_structure,
            target_tone=target_tone
        )
        
        response_text = call_claude(prompt, max_tokens=1000)
        reel = json.loads(response_text)
        return reel
    
    except json.JSONDecodeError as e:
        raise Exception(f"Claude returned invalid JSON for Reel script: {str(e)}")
    except Exception as e:
        raise Exception(f"Reel script generation failed: {str(e)}")


def score_hook(hook_text, niche):
    """
    Score a hook on a scale of 1-10 and suggest 3 alternative hooks.
    
    Args:
        hook_text (str): The hook to score
        niche (str): Creator's niche for context
    
    Returns:
        dict: Hook evaluation with keys:
            - score: Rating 1-10
            - feedback: Why it scored that way
            - alternatives: List of 3 alternative hooks
    
    Raises:
        Exception: If scoring fails
    """
    try:
        prompt_template = """You are a viral content expert and hook specialist.

CREATOR'S NICHE: {niche}

HOOK TO EVALUATE: "{hook_text}"

TASK: 
1. Score this hook on a scale of 1-10 based on:
   - Attention-grabbing power
   - Relevance to niche
   - Clarity and intrigue
   - Call-to-action strength

2. Give brief feedback on why it scored that way (max 2 sentences)

3. Suggest 3 ALTERNATIVE hooks that would work better

Format your response as a JSON object with these EXACT keys:
{{
    "score": 8,
    "feedback": "This hook is engaging but could be more specific...",
    "alternatives": [
        "Alternative hook 1...",
        "Alternative hook 2...",
        "Alternative hook 3..."
    ]
}}

Return ONLY the JSON object, no other text."""
        
        prompt = prompt_template.format(
            niche=niche,
            hook_text=hook_text
        )
        
        response_text = call_claude(prompt, max_tokens=800)
        evaluation = json.loads(response_text)
        return evaluation
    
    except json.JSONDecodeError as e:
        raise Exception(f"Claude returned invalid JSON for hook scoring: {str(e)}")
    except Exception as e:
        raise Exception(f"Hook scoring failed: {str(e)}")
