# 🎬 CreatorAI TrendScribe
### AI-Driven Content Intelligence for Indian Creators
**AI for Bharat Hackathon | Team Cr8r Crew | Track: AI for Media, Content & Digital Experiences**

---

## 💡 What is it?

CreatorAI TrendScribe is an end-to-end AI pipeline that:
1. **Learns** a creator's unique style and niche from their past content (Style DNA)
2. **Discovers** trending topics semantically relevant to their domain
3. **Generates** structured, personalized video scripts in their voice — in English or Indian regional languages

> *"From trend spotted to script ready — in seconds, not hours."*

---

## 🚨 The Problem

Indian content creators face a brutal cycle:
- Spend hours manually researching what's trending in their niche
- End up with generic, off-brand AI scripts that don't sound like them
- Miss viral windows because the research-to-script process is too slow
- Regional language creators have almost no AI tooling built for them

---

## ✅ Our Solution

A RAG (Retrieval-Augmented Generation) pipeline built on AWS:

```
Creator's past content
        ↓
  Titan Embeddings (Style DNA)
        ↓
  Trend Ingestion (Google Trends, YouTube API)
        ↓
  Cosine Similarity + Novelty Scoring
        ↓
  Claude generates personalized script
        ↓
  Creator reviews, edits, publishes
```

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🧠 **Style DNA Modeling** | Analyzes creator's past content to build a semantic profile — tone, niche, examples, style |
| 🔥 **Trend-to-Script Engine** | Proactively matches emerging trends to creator's domain using embedding similarity + novelty scoring |
| 🎬 **Reel vs YouTube Mode** | One click generates both a 60-sec Reels script AND a long-form YouTube script for the same trend |
| 🪝 **Hook Scorer** | Rates your opening hook 1–10 and suggests 3 alternatives — because hooks make or break videos |
| 🌐 **Bharat-First Language** | Generates scripts in Hindi, Tamil, Telugu, Kannada and more — with cultural context, not just translation |
| 💡 **Ideation Partner** | Suggests video titles, thumbnail text, and alternative angles Claude thinks the creator hasn't covered yet |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         AWS Amplify (React Frontend)    │
└────────────────┬────────────────────────┘
                 ↓ HTTPS
┌─────────────────────────────────────────┐
│         Amazon API Gateway              │
└────────────────┬────────────────────────┘
                 ↓
┌────────────────┬────────────┬───────────┐
│ Content        │ Trend      │ Script    │
│ Processing     │ Analysis   │ Generation│
│ Lambda         │ Lambda     │ Lambda    │
└────────────────┴────────────┴───────────┘
                 ↓
┌─────────────────────────────────────────┐
│         Amazon Bedrock                  │
│  Titan Embeddings + Anthropic Claude    │
└────────────────┬────────────────────────┘
                 ↓
┌──────────────┬──────────────┬───────────┐
│ Amazon S3    │  DynamoDB    │  Cognito  │
│ (content,    │  (profiles,  │  (auth)   │
│  scripts)    │   trends)    │           │
└──────────────┴──────────────┴───────────┘
```

---

## 🛠️ Tech Stack

**Core AWS Services:**
- **Amazon Bedrock** — Titan Embeddings V1 + Anthropic Claude 3 Sonnet
- **AWS Lambda** — Serverless compute for all pipeline logic
- **Amazon S3** — Storage for transcripts and generated scripts
- **Amazon DynamoDB** — Creator profiles, embeddings, trend scores
- **Amazon API Gateway** — REST API layer
- **AWS Amplify** — Frontend hosting and deployment
- **Amazon Cognito** — User authentication

**Supporting:**
- Amazon CloudWatch — Monitoring and logging
- AWS IAM — Security and access management
- Amazon Transcribe — (Future) Auto-convert video to text

**Frontend:**
- React.js + Tailwind CSS

---

## 🗂️ Repo Structure

```
AIForBharatHackathon_Cr8rCrew/
├── README.md
├── design.md          # Full system design document
├── requirements.md    # Functional & non-functional requirements
├── frontend/          # React app (coming soon)
├── backend/
│   ├── lambdas/
│   │   ├── content-processor/
│   │   ├── trend-analyzer/
│   │   └── script-generator/
│   └── infrastructure/  # AWS CDK code
└── docs/
    └── architecture-diagram.png
```

---

## 👩💻 Team Cr8r Crew

- **Deepthi K** (Team Lead)
- **Shriya Bharadwaj**
- **Pratigya**

**Hackathon:** AI for Bharat | Powered by AWS
**Track:** AI for Media, Content & Digital Experiences

---

## 🚀 Current Status

- [x] Problem statement & solution design complete
- [x] Architecture finalized
- [x] Design document & requirements spec written
- [ ] AWS infrastructure setup (in progress)
- [ ] Lambda functions — Bedrock integration
- [ ] Frontend — React + Amplify
- [ ] End-to-end demo build

---

## 📊 Why This Matters for Bharat

- 20–25 lakh active creators in India, only 8–10% monetize effectively
- 75% of Indian internet users prefer content in their native language
- Most AI content tools are English-first and generic — we're building Bharat-first and personalized
- Regional creators from tier 2/3 cities get a "virtual content team" at zero cost

---

*Built with ❤️ for India's creator community at AI for Bharat Hackathon 2026*
