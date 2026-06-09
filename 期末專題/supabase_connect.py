import os
from supabase import create_client, Client
from dotenv import load_dotenv

# 載入 .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def query_tactic(name):
    data = supabase.table("tactics").select("*").eq("name", name).execute()
    if data.data:
        return data.data[0]["description"]
    else:
        return "查無此戰術。"
