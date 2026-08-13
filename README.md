# 📄 CV-Craft AI Studio

**CV-Craft AI** is a high-performance, LLM-powered ATS (Applicant Tracking System) resume auditor and optimizer. It extracts unstructured data from PDF resumes, performs deep structural auditing, quantifies achievements, and evaluates skill relevance against job roles using Groq's high-speed Llama 3.3 model.

---

## 🌟 Key Features

* 📑 **Automated PDF Parsing**: Fast and structured text extraction from multi-page PDF resumes using `pdfplumber`.
* ⚡ **Lightning-Fast LLM Inference**: Powered by `Groq` Cloud API running `llama-3.3-70b-versatile` for ultra-fast evaluation.
* 🎯 **Precision Keyword Matching**: Benchmarks ATS keywords, skills, and experience against target job profiles.
* 📊 **Structured JSON Output**: Ensures consistent, clean, and reliable data formatting for frontend UI rendering.
* 🎨 **Modern Streamlit Dashboard**: Clean, responsive, and interactive user interface.

---

## 🔄 System Architecture & Workflow

Below is the complete architectural flow showing how a resume transitions from an uploaded PDF into structured AI feedback:

```mermaid
graph TD
    A[📁 User Uploads PDF Resume] --> B[⚙️ PDF Text Extractor]
    
    subgraph Data Processing Pipeline
        B -->|pdfplumber| C[📝 Clean Raw Text]
        C --> D[🎯 Prompt Template Assembly]
        D --> E[🔒 Streamlit Secrets / API Key]
    end

    subgraph LLM Processing Engine
        E -->|Secure Payload| F[🚀 Groq API - Llama 3.3 70B]
        F -->|Forced JSON Output| G[📦 JSON Response]
    end

    subgraph UI & Reporting
        G --> H[📊 Streamlit UI Parser]
        H --> I[⭐ ATS Audit Report & Feedback]
    end