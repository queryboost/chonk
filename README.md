# chonk

**chonk** transforms your documents into an analytics-ready wide table. One row per page. One command.

## Installation

Coming soon as `chonk`. In the meantime:

```bash
pip install chonkster
```

## Quickstart

```python
from chonkster import Chonk

ck = Chonk()
df = ck.parse("my-document.pdf")
```

Supported formats: PDF, DOCX, PPTX, HTML, Markdown, and images (PNG, JPG, TIFF, BMP).
