import os
import faiss
import numpy as np
from google import genai
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 建立 Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 文件資料庫
docs = ["防禦戰策略", "攻擊戰術", "後勤補給", "指揮協調", "情報分析"]

# 嵌入文件
embeddings = client.models.embed_content(
    model="models/gemini-embedding-001",
    contents=docs
)

# 建立索引
vectors = np.array([e.values for e in embeddings.embeddings], dtype="float32")
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

print("索引建立完成，共有文件數:", len(docs))
