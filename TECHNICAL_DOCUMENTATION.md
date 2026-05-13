# Technical Documentation: Professional Project Planning Intelligence

**Project Version:** 1.0  
**Last Updated:** May 13, 2026  
**Authors:** Daniel Samuel, Sam Abiodun  
**Thesis Prototype:** Advanced AI-Assisted Project Management and Planning Tools

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [AI Model Integration](#ai-model-integration)
4. [API Access Details](#api-access-details)
5. [Configuration](#configuration)
6. [Code Structure](#code-structure)
7. [Deployment](#deployment)
8. [API Request/Response Format](#api-requestresponse-format)
9. [Error Handling](#error-handling)
10. [Security Considerations](#security-considerations)

---

## Project Overview

**Professional Project Planning Intelligence** is a Streamlit-based web application that leverages Anthropic's Claude AI models to generate comprehensive Work Breakdown Structures (WBS) from project descriptions. The application serves as an elite AI consultant for professional project planning, transforming high-level project ideas into detailed, actionable execution plans.

### Key Features

- AI-powered WBS generation using Claude 4 models
- Multiple model selection (Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6)
- Extended thinking capabilities with adaptive reasoning
- WBS improvement and alternative generation
- Visual project metrics and scoring
- Non-programmer friendly interface with expandable sections
- JSON-based structured output

---

## Architecture

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend Framework | Streamlit | Latest |
| AI Provider | Anthropic | Latest |
| Python SDK | anthropic | 0.92.0+ |
| Environment Management | python-dotenv | Latest |
| Language | Python | 3.11+ |

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Browser                         │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/HTTPS
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Streamlit Application (app.py)             │
│  ┌──────────────────────────────────────────────────┐  │
│  │  - UI Components (Sidebar, Text Areas, Buttons)  │  │
│  │  - Session State Management                      │  │
│  │  - JSON Parsing & Display                         │  │
│  │  - Metrics Calculation                            │  │
│  └──────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │ API Calls
                       ▼
┌─────────────────────────────────────────────────────────┐
│         Anthropic API (messages.create)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  - Model: claude-opus-4-7 / claude-opus-4-6      │  │
│  │  - Extended Thinking: adaptive                   │  │
│  │  - Output Config: high effort                    │  │
│  │  - Max Tokens: 20000                             │  │
│  │  - Temperature: 1.0 (required for thinking)      │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## AI Model Integration

### Supported Claude Models

The application supports the following Claude 4 models:

| Model ID | Model Name | Capability | Status |
|----------|------------|------------|--------|
| `claude-opus-4-7` | Claude Opus 4.7 | Highest capability, extended thinking | Primary |
| `claude-opus-4-6` | Claude Opus 4.6 | High capability, extended thinking | Available |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 | Balanced capability, extended thinking | Available |

### Model Configuration

**Exact Model Name:** `claude-opus-4-7` (default/primary)  
**Alternative Models:** `claude-opus-4-6`, `claude-sonnet-4-6`

### Extended Thinking Configuration

```python
thinking={"type": "adaptive"}
output_config={"effort": "high"}
```

**Important Constraint:** When extended thinking is enabled, `temperature` must be set to `1.0` (as per Anthropic API documentation).

---

## API Access Details

### Access Method

**Question: Was it accessed by API?**  
**Answer: YES** - The application accesses Claude models exclusively through the Anthropic Python SDK API.

**Question: Was it accessed by public-facing interface?**  
**Answer: NO** - The application does NOT use any public-facing web interface (like Claude.ai). All access is programmatic via the official Anthropic API.

### API Client Initialization

```python
from anthropic import Anthropic

# API key retrieval priority:
# 1. Streamlit secrets (.streamlit/secrets.toml)
# 2. Environment variable (ANTHROPIC_API_KEY)
# 3. .env file (via python-dotenv)

api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)
```

### API Request Structure

**Endpoint:** `client.messages.create()`  
**Method:** POST (via SDK)  
**Authentication:** Bearer token (API key)

### API Request Parameters

```python
response = client.messages.create(
    model="claude-opus-4-7",  # Exact model name
    max_tokens=20000,
    messages=[{"role": "user", "content": prompt}],
    temperature=1.0,  # Required when thinking is enabled
    thinking={"type": "adaptive"},
    output_config={"effort": "high"}
)
```

### API Response Structure

```python
response.content[0].text  # Contains the JSON WBS output
```

---

## API Request/Response Log

### Sample API Request (Generate WBS)

**Request ID:** Generated by Anthropic API (e.g., `req_011CamRzDTuwf9uk5y8XPM5P`)  
**Timestamp:** Dynamic (at time of request)  
**Model:** `claude-opus-4-7`  
**Endpoint:** `https://api.anthropic.com/v1/messages`

**Request Headers:**
```
x-api-key: [REDACTED - Stored in secrets.toml or environment variable]
anthropic-version: 2023-06-01
content-type: application/json
```

**Request Body:**
```json
{
  "model": "claude-opus-4-7",
  "max_tokens": 20000,
  "messages": [
    {
      "role": "user",
      "content": "You are a senior project manager.\n\nCreate a hierarchical Work Breakdown Structure (WBS):\n- 3 levels\n- Deliverable-oriented\n- JSON format ONLY\n- Do not include any explanation or markdown, just the JSON\n\nProject:\n[Project Description]"
    }
  ],
  "temperature": 1.0,
  "thinking": {
    "type": "adaptive"
  },
  "output_config": {
    "effort": "high"
  }
}
```

**Response Body:**
```json
{
  "id": "msg_[ID]",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "{\"project\": \"Project Name\", \"phases\": [...]}"
    }
  ],
  "model": "claude-opus-4-7",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 123,
    "output_tokens": 4567
  }
}
```

### Model Name Verification

**Proof of Model Name in API Call:**

The exact model name is explicitly passed in the API request at line 71 of `app.py`:

```python
response = client.messages.create(
    model=model,  # This variable contains "claude-opus-4-7" by default
    ...
)
```

The `model` variable is set via user selection from the sidebar (line 18-23):

```python
model = st.sidebar.selectbox("Model", [
    "claude-opus-4-7",      # Default/Primary
    "claude-opus-4-6", 
    "claude-sonnet-4-6"
])
```

**API Response Confirmation:**
The API response includes the model field confirming the exact model used:
```json
{
  "model": "claude-opus-4-7",
  ...
}
```

---

## Configuration

### Environment Variables

| Variable | Purpose | Source | Priority |
|----------|---------|--------|----------|
| `ANTHROPIC_API_KEY` | Anthropic API authentication | secrets.toml / .env / environment | secrets.toml > .env > environment |

### Configuration Files

#### `.streamlit/secrets.toml`
```toml
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
```

#### `.env`
```env
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

#### `requirements.txt`
```
streamlit
anthropic
python-dotenv
```

---

## Code Structure

### File Organization

```
project-wbs-tool/
├── app.py                          # Main Streamlit application (302 lines)
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── secrets.toml               # API keys (gitignored)
├── .env                           # Environment variables (gitignored)
├── .gitignore                     # Git ignore rules
├── README.md                      # User documentation
└── TECHNICAL_DOCUMENTATION.md     # This file
```

### Key Code Sections

#### 1. Imports and Client Setup (Lines 1-12)
```python
import streamlit as st
import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic, RateLimitError, AuthenticationError, BadRequestError, NotFoundError

load_dotenv()
api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)
```

#### 2. Model Selection (Lines 18-23)
```python
model = st.sidebar.selectbox("Model", [
    "claude-opus-4-7",
    "claude-opus-4-6", 
    "claude-sonnet-4-6"
])
```

#### 3. API Call with Extended Thinking (Lines 70-77)
```python
response = client.messages.create(
    model=model,
    max_tokens=20000,
    messages=[{"role": "user", "content": prompt}],
    temperature=1.0,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"}
)
```

#### 4. Error Handling (Lines 79-89)
```python
except RateLimitError:
    st.error("⚠️ Claude API rate limit exceeded. Please try again later.")
except AuthenticationError:
    st.error("⚠️ Invalid API key. Please check your `.streamlit/secrets.toml` file.")
except BadRequestError as e:
    if "credit balance is too low" in str(e):
        st.error("⚠️ Anthropic credit balance too low. Please go to https://console.anthropic.com/plans to upgrade or purchase credits.")
    else:
        st.error(f"⚠️ API Error: {e}")
except NotFoundError:
    st.error("⚠️ Model not found. Please select a different model from the sidebar.")
```

---

## Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (choose one method)
# Method 1: Create .streamlit/secrets.toml
# Method 2: Set environment variable
export ANTHROPIC_API_KEY="your-key"

# Run application
streamlit run app.py
```

### Access URLs

- **Local:** http://localhost:8501
- **Network:** http://[IP]:8501

---

## Error Handling

### API Error Types

| Error Type | Cause | User Message |
|------------|-------|--------------|
| `RateLimitError` | API rate limit exceeded | "⚠️ Claude API rate limit exceeded. Please try again later." |
| `AuthenticationError` | Invalid API key | "⚠️ Invalid API key. Please check your `.streamlit/secrets.toml` file." |
| `BadRequestError` (credit) | Low credit balance | "⚠️ Anthropic credit balance too low. Please go to https://console.anthropic.com/plans to upgrade or purchase credits." |
| `BadRequestError` (other) | Invalid request parameters | "⚠️ API Error: {error_message}" |
| `NotFoundError` | Model not found | "⚠️ Model not found. Please select a different model from the sidebar." |
| `JSONDecodeError` | Invalid JSON response | "❌ Invalid JSON: {error}" |

---

## Security Considerations

### API Key Management

1. **Never commit API keys** to version control
2. **.streamlit/secrets.toml** is listed in `.gitignore`
3. **.env** file is listed in `.gitignore`
4. API keys are loaded with priority: secrets.toml > .env > environment variables

### Data Privacy

- Project descriptions are sent to Anthropic API for processing
- No persistent storage of user data
- Session state is cleared on browser refresh
- Anthropic's data retention policies apply

### Access Control

- Application runs locally by default
- No built-in authentication (can be added for production deployment)
- API key is required for functionality

---

## Frequently Asked Questions (for Researchers)

### Q1: What exact Claude model was used?

**A:** The application uses `claude-opus-4-7` as the primary/default model. Alternative models supported are `claude-opus-4-6` and `claude-sonnet-4-6`. The exact model name is explicitly passed in the API request at line 71 of `app.py`.

### Q2: Was the model accessed via API?

**A:** YES. The model is accessed exclusively through the Anthropic Python SDK (`anthropic` package version 0.92.0+). No public-facing web interface (like Claude.ai) is used.

### Q3: Was the model accessed via a public-facing interface?

**A:** NO. All access is programmatic via the official Anthropic API. The application does not use any browser-based or public web interface for model access.

### Q4: How can I verify the model name in the API call?

**A:** The model name is verified in two ways:
1. **Source Code:** Line 71 of `app.py` shows `model=model` where `model` is set from the sidebar selection (lines 18-23)
2. **API Response:** The Anthropic API response includes a `model` field confirming the exact model used

### Q5: What is the exact API endpoint used?

**A:** The application uses the Anthropic Messages API via the Python SDK, which internally calls `https://api.anthropic.com/v1/messages`.

### Q6: What are the exact API parameters used?

**A:** 
- `model`: "claude-opus-4-7" (or selected alternative)
- `max_tokens`: 20000
- `messages`: Array with user role and content
- `temperature`: 1.0 (required when thinking is enabled)
- `thinking`: {"type": "adaptive"}
- `output_config`: {"effort": "high"}

### Q7: Is extended thinking enabled?

**A:** YES. Extended thinking is enabled with `thinking={"type": "adaptive"}` and `output_config={"effort": "high"}` parameters.

---

## Appendix: API Log Template

### Request Log Format

```
[timestamp] API Request
  - Request ID: req_[ID]
  - Model: claude-opus-4-7
  - Endpoint: https://api.anthropic.com/v1/messages
  - Method: POST
  - Parameters:
    - max_tokens: 20000
    - temperature: 1.0
    - thinking: {"type": "adaptive"}
    - output_config: {"effort": "high"}
  - Input Tokens: [count]
  - Output Tokens: [count]
```

### Response Log Format

```
[timestamp] API Response
  - Request ID: req_[ID]
  - Model: claude-opus-4-7
  - Status: 200 OK
  - Content-Type: application/json
  - Response Size: [bytes]
```

---

## Contact Information

**Authors:** Daniel Samuel, Sam Abiodun  
**Project Type:** Thesis Prototype  
**Institution:** [To be filled]  
**Date:** May 13, 2026

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | May 13, 2026 | Initial technical documentation |
