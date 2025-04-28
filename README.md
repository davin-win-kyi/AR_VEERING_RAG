# RAG Embeddings Generator

A simple pipeline to generate text embeddings from web documentation and local C# source, producing a JSON file suitable for Retrieval‑Augmented Generation (RAG).

## Overview

1. **Load** documents from:
   - A web‑hosted shapes API (`WebBaseLoader`)  
   - Unity documentation sitemap (`SitemapLoader`)  
   - Your local C# definitions (`TextLoader`)  
2. **Chunk** the combined documents into overlapping snippets.  
3. **Embed** each snippet using OpenAI’s `text-embedding-ada-002`.  
4. **Dump** the results to `docsEmbedding.json` for later use in a vector store.

## Files

- `rag_json_generation.py` – Python script orchestrating steps above.  
- `types.cs` – C# classes defining your domain objects.  
- `requirements.txt` – Python dependencies.  
- `docsEmbedding.json` – Output embeddings file.

## Prerequisites

- Python 3.7 or higher  
- An [OpenAI API key][openai]  
- Internet access to fetch web documentation  

## Configuration

Set your OpenAI key (do **not** hard‑code it in the script):

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

Alternatively, modify the first line of `rag_json_generation.py` to read the key from your environment.

## Usage

```bash
python rag_json_generation.py
```

By default, this will:

1. Load docs from:
   - `https://acegikmo.com/shapes/docs`  
   - `https://docs.unity.com/sitemap.xml`  
   - `./types.cs`  
2. Split the text into 500‑token chunks with 50‑token overlap.  
3. Generate embeddings with `text-embedding-ada-002`.  
4. Write out `docsEmbedding.json`.

> **Note:** To customize paths or loaders, edit the corresponding lines in `rag_json_generation.py`.

How to load documentation:
```bash
# link documentation
shapes = WebBaseLoader("https://acegikmo.com/shapes/docs").load()

# file documentation
cs_docs = TextLoader("/Users/davinwinkyi/rag_json_generation/types.cs", encoding="utf-8").load()
```

## Output

- **`docsEmbedding.json`** – An array of objects, each with:
  ```json
  {
    "text": "<chunk of source text>",
    "embedding": [<array of floats>]
  }
  ```

## File Descriptions

### `rag_json_generation.py`  
Implements the end‑to‑end embedding workflow using LangChain loaders, splitters, and `OpenAIEmbeddings`.

### `types.cs`  
Defines domain classes for sound and script data, which are ingested as plain text for embedding.

### `requirements.txt`  
Specifies:
```
langchain
langchain-openai
langchain-text-splitters
openai
beautifulsoup4
requests
langchain-community
lxml
```

### `docsEmbedding.json`  
Sample output structure containing text/embedding pairs for RAG.

## Next Steps

- Load `docsEmbedding.json` into your preferred vector database (e.g., Faiss, Pinecone).  
- Implement a similarity search to retrieve top‑k relevant chunks at query time.  
- Build your RAG prompt by concatenating retrieved snippets with user queries before calling the language model.

---

[openai]: https://platform.openai.com/
