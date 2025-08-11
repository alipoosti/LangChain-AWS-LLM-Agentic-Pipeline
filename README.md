# LangChain LLM Agentic Pipeline Running on AWS

## Quick Introduction

This project implements an agentic pipeline using LangChain and AWS Bedrock to extract and summarize academic papers. The pipeline uses multiple specialized agents to extract authors, abstract, title, introduction summary, and conclusion summary from PDF academic papers, then compiles a comprehensive markdown summary.

## Installation and Setup

It is recommended to use a Python virtual environment to manage dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## AWS API Key Setup

This project uses AWS Bedrock services via the `langchain_aws` package. To authenticate, you need to set up your AWS credentials:

1. Create an AWS IAM user with appropriate permissions for Bedrock.
2. Obtain your AWS Access Key ID and Secret Access Key.
3. Set the following environment variables in your shell:

```bash
export AWS_ACCESS_KEY_ID="your_access_key_id"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
export AWS_DEFAULT_REGION="ca-central-1"
```

Replace `"your_access_key_id"` and `"your_secret_access_key"` with your actual credentials.

## File Structure

```txt
.
├── llm_agents.py
├── Main_Paper_Summary.py
├── test_paper.pdf
├── test_paper_summary.md
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/
```

## Pipeline Overview

The pipeline consists of the following agents:

- **AuthorExtractorAgent**: Extracts author names from the first page of the academic paper.
- **AbstractExtractorAgent**: Extracts the abstract section from the first page.
- **TitleExtractorAgent**: Extracts the paper title from the first page.
- **IntroExtractorAgent**: Summarizes the introduction from the first 5 pages.
- **ConclusionExtractorAgent**: Summarizes the conclusion from the last 5 pages.
- **PaperSummaryWriterAgent**: Compiles all extracted information into a comprehensive markdown summary.

A visual representation of the pipeline is available in `pipeline.jpg`.

## Example Usage

Run the pipeline on a PDF file by executing:

```bash
python Main_Paper_Summary.py
```

Make sure to replace the `pdf_file` variable in `Main_Paper_Summary.py` with the path to your PDF file.

The output summary will be saved as `test_paper_summary.md`.