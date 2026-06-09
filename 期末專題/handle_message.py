if text in ["防禦戰", "縱深防禦"]:
    reply_text = "防禦戰術：以縱深配置延緩敵軍推進，爭取反擊時機。"
elif text in ["攻擊戰", "奇襲"]:
    reply_text = "攻擊戰術：以速度與出其不意為主，打擊敵軍弱點。"
else:
    reply_text = "請選擇戰術類別或輸入問題，我會幫你查詢。"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    print("收到訊息：", user_text)   # ← 這會顯示使用者輸入

    result = query_branch(user_text)
    print("branch 查詢結果：", result)   # ← 這會顯示查詢結果

    if result:
    data = result[0]
    # 假設資料庫欄位是 branch_name
    reply = f"🪖 軍種名稱：{data['branch_name']}\n職責：{data['duty']}"
    line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=reply)])
    return

    result = query_relation(user_text)
    print("relation 查詢結果：", result)   # ← 這會顯示查詢結果

    if result:
        battles = [r["battle_name"] for r in result]
        reply = f"🧩 戰術「{user_text}」相關戰役：\n" + "\n".join(battles)
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=reply)])
        return

    line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="找不到資料")])
