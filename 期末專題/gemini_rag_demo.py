# 1️⃣ 嵌入文件
docs = ["防禦戰策略", "攻擊戰術", "後勤補給"]
embeddings = client.models.embed_content(
    model="models/gemini-embedding-001",
    contents=docs
)

# 2️⃣ 建立索引
vectors = np.array([e.values for e in embeddings.embeddings], dtype="float32")
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

# 3️⃣ 查詢
query = "如何進行縱深防禦？"
query_embed = client.models.embed_content(
    model="models/gemini-embedding-001",
    contents=[query]
)
D, I = index.search(np.array([query_embed.embeddings[0].values], dtype="float32"), k=1)
retrieved_doc = docs[I[0][0]]

# 4️⃣ 結合生成
response = client.models.generate_content(
    model="models/gemini-1.5-flash",
    contents=[f"根據以下資料回答問題：{retrieved_doc}\n問題：{query}"]
)
print(response.text)
