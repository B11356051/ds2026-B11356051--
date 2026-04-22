# 戰役戰術知識檢索系統白皮書
## 背景與動機
戰役戰術知識檢索需要快速、準確且可解釋的系統，以支援軍事教育、戰術研究與戰役資料分析。傳統檢索方式難以處理長篇戰術文件與專有名詞，需要結合語義理解與結構化知識的檢索增強生成架構。

## 系統設計理念
模組化設計：ETL → Embedding → Vector DB → Retrieval → Reranker

高效檢索：Hybrid Search + Parent-Document Retrieval

可解釋性：提供檢索來源透明度，避免幻覺答案

## 技術選型理由
BGE-M3：多語言支援，適合軍事文本

pgvector：Postgres 原生支援，易於維護

Hybrid Search：結合語義與關鍵字檢索，提升召回率

Reranker：提升答案排序準確度

本系統的技術選擇已在 [Specs](specs.md) 中定義，並透過 ADR 文件詳細記錄決策過程：
- 向量資料庫 → [ADR-001](adr/adr-001.md)
- Embedding 模型 → [ADR-002](adr/adr-002.md)
- 檢索策略 → [ADR-003](adr/adr-003.md)
- Reranker 模型 → [ADR-004](adr/adr-004.md)

## 使用情境
戰術案例查詢
軍事知識教育
戰役資料分析

## 資料分層策略 (Data Stratification Strategy)
L0 基礎層 (Foundation)：軍事教範、戰術教材，定義術語與本體。

L1 結構化層 (RAG Core)：兵種編制、戰術原則，切分為知識原子。

L2 文獻層 (Evidence)：戰史案例、戰役資料，補足理論脈絡。

L3 應用層 (Application)：模擬演習、戰術推演，映射真實場景。

## 智能切塊策略 (Smart Chunking Strategy)
錯誤示範：固定長度切塊，容易斷裂戰術邏輯。

最佳實踐：
最小原子 (Atomic)：單一戰術術語或兵種配置。

戰術單元 (Tactical Unit)：完整的戰術步驟或防禦方案。

案例單元 (Case)：完整戰役案例，含背景與結果。

## 檢索能力矩陣 (Retrieval Capability Matrix)
型態 A：戰術案例查詢（如「某戰役的防禦部署」）。

型態 B：術語查詢（如「什麼是縱深防禦？」）。

型態 C：比較查詢（如「游擊戰 vs 正規戰」）。

型態 D：經典佐證（如「孫子兵法對奇襲的描述」）。

## 混合檢索管線 (Hybrid Retrieval Pipeline)
查詢正規化 (Normalize)

結構化過濾 (Filter)

混合召回 (Hybrid Retrieve: Vector + FTS + Graph)

深度重排 (Rerank)

證據裝配 (Assemble)

## 兩階段推理生成 (Two-Stage Reasoning Generation)
Stage 1：候選戰術生成
僅輸出候選列表
支持 / 反證特徵
尚缺資訊

Stage 2：證據化回答生成
LLM 撰寫論述，依據 Stage 1 的硬證據
不武斷給出「必勝方案」

## 安全治理矩陣 (Safety & Governance Matrix)
必須執行：標示不確定性、提供來源引用。

絕對禁止：編造戰史、斷言戰術必勝。

## 未來改進方向
引入知識圖譜，提升戰術邏輯驗證能力

增加多模態檢索 (文字 + 圖像)，讓系統能同時處理文本與戰術圖像資料，提升查詢的多樣性與解釋力

## 理論深度
戰役戰術知識轉換為向量表徵的挑戰：
戰術語境依賴強，單靠向量相似度容易誤判
專有名詞繁多（武器代號、兵種編制、戰術術語），冷啟動問題顯著

## 創新性
解決 hallucination：透過 Reranker + 知識圖譜驗證，避免生成錯誤戰術結論

冷啟動問題：建立軍事專有名詞詞典（例如 NATO 縮寫、武器代號），確保檢索準確性

## 系統實作藍圖 (Implementation Roadmap)
Phase 1 (MVP)：建立基礎戰術知識庫 + pgvector 檢索。

Phase 2 (進階版)：加入反證邏輯、冷啟動詞典。

Phase 3 (研究級)：引入知識圖譜、多模態檢索（文字 + 圖像）。

