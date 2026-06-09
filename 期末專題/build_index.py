from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader

loader = TextLoader("tactics.txt")
docs = loader.load()

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = [model.encode(doc.page_content) for doc in docs]

db = FAISS.from_embeddings(embeddings, docs)
db.save_local("tactics_index")
