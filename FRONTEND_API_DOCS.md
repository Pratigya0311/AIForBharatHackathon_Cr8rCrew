# TrendScribe Serverless API Documentation

This document explains how to interact with the **TrendScribe Serverless API**. All endpoints accept and return `application/json`.

## Endpoints Overview

### 1. Generate Scripts & Titles
Generates YouTube or Reel scripts based on a given trend and the creator's style profile.

**`POST /scripts/generate`**

**Request:**
```json
{
  "userId": "creator_123",
  "trend": {
    "title": "AI in the Creator Economy",
    "description": "How to scale your content using Claude and Bedrock",
    "context": "A rising trend in 2026 for tech creators"
  },
  "creator_profile": {
    "niche": "Tech & AI for Indian Creators",
    "tone": "Casual and highly energetic",
    "style": "Fast-paced storytelling with specific examples"
  },
  "format": "both", // "youtube", "reel", or "both"
  "language": "en",  // Options: "en", "hi", "ta", "te", "kn", "mr" (For Native Indian Languages)
  "options": {
    "length": "5-8 minutes", // Or "short and punchy", "30-60 seconds"
    "tone": "humorous", // E.g., "professional", "casual", "urgent"
    "structure": "educational tutorial" // E.g., "review", "storytime"
  }
}
```

**Response (200 OK):**
```json
{
  "userId": "creator_123",
  "format": "both",
  "language": "en",
  "scriptId": "script_creator_123_1772348494",
  "youtube_script": {
    "title": "Main Generated Title",
    "viral_title_ideas": [
      "I 10x'd My YouTube Growth With This AI Tool",
      "The AI Setup Every Indian Creator Needs in 2026",
      "Stop Making Content Manually (Do This Instead)"
    ],
    "thumbnail_ideas": [
      "Split screen: Sad creator at desk vs Creator relaxing on beach. Text: '10x FASTER'"
    ],
    "hook": "Imagine producing content 10x faster while earning 10x more.",
    "hook_score": {
      "score": 8,
      "feedback": "Strong hook with immediate value proposition.",
      "alternatives": ["In 2026, creators using AI are earning 5x more..."]
    },
    "section_1": "First, let's understand... [VISUAL: Show B-Roll of creators looking stressed]",
    "section_2": "Here's the real secret...",
    "section_3": "Now let me show you...",
    "conclusion": "The opportunity is massive.",
    "cta": "Drop a comment below!"
  },
  "reel_script": {
    "title": "How AI Can 10x Your Content Production",
    "viral_title_ideas": ["My Secret AI Creator Stack 🤫"],
    "hook": "Most creators are still manual... [VISUAL: TEXT ON SCREEN 'SMART CREATORS']",
    "hook_score": {
      "score": 8,
      "feedback": "Good attention grabber.",
      "alternatives": ["Stop scrolling if you want to grow..."]
    },
    "body": "ChatGPT and Claude aren't just tools...",
    "cta": "Watch the full video - link in bio.",
    "hashtags": ["#AIForCreators", "#GenAI2026", "#ContentCreation"]
  }
}
```

---

### 2. Process Creator Content (Style DNA)
Uploads text/transcript from a creator to extract their unique "Style DNA" and store it in DynamoDB.

**`POST /content/process`**

**Request:**
```json
{
  "userId": "creator_123",
  "contentId": "video_transcript_001",
  "text": "Hey guys, honestly the future of AI is crazy. You need to build your stack today. If you're missing out, you're losing money!"
}
```

**Response (200 OK):**
```json
{
  "userId": "creator_123",
  "status": "success",
  "style_dna": {
    "niche": "AI & Tech Entrepreneurship",
    "tone": "Energetic, urgent, conversational",
    "style": "Direct-to-camera advice",
    "key_phrases": ["honestly", "build your stack", "losing money"],
    "target_audience": "Ambitious creators and tech enthusiasts"
  }
}
```

---

### 3. Analyze & Rank Trends
Fetches trending topics and ranks them against the Creator's specific Style DNA.

**`POST /trends/analyze`**

**Request:**
```json
{
  "userId": "creator_123",
  "trends": [
    {
      "title": "Generative AI Agents",
      "description": "Autonomous AI systems that execute complex tasks."
    },
    {
      "title": "Baking Sourdough Bread",
      "description": "Techniques for high hydration sourdough."
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "userId": "creator_123",
  "ranked_trends": [
    {
      "trendId": "trend_001",
      "title": "Generative AI Agents",
      "description": "Autonomous AI systems that execute complex tasks.",
      "relevance_score": 0.92,
      "trajectory": "Rising",     // Options: "Rising", "Peaking", "Falling"
      "novelty_score": 85,        // Scale of 1-100 (100 is completely untapped and fresh)
      "forecast_reason": "Rapid early adoption in tech niches but yet to hit mainstream lifestyle creators."
    },
    {
      "trendId": "trend_002",
      "title": "Baking Sourdough Bread",
      "description": "Techniques for high hydration sourdough.",
      "relevance_score": 0.12,
      "trajectory": "Falling",
      "novelty_score": 30,
      "forecast_reason": "Trend peaked during 2020 lockdowns and has since oversaturated the market."
    }
  ]
}
```
