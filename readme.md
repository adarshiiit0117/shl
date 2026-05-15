# 🧠 SHL Assessment Recommendation System

> An AI-powered conversational backend that recommends SHL assessments based on hiring intent — not just keywords.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Sentence Transformers](https://img.shields.io/badge/SentenceTransformers-2.x-orange)](https://www.sbert.net)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview

The **SHL Assessment Recommendation System** is a production-grade conversational AI backend that acts as a **hiring assessment consultant**, not a simple search engine.

Given a recruiter's natural language input — whether a job description, a role title, or a conversational refinement — the system returns a curated list of SHL assessments with explanations, respects duration constraints, asks clarifying questions when needed, and supports multi-turn iterative refinement.

```
Recruiter: "We're hiring graduate financial analysts."
System:    Recommends Verify Numerical Reasoning + OPQ + Graduate Scenarios.

Recruiter: "Add a situational judgement test and keep it under 45 minutes."
System:    Adds SJT, filters battery by duration, re-ranks and explains.
```

This system was built to simulate the behavior of a knowledgeable SHL consultant embedded in an API.

---

## ✨ Core Features

### 1. 🗣️ Conversational Recommendation Engine

The engine understands **recruiter hiring intent** across multiple turns. It doesn't just match keywords — it interprets role context, seniority, function, and constraints to recommend the right battery of assessments.

- Understands incomplete or colloquial role descriptions
- Asks clarification questions before recommending when intent is ambiguous
- Adapts recommendations across a full hiring conversation
- Detects when a conversation has reached a natural conclusion

**Example:**

| Turn | Role | Message |
|------|------|---------|
| 1 | User | "We need to hire a new branch manager." |
| 2 | System | "Is this a senior leadership role or a first-time manager position? That helps me recommend the right personality and leadership assessments." |
| 3 | User | "Senior, 10+ years experience." |
| 4 | System | Recommends OPQ32r + MQ + Leadership Report + Verify G+ |

---

### 2. 🔍 Hybrid Retrieval Architecture

The retrieval layer combines **semantic embeddings** with **BM25 keyword search** to get the best of both worlds.

#### Why Hybrid Instead of Pure Vector Search?

| Approach | Strength | Weakness |
|----------|----------|----------|
| Pure Semantic | Captures meaning, handles paraphrases | Misses exact SHL product names |
| Pure BM25 | Precise keyword matching | No semantic generalization |
| **Hybrid (used here)** | **Handles both meaning and exact terms** | Slightly more complex fusion |

SHL assessments have highly specific product names — *Verify Numerical Reasoning*, *OPQ32r*, *Graduate Scenarios*, *DSI* — which pure semantic search can fail to retrieve precisely. BM25 anchors retrieval to exact terminology, while the semantic layer handles intent generalization.

**Libraries:**
- [`sentence-transformers`](https://www.sbert.net/) — embedding generation
- [`scikit-learn`](https://scikit-learn.org/) — cosine similarity computation
- [`rank-bm25`](https://github.com/dorianbrown/rank_bm25) — BM25 retrieval

**Score Fusion:**
```
hybrid_score = α × semantic_score + (1 - α) × bm25_score
```
Alpha is tuned to weight semantic relevance slightly higher for general hiring descriptions, with BM25 providing a precision boost for named assessments.

---

### 3. 🏗️ Heuristic Recommendation Layer

Beyond retrieval, the system includes a **rule-based orchestration layer** that maps hiring archetypes to assessment patterns derived from SHL's own sample traces.

| Hiring Context | Heuristic Rules Applied |
|---------------|------------------------|
| Leadership / Senior Management | OPQ32r + Motivation Questionnaire + Leadership Report |
| Graduate / Entry-Level | Cognitive Battery + Graduate SJT + Personality |
| Safety-Critical / Manufacturing | Dependability & Safety Instrument (DSI) |
| Technical / Engineering | Verify G+ or Verify Technical + Coding Assessment |
| Customer Service / Contact Centre | Service + Verbal + OPQ Service Report |

**Why heuristics?**

Pure retrieval can produce technically correct but *contextually thin* results. The heuristic layer ensures:
- Recommendations feel like those of a trained SHL consultant
- Assessment batteries are holistically appropriate, not just individually relevant
- Behavior matches expected SHL sample conversation traces
- Refinements behave deterministically and predictably

---

### 4. 🔄 Conversational Refinement

The system supports a full range of **iterative refinement operations** without losing prior context:

- **Add** — "Add a situational judgement test"
- **Remove** — "Remove the OPQ, we don't need personality"
- **Shorten** — "We need a shorter battery, under 30 minutes total"
- **Expand cognitive** — "Add more reasoning tests"
- **Swap** — "Replace the numerical test with a verbal one"

Refinements are applied on top of the current recommendation state, preserving conversation history and re-ranking the updated battery.

---

### 5. ❓ Clarification Logic

When a recruiter's input is underspecified, the system proactively asks targeted clarification questions rather than making poor assumptions.

**Triggers for clarification:**

| Ambiguous Input | Clarification Asked |
|-----------------|---------------------|
| "Customer service role" | "Is this a voice-based or digital channel role? Do you need language proficiency testing?" |
| "Leadership position" | "Is this a first-time manager, mid-level, or C-suite role?" |
| "We're hiring for our warehouse" | "Is safety compliance a key requirement for this role?" |
| Vague or one-word inputs | "Could you tell me more about the responsibilities or the level of the role?" |

This simulates **recruiter workflow disambiguation** — the natural back-and-forth of a real hiring conversation.

---

### 6. ⏱️ Duration Constraints

The system extracts time constraints from natural language and filters recommendations accordingly.

**Supported patterns:**
- `"under 20 minutes"`
- `"max 45 mins"`
- `"keep it under an hour"`
- `"short battery"`

Assessments are filtered and re-prioritized to fit within the specified window, with total estimated duration reported in the response.

---

### 7. 🛡️ Guardrails

The backend includes a guardrails layer that rejects out-of-scope requests before they reach the recommendation engine.

**Rejected requests include:**
- Legal or compliance advice
- General HR consulting
- Non-assessment-related queries
- Competitor product questions

**Example:**
```
User:   "Can you help me write a job description?"
System: "I'm here to help with SHL assessment recommendations. 
         For job description help, you may want to use a dedicated HR tool."
```

---

## 🏛️ Architecture

```
app/
├── agent/
│   ├── extractor.py        # NLP-based intent & entity extraction
│   ├── recommender.py      # Core recommendation orchestration
│   ├── refinement.py       # Add/remove/shorten operations
│   ├── responder.py        # Response generation & formatting
│   ├── conversation.py     # Conversational memory & turn management
│   ├── clarifier.py        # Ambiguity detection & question generation
│   ├── comparer.py         # Assessment comparison logic
│   └── guardrails.py       # Out-of-scope request filtering
├── retrieval/
│   ├── embeddings.py       # Sentence Transformer embedding pipeline
│   ├── hybrid_search.py    # BM25 + semantic fusion search
│   └── ranker.py           # Score normalization & result ranking
├── routes/
│   └── chat.py             # POST /chat endpoint
├── models/                 # Pydantic request/response schemas
├── scripts/                # Data pipeline & preprocessing utilities
├── data/                   # Processed SHL catalog (embeddings + metadata)
└── main.py                 # FastAPI app initialization
```

### Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `extractor.py` | Parses role type, seniority, duration constraints, and refinement intent from user messages |
| `recommender.py` | Combines retrieval results with heuristic rules to produce a final ranked recommendation list |
| `refinement.py` | Handles stateful add/remove/shorten operations on the current recommendation set |
| `responder.py` | Converts internal recommendation objects into structured, human-readable API responses |
| `conversation.py` | Maintains multi-turn context, detects conversation completion, reconstructs history |
| `clarifier.py` | Detects when input is underspecified and generates targeted clarification questions |
| `comparer.py` | Produces side-by-side assessment comparisons when asked |
| `guardrails.py` | Intercepts and rejects non-SHL or harmful requests early in the pipeline |
| `embeddings.py` | Loads Sentence Transformer model and generates dense vector representations |
| `hybrid_search.py` | Runs parallel BM25 and semantic search and fuses scores |
| `ranker.py` | Normalizes scores, applies diversity penalties, and returns top-k results |

---

## 🔄 Data Pipeline

The system uses a preprocessed SHL assessment catalog as its knowledge base.

```
Raw SHL Catalog (Web)
        │
        ▼
  1. Scraping & Extraction
     └─ Extract assessment names, descriptions, types, durations, URL slugs
        │
        ▼
  2. Catalog Cleaning
     └─ Normalize text, remove HTML artifacts, standardize field names
        │
        ▼
  3. Preprocessing & Chunking
     └─ Combine name + description into retrieval-ready text chunks
        Add metadata: type, duration, remote/adaptive flags
        │
        ▼
  4. Embedding Generation
     └─ Encode all chunks with Sentence Transformers (all-MiniLM-L6-v2)
        Store as NumPy arrays in data/embeddings.npy
        │
        ▼
  5. Retrieval Indexing
     └─ Build BM25 index from tokenized corpus
        Load embeddings into memory at startup
        Metadata stored in data/catalog.json
```

**Artifacts produced:**

| File | Contents |
|------|----------|
| `data/catalog.json` | Cleaned SHL assessments with metadata |
| `data/embeddings.npy` | Dense embedding matrix (N × 384) |
| `data/bm25_corpus.pkl` | Tokenized corpus for BM25 index |

---

## 🔌 API Reference

### `POST /chat`

Submit a conversation and receive assessment recommendations.

**Request:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "We are hiring graduate financial analysts."
    }
  ]
}
```

**Response:**
```json
{
  "reply": "For graduate financial analyst roles, I recommend a combination of numerical reasoning, personality, and situational judgement assessments...",
  "recommendations": [
    {
      "name": "Verify Numerical Reasoning",
      "type": "Ability & Aptitude",
      "duration_minutes": 18,
      "remote_testing": true,
      "adaptive": false,
      "url": "https://www.shl.com/solutions/products/verify-numerical-reasoning/"
    },
    {
      "name": "OPQ32r",
      "type": "Personality",
      "duration_minutes": 25,
      "remote_testing": true,
      "adaptive": false,
      "url": "https://www.shl.com/solutions/products/opq/"
    },
    {
      "name": "Graduate Scenarios",
      "type": "Situational Judgement",
      "duration_minutes": 20,
      "remote_testing": true,
      "adaptive": false,
      "url": "https://www.shl.com/solutions/products/graduate-scenarios/"
    }
  ],
  "end_of_conversation": false
}
```

---

### Multi-Turn Conversation Example

**Request (turn 2 — refinement):**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "We are hiring graduate financial analysts."
    },
    {
      "role": "assistant",
      "content": "I recommend Verify Numerical Reasoning, OPQ32r, and Graduate Scenarios..."
    },
    {
      "role": "user",
      "content": "Remove the OPQ and keep it under 40 minutes total."
    }
  ]
}
```

**Response:**
```json
{
  "reply": "Understood. I've removed the OPQ32r and filtered the battery to fit within 40 minutes. The updated recommendation includes Verify Numerical Reasoning (18 min) and Graduate Scenarios (20 min), totalling 38 minutes.",
  "recommendations": [
    {
      "name": "Verify Numerical Reasoning",
      "type": "Ability & Aptitude",
      "duration_minutes": 18,
      "remote_testing": true,
      "adaptive": false
    },
    {
      "name": "Graduate Scenarios",
      "type": "Situational Judgement",
      "duration_minutes": 20,
      "remote_testing": true,
      "adaptive": false
    }
  ],
  "end_of_conversation": false
}
```

---

### Clarification Example

**Request:**
```json
{
  "messages": [
    { "role": "user", "content": "We need assessments for a leadership position." }
  ]
}
```

**Response:**
```json
{
  "reply": "I'd be happy to help. To recommend the most relevant assessments, could you tell me more about the seniority level? For example, is this a first-time manager, a mid-level team lead, or a senior executive role?",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

### Guardrail Example

**Request:**
```json
{
  "messages": [
    { "role": "user", "content": "Can you give me legal advice on employment contracts?" }
  ]
}
```

**Response:**
```json
{
  "reply": "I can only assist with SHL assessment recommendations. For legal or employment contract advice, please consult a qualified HR or legal professional.",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

## 💬 Example Conversations

<details>
<summary><strong>🏢 Leadership Hiring</strong></summary>

**User:** We're looking to hire a new Head of Operations. Senior role, 15+ years experience expected.

**System:** For a senior leadership role like Head of Operations, I recommend a comprehensive leadership assessment battery:
- **OPQ32r** — Maps personality to leadership competencies
- **Motivation Questionnaire (MQ)** — Assesses leadership drive and motivational style
- **SHL Leadership Report** — Integrates OPQ data into a leadership-specific narrative
- **Verify G+** — Measures general cognitive ability for complex decision-making

This battery is designed to evaluate both potential and style at the senior level.

---

**User:** Can we remove the cognitive test? They have a strong track record.

**System:** Understood. I've removed Verify G+ from the battery. Your updated recommendation is OPQ32r + Motivation Questionnaire + Leadership Report — focused entirely on leadership style and motivational fit.

</details>

<details>
<summary><strong>🎓 Graduate Financial Analyst Hiring</strong></summary>

**User:** We're hiring graduate financial analysts — entry level, straight out of university.

**System:** For graduate financial analyst roles, I recommend:
- **Verify Numerical Reasoning** — Tests quantitative aptitude directly relevant to finance
- **Verify Verbal Reasoning** — Assesses written comprehension for report analysis
- **Graduate Scenarios** — SJT designed specifically for graduate-level decision-making
- **OPQ32r** — Personality profiling to assess conscientiousness and detail orientation

---

**User:** Add a cognitive reasoning test and keep everything under 60 minutes.

**System:** I've added Verify G+ for broader cognitive reasoning. The updated battery totals 58 minutes: Verify Numerical (18 min) + Verify Verbal (17 min) + Graduate Scenarios (20 min) + Verify G+ (3 min adaptive). OPQ32r has been removed to keep within your time constraint.

</details>

<details>
<summary><strong>📞 Customer Service Hiring</strong></summary>

**User:** We need assessments for customer service agents in our contact centre.

**System:** Before I recommend, could I ask — is this a voice-based role (phone/calls) or a digital channel role (email/chat)? That affects whether language and communication assessments are prioritised.

---

**User:** Voice-based, English language, handling complaints.

**System:** For voice-based customer service handling complaints, I recommend:
- **Customer Contact Scenarios** — SJT for customer-facing decision-making
- **Verify Verbal Reasoning** — Assesses reading and comprehension skills
- **OPQ32r (Service Report)** — Personality assessment with a customer service lens
- **Call Centre Simulation** — Realistic work preview for contact centre environments

</details>

<details>
<summary><strong>🏭 Safety-Critical Manufacturing Role</strong></summary>

**User:** We're recruiting for a machine operator role in a chemical plant. Safety is paramount.

**System:** For safety-critical manufacturing environments, I strongly recommend including a safety and dependability assessment:
- **Dependability & Safety Instrument (DSI)** — Specifically designed to assess attitudes toward safety compliance and reliability
- **Verify G+** — Cognitive ability for following complex safety procedures
- **OPQ32r** — Assesses conscientiousness and rule-following tendencies

The DSI is particularly important for roles where safety non-compliance has serious consequences.

</details>

<details>
<summary><strong>💻 Technical / Engineering Hiring</strong></summary>

**User:** Hiring mid-level software engineers. We need to test both technical and reasoning skills.

**System:** For software engineer hiring, I recommend a technical and cognitive battery:
- **Verify G+** — General cognitive ability, predictive of technical problem-solving
- **Verify Numerical Reasoning** — Quantitative reasoning relevant to algorithm thinking
- **SHL Coding Simulation** — Hands-on coding assessment in a realistic environment
- **OPQ32r** — Personality profile for team fit and working style

---

**User:** Great. Can you compare the coding simulation to a standard technical test?

**System:** Here's a comparison:

| Feature | Coding Simulation | Standard Technical Test |
|---------|-------------------|------------------------|
| Format | Realistic IDE environment | Multiple choice / written |
| Measures | Practical coding skill | Theoretical knowledge |
| Duration | 45–90 min | 20–40 min |
| Cheating resistance | High (process-based) | Moderate |
| Best for | Mid-senior engineers | Screening / volume hiring |

For mid-level engineers, the Coding Simulation provides stronger signal on practical ability.

</details>

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI |
| Language | Python 3.10+ |
| Embedding Model | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Similarity Computation | scikit-learn (cosine similarity) |
| Keyword Search | rank-bm25 |
| Numerical Operations | NumPy |
| ASGI Server | Uvicorn |
| Deployment | Render |

---

## 🚀 Deployment

### Local Development

```bash
# Clone the repository
git clone https://github.com/your-username/shl-recommendation-system.git
cd shl-recommendation-system

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

---

### Render Deployment

This project is configured for **one-click deployment on Render's free tier**.

| Setting | Value |
|---------|-------|
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port 10000` |
| **Python Version** | 3.10.x |

**Environment Variables:**

| Variable | Description | Required |
|----------|-------------|----------|
| `EMBEDDING_MODEL` | HuggingFace model name | No (defaults to `all-MiniLM-L6-v2`) |
| `HYBRID_ALPHA` | Weight for semantic vs BM25 fusion (0.0–1.0) | No (defaults to `0.6`) |
| `MAX_RECOMMENDATIONS` | Maximum results returned | No (defaults to `10`) |

> **Note:** On Render's free tier, the service will spin down after inactivity. First requests after a cold start may take 30–60 seconds while the embedding model loads into memory.

---

## 🔬 Design Decisions

### Why Hybrid Retrieval Instead of Pure Vector Search?

SHL's assessment catalog contains highly specific product names and terminology — *OPQ32r*, *Verify Numerical Reasoning*, *Graduate Scenarios*, *DSI* — that don't always map cleanly to semantic space.

**The problem with pure vector search on small, specialized corpora:**

1. Embeddings trained on general text may not preserve SHL-specific naming conventions in the embedding space
2. A query like "OPQ" may not return *OPQ32r* as the top result if semantic similarity is the only signal
3. With ~40 assessments, BM25 has very low recall penalty and high precision gain for exact names

Hybrid retrieval gives us:
- **BM25 precision** for named assessments, acronyms, and SHL-specific jargon
- **Semantic generalization** for role descriptions, paraphrases, and indirect hiring intents
- **Better overall retrieval quality** at low dataset scale

---

### Why Rule-Based Heuristics Were Added?

Pure retrieval systems optimize for individual document relevance. But hiring assessment recommendations require **battery-level thinking** — which combination of assessments is right for this role profile.

The heuristic layer was added because:

1. **SHL sample traces show consistent patterns** — leadership roles consistently use OPQ + MQ + Leadership Report; graduate roles consistently use cognitive + SJT + personality
2. **Retrieval alone is too localized** — it returns individually relevant assessments but may miss complementary ones
3. **Conversational realism requires determinism** — refinement operations (add/remove) must behave predictably and consistently
4. **It improves consultant-like behavior** — the system's output feels like expert judgment, not search results

The heuristics are lightweight pattern-matching rules that operate as a post-retrieval orchestration layer, not a replacement for retrieval.

---

## 🔮 Future Improvements

| Improvement | Description |
|-------------|-------------|
| **Vector Database Migration** | Replace in-memory NumPy search with Pinecone or Weaviate for scalability |
| **LLM-Based Reasoning** | Add an LLM reasoning layer for more nuanced intent interpretation |
| **Learning-to-Rank** | Train a ranking model on recruiter feedback signals |
| **Recruiter Dashboard** | Frontend interface for non-technical recruiters |
| **Evaluation Framework** | Automated metrics (NDCG, recall@k) against SHL sample traces |
| **Multilingual Support** | Extend to French, German, Spanish for global deployments |
| **Feedback Loops** | Capture recruiter accept/reject signals to improve ranking |
| **Assessment Coverage** | Expand catalog beyond current scraped subset |

---

## 📁 Project Structure

```
shl-recommendation-system/
├── app/
│   ├── agent/
│   │   ├── extractor.py
│   │   ├── recommender.py
│   │   ├── refinement.py
│   │   ├── responder.py
│   │   ├── conversation.py
│   │   ├── clarifier.py
│   │   ├── comparer.py
│   │   └── guardrails.py
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── hybrid_search.py
│   │   └── ranker.py
│   ├── routes/
│   │   └── chat.py
│   ├── models/
│   └── main.py
├── data/
│   ├── catalog.json
│   ├── embeddings.npy
│   └── bm25_corpus.pkl
├── scripts/
│   ├── scrape_catalog.py
│   ├── preprocess.py
│   └── generate_embeddings.py
├── requirements.txt
├── render.yaml
└── README.md
```

---



<div align="center">
  Built as an AI systems project demonstrating conversational retrieval, hybrid search, and consultative recommendation behavior.
</div>
