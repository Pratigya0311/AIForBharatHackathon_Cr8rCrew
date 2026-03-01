# 🎬 CreatorAI TrendScribe

**AI for Bharat Hackathon | Team Cr8r Crew**
*Track: AI for Media, Content & Digital Experiences*

CreatorAI TrendScribe is an end-to-end AI pipeline that learns a creator's unique Style DNA, discovers trending topics, and generates personalized video scripts in their voice—in English or native Indian languages.

---

## ⚡ What We Built For The Hackathon

We have completely finished **Phase 1, 2, and 3** of the Backend Serverless architecture powered by Amazon Bedrock (Claude 3 Sonnet + Titan Embeddings).

Our AI generates incredibly human-like JSON payloads that include:
- **Viral Title Ideas** (For A/B Testing)
- **Thumbnail Concept Prompts**
- **Automatic Hook Scoring (1-10)**
- **[VISUAL] B-Roll Cues embedded in the script**
- **Native Translation (Hindi, Tamil, Telugu, etc.)**

---

## 🎨 Attention Frontend Developers!

We have deleted all the old clunky backend documentation so you can focus strictly on building a winning, beautiful UI. 

👉 **Please read the [Frontend API Docs](./FRONTEND_API_DOCS.md) for the exact JSON structures you need to build the dashboard.**

Your goal is to take the structured JSON responses from our API and build a stunning, "human-like" interactive React/Vite dashboard to wow the hackathon judges.

---

## 🛠️ Testing Locally

The backend currently has **MOCK_MODE enabled**, meaning you can run the entire API pipeline locally to test your frontend *without* needing active AWS Bedrock credentials. 

To run the integration test suite and see the magic in action:
```bash
python backend/tests/test_script_generation.py
```
*(You will see 5/5 tests pass, simulating the entire Cloud architecture locally).*
