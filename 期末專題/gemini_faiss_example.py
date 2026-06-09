import faiss
import numpy as np

# 假設你已經有多筆向量
vectors = np.array([embedding.embeddings[0].values], dtype="float32")

# 建立索引
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

# 查詢
query = np.array([embedding.embeddings[0].values], dtype="float32")
D, I = index.search(query, k=1)
print("最相似的索引:", I)
print("距離:", D)
