import os, json
from langchain.document_loaders import WebBaseLoader, SitemapLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"

# 1. Load docs from all three sources
# — your existing web sources:
shapes = WebBaseLoader("https://acegikmo.com/shapes/docs").load()
unity  = SitemapLoader("https://docs.unity.com/sitemap.xml").load()

# — **new**: load your local types.cs
#    if it's a single file:
cs_docs = TextLoader("/Users/davinwinkyi/rag_json_generation/types.cs", encoding="utf-8").load()

#    or, if you have a folder full of .cs files:
# from langchain.document_loaders import DirectoryLoader
# cs_docs = DirectoryLoader("/path/to/cs_folder", glob="*.cs", loader_cls=TextLoader).load()

all_docs = cs_docs + shapes + unity

# 2. Chunk
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks   = splitter.split_documents(all_docs)
texts    = [c.page_content for c in chunks]

# 3. Embed
emb = OpenAIEmbeddings(model="text-embedding-ada-002")
vectors = emb.embed_documents(texts)

# 4. Dump to JSON
out = [{"text": t, "embedding": v} for t, v in zip(texts, vectors)]
with open("/Users/davinwinkyi/rag_json_generation/docsEmbedding.json","w") as f:
    json.dump(out, f, indent=2)

