import json
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# -------------------------
# 1. Load your JSONL file
# -------------------------
def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

data = load_jsonl("pokemon_data_smaller_text_2.jsonl")

poke_chunks = [json.dumps(i) for i in data]

# -------------------------
# 2. Split text into chunks
# -------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)

chunks = []

for entry in poke_chunks:
    split_texts = splitter.split_text(entry)
    chunks.extend(split_texts)

print(f"Total chunks created: {len(chunks)}")

# -------------------------
# 3. Create embeddings using HuggingFace
# -------------------------
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# -------------------------
# 4. Create FAISS VectorStore
# -------------------------
db = FAISS.from_texts(texts=chunks, embedding=embedding)

# -------------------------
# 5. Save Vector DB
# -------------------------
save_dir = "faiss_pokemon"
db.save_local(save_dir)
print(f"FAISS index saved to: {save_dir}")

# -------------------------
# Load saved FAISS vector DB
# -------------------------
db = FAISS.load_local("faiss_pokemon", embeddings=embedding, allow_dangerous_deserialization=True)

# Perform a similarity search
results = db.similarity_search("Who has the strongest electric attack?", k=3)

for res in results:
    print(f"Chunk: {res.page_content[:300]}...")