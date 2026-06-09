import os
from dotenv import load_dotenv
from supabase import create_client

# 載入環境變數
load_dotenv()

# 建立 Supabase 連線
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 查戰役
def query_battle(name):
    response = supabase.table("battles").select("*").ilike("name", f"%{name}%").execute()
    return response.data

# 查戰術
def query_tactic(name):
    response = supabase.table("tactics").select("*").ilike("name", f"%{name}%").execute()
    return response.data

# 查戰術 → 戰役
def query_relation_by_tactic(tactic_name):
    # 先查戰術 id
    tactic = supabase.table("tactics").select("id").ilike("name", f"%{tactic_name}%").execute()
    if not tactic.data:
        return []
    tactic_id = tactic.data[0]["id"]

    # 查關聯表
    relations = supabase.table("tactic_battle_relations").select("battle_id, effectiveness, notes").eq("tactic_id", tactic_id).execute()
    if not relations.data:
        return []

    # 查戰役名稱
    results = []
    for rel in relations.data:
        battle = supabase.table("battles").select("name").eq("id", rel["battle_id"]).execute()
        if battle.data:
            results.append({
                "battle_name": battle.data[0]["name"],
                "effectiveness": rel["effectiveness"],
                "notes": rel["notes"]
            })
    return results

# 查戰役 → 戰術
def query_relation_by_battle(battle_name):
    # 先查戰役 id
    battle = supabase.table("battles").select("id").ilike("name", f"%{battle_name}%").execute()
    if not battle.data:
        return []
    battle_id = battle.data[0]["id"]

    # 查關聯表
    relations = supabase.table("tactic_battle_relations").select("tactic_id, effectiveness, notes").eq("battle_id", battle_id).execute()
    if not relations.data:
        return []

    # 查戰術名稱
    results = []
    for rel in relations.data:
        tactic = supabase.table("tactics").select("name").eq("id", rel["tactic_id"]).execute()
        if tactic.data:
            results.append({
                "tactic_name": tactic.data[0]["name"],
                "effectiveness": rel["effectiveness"],
                "notes": rel["notes"]
            })
    return results

# 舊版 query_relation（保留相容性）
def query_relation(tactic_name):
    tactic = supabase.table("tactics").select("id").ilike("name", f"%{tactic_name}%").execute()
    if not tactic.data:
        return []
    tactic_id = tactic.data[0]["id"]
    response = supabase.table("tactic_battle_relations").select("*").eq("tactic_id", tactic_id).execute()
    return response.data

# 查武器
def query_weapon(name):
    response = supabase.table("weapons").select("*").ilike("weapon_name", f"%{name}%").execute()
    return response.data

# 查軍種
def query_branch(name):
    response = supabase.table("branches").select("*").ilike("branch_name", f"%{name}%").execute()
    return response.data

# 測試用：直接執行 db.py 時印出查詢結果
if __name__ == "__main__":
    print("測試查詢戰役：", query_battle("北非戰役"))
    print("測試查詢戰術：", query_tactic("游擊戰"))
    print("測試查詢武器：", query_weapon("F-16戰鬥機"))
    print("測試查詢軍種：", query_branch("陸軍"))
    print("測試查詢戰術→戰役：", query_relation_by_tactic("游擊戰"))
    print("測試查詢戰役→戰術：", query_relation_by_battle("越南戰爭"))
    print("測試查詢舊版關聯：", query_relation("游擊戰"))
