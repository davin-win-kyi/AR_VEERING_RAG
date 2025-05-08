import json
from langchain_unstructured import UnstructuredLoader  # for local files
from langchain_community.document_loaders import UnstructuredURLLoader  # for URLs
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# 0. Your OpenAI key
api_key = "OPEN API KEY"

# 1. Load & partition

# — local C# file
cs_docs = UnstructuredLoader(
    file_path="/Users/davinwinkyi/rag_json_generation/types.cs",
    mode="elements"        # split into headings, paragraphs, code blocks, etc.
).load()

# — remote Shape docs
shape_docs = UnstructuredURLLoader(
    urls=["https://acegikmo.com/shapes/docs"],
    mode="elements"
).load()

# — remote Unity docs
unity_docs = UnstructuredURLLoader(
    urls=["https://docs.unity.com/"],
    mode="elements"
).load()

all_docs = cs_docs + shape_docs + unity_docs

# 2. Chunk semantically (paragraph‑level first, then chars)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)
chunks = splitter.split_documents(all_docs)
texts  = [c.page_content for c in chunks]

# 3. Embed (passing the key directly)
emb     = OpenAIEmbeddings(openai_api_key=api_key, model="text-embedding-ada-002")
vectors = emb.embed_documents(texts)

# 4. Serialize
out = [{"text": t, "embedding": v} for t, v in zip(texts, vectors)]
with open("docsEmbedding.json", "w") as f:
    json.dump(out, f, indent=2)



