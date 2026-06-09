import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

embedding = client.models.embed_content(
    model="models/gemini-embedding-001",
    contents=["防禦戰：固守陣地、縱深防禦、反擊策略。"]
)

# embeddings 是一個 list，裡面每個元素都有向量
vector = embedding.embeddings[0].values

print(len(vector))      # 向量維度
print(vector[:10])      # 前10個維度
