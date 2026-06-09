def rag_query(query):
    query_embed = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=[query]
    )
    D, I = index.search(np.array([query_embed.embeddings[0].values], dtype="float32"), k=1)
    retrieved_doc = docs[I[0][0]]
    response = client.models.generate_content(
        model="models/gemini-1.5-flash",
        contents=[f"根據以下資料回答問題：{retrieved_doc}\n問題：{query}"]
    )
    return response.text
