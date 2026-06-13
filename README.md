# wordpress-analyser

WordPress theme and plugin analyser — part of the [analyser family](https://github.com/michael-borck/lens-analysers).

Analyses WordPress themes and plugins for hook/filter architecture, template hierarchy compliance, plugin API usage, `wp_enqueue` discipline, and child theme structure.

**Status:** Available on PyPI.

## Installation

```bash
pip install wordpress-analyser
```

## Usage

```bash
wordpress-analyser path/to/theme/     # human-readable summary
wordpress-analyser path/to/plugin/ --json
wordpress-analyser serve              # FastAPI server on port 8005
```

## Analyser family

| Tool | Purpose | Port |
|---|---|---|
| document-analyser | PDF, Word, text | 8000 |
| speech-analyser | Audio, video transcription | 8001 |
| video-analyser | Video quality, scenes, OCR | 8002 |
| records-analyser | CSV, Excel, JSON | 8003 |
| code-analyser | Source code, multi-language | 8004 |
| wordpress-analyser | WP themes and plugins | 8005 |
| folder-analyser | Project structure | 8006 |
| git-analyser | Git history and churn | 8007 |
