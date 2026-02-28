# Phase 1: Core AI Functions

## The Main Pieces

### 1. Bedrock Client (`bedrock_client.py`)
This talks to AWS. Two simple functions:
- `call_claude()` - Ask Claude a question
- `call_titan()` - Turn text into numbers (embeddings)

### 2. Embeddings (`embeddings.py`)
This finds patterns in text:
- `generate_embedding()` - Convert text to a 1536-number vector
- `cosine_similarity()` - Check if two texts are similar (0 to 1)
- `extract_style_dna()` - Understand a creator's voice, tone, style from their past content
- `match_trend_to_creator()` - See if a trending topic fits with what the creator makes

### 3. Script Generator (`script_generator.py`)
This creates the actual scripts:
- `generate_youtube_script()` - Make an 8-12 minute YouTube script
- `generate_reel_script()` - Make a 30-60 second Reel script
- `score_hook()` - Rate how good a hook is (1-10) and suggest 3 better ones

## How It Works (Simple Version)

**Step 1**: Creator gives us some of their old content (blog, transcript, past video)
↓
**Step 2**: Claude reads it and figures out their voice → Style DNA
↓
**Step 3**: User picks a trending topic
↓
**Step 4**: We check if the trend matches the creator's niche using embeddings
↓
**Step 5**: If it matches, Claude generates a personalized script using the creator's voice
↓
**Step 6**: Done! Creator gets a script that sounds like them

## Key Feature: "One Button, Both Outputs"

You can ask for:
- Just YouTube script
- Just Reel script  
- Both at once

Same trend, two different lengths. Perfect for creators who post on both platforms.

## The Data

When you send content to Phase 1, it extracts:
```
Style DNA = {
  niche: "what they make about",
  tone: "how they talk",
  style: "how they structure content",
  key_phrases: ["words they use"],
  target_audience: "who they talk to"
}
```

When you generate a script:
```
Script = {
  title: "...",
  hook: "...",
  sections: ["...", "...", "..."],
  conclusion: "...",
  call_to_action: "..."
}
```

## Testing

Run the test (no AWS needed):
```bash
cd backend
python tests/test_phase1.py
```

## For Phase 2

The Lambda handlers will wrap these functions as API endpoints:
- `POST /creator/profile` - Extract Style DNA
- `GET /trends` - List trending topics
- `POST /scripts/generate` - Make scripts (format: youtube/reel/both)
- `POST /hooks/score` - Score a hook

When you call the API, it will:
1. Use Phase 1 functions to do the AI work
2. Store the results in DynamoDB
3. Send back the script to the creator

## Under the Hood: Why This Is Good

- **Not repetitive**: One hook, variations for any creator
- **Personalized**: Uses their actual voice, not generic AI
- **Fast**: ~2-3 seconds for a YouTube script, ~1-2 for a Reel
- **Scalable**: Can handle hundreds of creators
- **Platform-smart**: Knows the difference between YouTube and Reels




