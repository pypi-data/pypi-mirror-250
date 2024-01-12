# PromptCache

A simple-to-use prompt caching optmized for simplicity and speed.

## Installation

```bash
pip install promptcache
```

## Quickstart

```python
from promptcache import RedisCache

>>> cache = RedisCache()
>>> cache.set("this is a prompt", "this is the completion")
>>> cache.search("this is a prompt")
{'completion': 'this is the completion', 'prompt': 'this is a prompt', 'distance': 0}

>>> cache.search("this is a prompt prompt prompt")
{'completion': 'this is the completion', 'prompt': 'this is a prompt', 'distance': 0.1254}

>>> cache.get("this is a prompt")
'this is the completion'

>>> cache.delete("this is a prompt")
>>> cache.get("this is a prompt")
None 

```

# Features
1. Simplicity, speed and scalability using [redis](https://redis.io)
2. Fast embedding base on [fastembed](https://github.com/qdrant/fastembed)
3. Insturction embedding based on [InstructorEmbedding](https://github.com/xlang-ai/instructor-embedding) 
