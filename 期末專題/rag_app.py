import os
import streamlit as st
import numpy as np
import faiss
from google import genai
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

# 1️⃣ 載入環境變數與初始化 Gemini client
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2️⃣ 自動檢查可用模型
available_models = [m.name for m in client.models.list()]
if "models/gemini-1.5-flash-latest" in available_models:
    GENERATE_MODEL = "models/gemini-1.5-flash-latest"
elif "models/gemini-1.5-pro-latest" in available_models:
    GENERATE_MODEL = "models/gemini-1.5-pro-latest"
else:
    GENERATE_MODEL = next((m for m in available_models if "gemini" in m), None)

# 3️⃣ 建立 Supabase 連線
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 4️⃣ 從 Supabase 查詢所有資料並建立文件庫
docs = []

# 戰役資料
battles = supabase.table("battles").select("id, name, location, date, tactic_used, result").execute().data
for b in battles:
    docs.append(
        f"戰役：{b['name']}，地點：{b['location']}，日期：{b['date']}，戰術：{b['tactic_used']}，結果：{b['result']}"
    )

# 戰術資料
tactics = supabase.table("tactics").select("id, name, description, example").execute().data
for t in tactics:
    docs.append(f"戰術：{t['name']}，描述：{t['description']}，範例：{t['example']}")

# 武器資料
weapons = supabase.table("weapons").select("weapon_name, type, country, used_in_tactic, description").execute().data
for w in weapons:
    docs.append(
        f"武器：{w['weapon_name']}，類型：{w['type']}，國家：{w['country']}，使用戰術：{w['used_in_tactic']}，描述：{w['description']}"
    )

# 軍種資料
branches = supabase.table("branches").select("branch_name, description, example_tactics").execute().data
for br in branches:
    docs.append(f"軍種：{br['branch_name']}，描述：{br['description']}，常用戰術：{br['example_tactics']}")

# 戰役與戰術關聯資料 (用 battle_id / tactic_id 查名稱)
relations = supabase.table("tactic_battle_relations").select("battle_id, tactic_id, effectiveness, notes").execute().data
for r in relations:
    battle = supabase.table("battles").select("name").eq("id", r["battle_id"]).execute().data
    battle_name = battle[0]["name"] if battle else "未知戰役"

    tactic = supabase.table("tactics").select("name").eq("id", r["tactic_id"]).execute().data
    tactic_name = tactic[0]["name"] if tactic else "未知戰術"

    docs.append(
        f"戰役：{battle_name}，使用戰術：{tactic_name}，效果：{r['effectiveness']}，備註：{r['notes']}"
    )

# 5️⃣ 使用中文專用 HuggingFace 模型做 embedding
model = SentenceTransformer("shibing624/text2vec-base-chinese")
vectors = model.encode(docs)

# 6️⃣ 建立 FAISS 索引
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors, dtype="float32"))

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# 初始化 BLIP 模型（改用公開可用的 image captioning base）
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base",
    device_map="auto",
    torch_dtype="float16"
)

def analyze_tactic_image(image_path):
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    out = blip_model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    # 🔹 轉換為 Finding IR 結構
    finding_ir = {
        "terrain": "mountain",
        "formation": "ambush",
        "unit_size": "small",
        "weather": "rainy",
        "description": description
    }

    return finding_ir

# 7️⃣ 封裝查詢函式（檢索全部資料 + 安全語氣提示 + 寫入日誌）
def rag_query(query):
    query_vector = model.encode([query])
    D, I = index.search(np.array(query_vector, dtype="float32"), k=len(docs))  # ✅ 檢索全部資料
    retrieved_docs = [docs[i] for i in I[0]]
    
    if not retrieved_docs or all(d.strip() == "" for d in retrieved_docs):
        return "根據目前的資料庫，沒有找到相關戰役、戰術或武器的記錄。請確認 Supabase 是否有相關資料。", ""

    sources = "\n".join([f"- {doc}" for doc in retrieved_docs[:5]])
    response = client.models.generate_content(
        model=GENERATE_MODEL,
        contents=[f"請根據以下資料提供輔助性回答，避免確定語氣：{sources}\n問題：{query}"]
    )

    # ✅ 寫入檢索日誌
    supabase.table("retrieval_logs").insert({
        "query": query,
        "matched_docs": retrieved_docs,
        "similarity_scores": D[0].tolist()
    }).execute()

    return response.text, sources

# 8️⃣ Streamlit 介面
st.title("戰役、戰術、武器知識檢索系統 RAG (Supabase + HuggingFace + Gemini)")
query = st.text_input("請輸入問題：")
if query:
    answer, sources = rag_query(query)
    st.write("🧠 回答：", answer)
    st.write("📚 檢索來源：")
    st.text(sources)

uploaded_image = st.file_uploader("上傳戰術影像：", type=["png", "jpg", "jpeg"])
if uploaded_image:
    st.image(uploaded_image, caption="戰術影像預覽")
    finding_ir = analyze_tactic_image(uploaded_image)
    st.json(finding_ir)
