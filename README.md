# AI-Assisted Work Breakdown Structure (WBS) Generator

An intelligent tool for generating, refining, comparing, and evaluating Work Breakdown Structures using AI.

## Overview

This Streamlit application leverages OpenAI's GPT models to assist project managers and teams in creating comprehensive Work Breakdown Structures. The tool provides AI-powered WBS generation with customizable parameters for creativity and model selection.

## Features

- **AI-Powered WBS Generation**: Generate detailed work breakdown structures from project descriptions
- **Model Selection**: Choose between GPT-4.1-mini and GPT-4.1 models
- **Creativity Control**: Adjust temperature settings for more deterministic or creative outputs
- **Example Projects**: Quick-start templates for common project types
- **Comparison & Evaluation**: Compare and score different WBS variations

## Installation

```bash
pip install -r requirements.txt
```

## Setup

1. Create a `.streamlit/secrets.toml` file with your OpenAI API key:

```toml
OPENAI_API_KEY = "your-api-key-here"
```

2. Run the application:

```bash
streamlit run app.py
```

## Usage

1. Launch the application and access it via the local URL (default: http://localhost:8501)
2. Enter a project description or select from example templates
3. Choose your preferred AI model and adjust creativity settings
4. Generate and refine your WBS structure

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
- OpenAI Python SDK

## License

This project is part of a thesis prototype for advanced AI-assisted project management tools.
