# TrendScribe: Complete Architecture and Implementation

## Project Overview

TrendScribe is an AI-powered video script generator for Indian creators. It analyzes what creators are known for (their style, voice, audience) and generates personalized video scripts for trending topics in their niche. Created during the AI For Bharat Hackathon.

The system spans three layers: core AI functions, API handlers, and cloud infrastructure, all fully tested and integrated.

## Technology Stack

**AI/Language Models:**
- AWS Bedrock with Claude 3 Sonnet (text generation)
- AWS Titan Embeddings V1 (1536-dimensional semantic vectors)

**Cloud Infrastructure:**
- AWS Lambda (3 serverless handlers)
- AWS DynamoDB (3 tables: CreatorProfiles, Scripts, Trends)
- AWS S3 (versioned bucket for content and script storage)
- AWS CDK (Infrastructure as Code)
- API Gateway + Cognito (unified endpoint and authentication)

**Languages & Frameworks:**
- Python 3.x (all backend code)
- unittest.mock (testing framework)
- AWS SDKs (boto3 for clients)

## Architecture Components

### Layer 1: Core AI Functions (Phase 1)

**File: backend/lambdas/bedrock_client.py (80 lines)**
- `call_claude(prompt)` - Sends requests to Claude 3 Sonnet for text generation
- `call_titan(text)` - Generates 1536-dimensional embeddings for semantic analysis

**File: backend/lambdas/embeddings.py (153 lines)**
- `generate_embedding(text)` - Converts text to vector representation
- `cosine_similarity(vec1, vec2)` - Computes similarity between two embeddings (0-1 scale)
- `extract_style_dna(creator_content)` - Analyzes creator's past content to determine:
  - Niche (topic focus)
  - Tone (communication style)
  - Target audience demographics
  - Key phrases and speaking patterns
- `match_trend_to_creator(trend, creator_profile)` - Checks semantic fit between trending topic and creator's niche

**File: backend/lambdas/script_generator.py (221 lines)**
- `generate_youtube_script(trend, creator_profile)` - Creates 8-12 minute long-form script
- `generate_reel_script(trend, creator_profile)` - Creates 30-60 second short-form script
- `score_hook(hook_text)` - Evaluates hook strength (1-10) and suggests 3 alternatives

### Layer 2: API Handlers (Phase 2)

Three Lambda functions expose the core AI through REST endpoints.

**File: backend/lambdas/content_processor.py (106 lines)**
Purpose: Extract and store creator profile
- Input: Creator content sample (blog post, transcript, video transcript)
- Process: Uses embeddings.extract_style_dna()
- Output: Style DNA, embedding, profile object
- Storage: Saves to DynamoDB CreatorProfiles table + S3 content bucket

**File: backend/lambdas/trend_analyzer.py (176 lines)**
Purpose: Match and rank trends for a creator
- Input: Creator ID, list of trends to analyze
- Process: Uses embeddings.match_trend_to_creator() for each trend
- Output: Ranked list by relevance score (highest first)
- Storage: Saves to DynamoDB Trends table with 48-hour TTL for auto-cleanup

**File: backend/lambdas/script_generator_handler.py (223 lines)**
Purpose: Generate scripts in requested format(s)
- Input: Creator ID, trend, format (youtube/reel/both), optional custom hook
- Process: Fetches creator profile, generates script(s), scores hooks
- Output: Complete script(s) with hook scores
- Storage: Saves to DynamoDB Scripts table + S3 as JSON backup
- Returns: scriptId and full content

All handlers include error handling that returns results even if database operations fail.

### Layer 3: Data Persistence (Phase 3)

**File: backend/infrastructure/dynamo_client.py (395 lines)**
DynamoDB operations with two modes:
- MOCK_MODE='true' for testing (no AWS credentials needed)
- Production mode for live deployment

Six core functions:
1. `save_creator_profile(userId, profile_data)` - Stores extracted profile
2. `get_creator_profile(userId)` - Retrieves stored profile
3. `save_scripts_by_user(userId, scripts, script_id)` - Saves generated scripts
4. `get_scripts_by_user(userId, limit)` - Fetches user's script history
5. `save_trends(userId, trends)` - Stores analyzed trends with TTL
6. `get_all_trends(userId)` - Retrieves active trends (non-expired)

**Three DynamoDB Tables:**

Table: CreatorProfiles
- Primary Key: userId (partition key)
- Fields: style_dna, embedding (1536 dims), niche, tone, audience, updated_at
- Purpose: Stores creator profiles for reuse

Table: Scripts
- Primary Key: userId (partition key), scriptId (sort key)
- Fields: format (youtube/reel/both), content, hook_score, trends, created_at
- Purpose: Script history and record-keeping

Table: Trends
- Primary Key: userId (partition key), trendId (sort key)
- Fields: trend_name, relevance_score, embedding, trending_score, ttl (48 hours)
- Purpose: Caches analyzed trends with auto-expiration

**File: backend/infrastructure/s3_client.py (247 lines)**
File storage operations matching DynamoDB modes:
- MOCK_MODE for testing
- Production for live deployment

Four core functions:
1. `upload_content(userId, contentId, content_text)` - Stores creator content samples
2. `get_content(userId, contentId)` - Retrieves content
3. `save_script(userId, scriptId, script_object)` - Stores script as JSON
4. `get_script(userId, scriptId)` - Retrieves and parses script JSON

**S3 Bucket Structure:**
```
users/
  {userId}/
    content/
      {contentId}.txt          (creator content samples)
    scripts/
      {scriptId}.json          (generated scripts as JSON)
```

Supports versioning and multiple content samples per creator.

**File: backend/infrastructure/cdk_stack.py (450+ lines)**
Infrastructure definitions:
- DynamoDB tables (on-demand pricing, TTL enabled)
- S3 bucket (versioning enabled, no public access)
- Lambda function configurations
- API Gateway (REST endpoint)
- Cognito user pool (authentication)
- IAM roles and policies
- CloudWatch logging

### Layer 4: Handler-DB Integration (Phase 3b)

Handlers now save and fetch from storage:

1. **Content Processor Flow:**
   - Extract Style DNA from uploaded content
   - Generate embedding
   - Save profile to CreatorProfiles table
   - Save content to S3
   - Return profile for immediate use

2. **Trend Analyzer Flow:**
   - Fetch creator profile from CreatorProfiles table
   - Match and rank input trends
   - Fetch existing trends from Trends table (with TTL filter)
   - Merge and deduplicate
   - Save new analyzed trends to Trends table
   - Return ranked list

3. **Script Generator Flow:**
   - Fetch creator profile from CreatorProfiles table
   - Generate requested format(s)
   - Score hooks automatically
   - Save scripts to Scripts table with format field
   - Save JSON backup to S3
   - Return scripts with scriptId

## Feature-Based Test Suite

Replaced phase-based tests with feature-based organization. Each test file covers one user-facing feature across all technical layers (Phase 1-3b).

**File: backend/tests/test_creator_profiles.py (5 tests)**
1. Extract Style DNA from creator content
2. Generate 1536-dimensional embeddings
3. Save creator profile to DynamoDB
4. Retrieve profile from DynamoDB
5. Multiple creator profiles isolated by userId

Validates: Content processing layer, embedding generation, profile storage and retrieval.

**File: backend/tests/test_trend_discovery.py (5 tests)**
1. Match trend to creator style using semantic similarity
2. Rank trends by relevance score (descending order)
3. Store trends with 48-hour TTL
4. Fetch and merge trends from DynamoDB
5. Filter active trends (exclude TTL-expired)

Validates: Trend matching, ranking, storage with auto-expiration, DB operations.

**File: backend/tests/test_script_generation.py (5 tests)**
1. Generate YouTube long-form script
2. Generate Reel short-form script
3. Generate both YouTube and Reel simultaneously
4. Save scripts to DynamoDB
5. Hook scoring variations (1-10 range)

Validates: Script generation for both formats, database storage, hook scoring accuracy.

**File: backend/tests/test_content_management.py (5 tests)**
1. Upload creator content sample to S3
2. Retrieve creator content from S3
3. Save generated script to S3 as JSON
4. Retrieve generated script from S3
5. Multiple content files per creator (isolation)

Validates: S3 operations, content/script storage, file isolation by userId.

**File: backend/tests/test_end_to_end_workflow.py (5 tests)**
1. Creator onboarding (upload content)
2. Discover relevant trends
3. Generate YouTube script
4. Generate Reel script
5. Complete workflow (both formats for multiple creators)

Validates: Full user journey from onboarding through script generation, cross-feature integration.

**Test Results:** 25/25 passing (5 tests × 5 files)
**Mode:** All tests use mocked AWS services (no credentials needed)

## User Journey

### How TrendScribe Works (From Creator Perspective)

**Step 1: Onboarding**
- Creator uploads sample content (blog post, video transcript, past content)
- System extracts Style DNA: niche, tone, audience, key phrases
- Embedding created for semantic matching

**Step 2: Trend Discovery**
- User provides list of trending topics
- System ranks by relevance to creator's niche
- Shows top matches with relevance scores

**Step 3: Script Generation**
- Creator selects a trending topic
- Chooses format: YouTube (long-form), Reel (short-form), or Both
- System generates personalized script in creator's voice
- Hook automatically scored and alternatives suggested

**Step 4: Script Management**
- Scripts saved to database for future reference
- Backed up in S3 as JSON
- Creator can view history and reuse trending ideas

## Code Organization

```
backend/
  lambdas/
    bedrock_client.py         (AWS APIs)
    embeddings.py             (AI functions)
    script_generator.py       (Script generation)
    content_processor.py      (Handler 1)
    trend_analyzer.py         (Handler 2)
    script_generator_handler.py (Handler 3)
  
  infrastructure/
    dynamo_client.py          (DynamoDB operations)
    s3_client.py              (S3 operations)
    cdk_stack.py              (Infrastructure definition)
  
  tests/
    test_creator_profiles.py       (Feature: Profile management)
    test_trend_discovery.py        (Feature: Trend ranking)
    test_script_generation.py      (Feature: Script output)
    test_content_management.py     (Feature: Storage)
    test_end_to_end_workflow.py    (Feature: Full journey)
```

## Key Implementation Details

**Embedding System:**
- Titan Embeddings V1 generates 1536-dimensional vectors
- Cosine similarity used to match trends (0 = opposite, 1 = identical)
- Anything above 0.5 considered relevant match

**Hook Scoring:**
- Automatic scoring on all generated scripts (1-10 scale)
- Evaluates: engagement, clarity, value proposition
- Suggests 3 alternatives for each hook

**Data Merging:**
- Trend analyzer merges database trends with new analyzed trends
- Profile updates merge stored profile with request data
- Database values take priority for consistency

**Error Handling:**
- Handler failures in database operations don't block script generation
- Scripts returned even if database save fails
- Errors logged but don't crash Lambda

**TTL and Auto-Cleanup:**
- Trends stored with 48-hour TTL
- DynamoDB automatically deletes expired trends
- Reduces storage costs and keeps data fresh

## Testing Strategy

**Mocking Approach:**
- All AWS services mocked using unittest.mock
- No credentials needed for testing
- MOCK_MODE environment variable controls behavior
- Tests simulate real AWS responses

**Coverage:**
- Layer 1: Core AI functions (bedrock, embeddings, generation)
- Layer 2: All three Lambda handlers
- Layer 3: DynamoDB and S3 operations
- Layer 4: Handler-to-database integration
- Integration: Multi-feature workflows

**Execution:**
Each test file runs independently and produces clear pass/fail output with details on what was validated.

## Deployment Readiness

**What's Complete:**
- All core AI functions implemented and tested
- All three Lambda handlers implemented and tested
- All database operations implemented and tested
- Infrastructure defined in CDK
- Feature-based test suite (25 tests, all passing)
- Error handling and logging
- S3 versioning and organization
- DynamoDB TTL and auto-cleanup

**What's Available for Deployment:**
- CDK stack definition for AWS infrastructure
- Lambda function code with environment-based mocking
- Database schemas and operations
- API handler code with unified endpoint
- Complete test suite for validation

**Configuration for Live:**
- Set MOCK_MODE to 'false' to use real AWS services
- Configure AWS credentials in environment
- Deploy CDK stack to AWS account
- API Gateway will provide endpoint URL
