# Basic usage

Analyse a WordPress PHP file for hooks, API usage, and quality signals.

## Install

```bash
pip install wordpress-analyser
```

## CLI

```bash
wordpress-analyser plugin.php
```

JSON output:

```bash
wordpress-analyser plugin.php --json
```

## Python

```python
from wordpress_analyser.core import analyse_file

result = analyse_file("plugin.php")
print(result.detected_type, result.action_count, result.filter_count)
```

## HTTP

Start the API, then upload a `.php` file (multipart):

```bash
wordpress-analyser serve --port 8005
curl -F file=@plugin.php http://localhost:8005/analyse
```
