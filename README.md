# Professional Project Planning Intelligence

An elite AI Consultant that transforms your project ideas into comprehensive actionable execution plans in seconds.

## Overview

This Streamlit application leverages Anthropic's Claude models to serve as an elite AI consultant for professional project planning. It transforms high-level project ideas into detailed, actionable execution plans including Work Breakdown Structures (WBS), task hierarchies, and project scoping.

## Features

- **AI-Powered Project Planning**: Transform project ideas into comprehensive execution plans with detailed WBS
- **Model Selection**: Choose between Claude 3 Haiku, Sonnet, and Opus models
- **Creativity Control**: Adjust temperature settings for more deterministic or creative outputs
- **Example Projects**: Quick-start templates for common project types
- **Comparison & Evaluation**: Compare and score different WBS variations

## Installation

```bash
pip install -r requirements.txt
```

## Setup

1. Set your Anthropic API key using either method:

   **Option A:** Create a `.streamlit/secrets.toml` file:
   ```toml
   ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
   ```

   **Option B:** Set an environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your-anthropic-api-key-here"
   ```

2. Run the application:

```bash
streamlit run app.py
```

## Usage

1. Launch the application and access it via the local URL (default: http://localhost:8501)
2. Enter a project description or select from example templates
3. Choose your preferred AI model and adjust creativity settings
4. Generate and refine your complete project execution plan

## Authors

- **Daniel Samuel**
- **Sam Abiodun**

## Project Structure

```
project-wbs-tool/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .streamlit/         # Streamlit configuration
│   └── secrets.toml    # API keys (not tracked in git)
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## Requirements

- Python 3.11+
- Streamlit
- Anthropic Python SDK

## License

This project is part of a thesis prototype for advanced AI-assisted project management and planning tools.
