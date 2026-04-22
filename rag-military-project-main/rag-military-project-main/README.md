# 戰役戰術知識檢索系統 (RAG)

## 核心文件
- 架構圖解: architecture.png
- 規格說明書: specs.md
- 架構決策紀錄: adr/
- 白皮書: whitepaper.md

## 專案簡介
本系統透過 **檢索增強生成 (RAG)** 技術，結合軍事戰術知識文件，提供高效的知識查詢與答案生成。  
主要特色：
- 使用 **BGE-M3** 模型進行向量嵌入
- 採用 **pgvector** 作為向量資料庫
- 檢索策略：**Parent-Document Retrieval + Hybrid Search**
- 使用 **Reranker 模型** 提升答案精準度

## 系統架構圖
![系統架構圖](architecture.png)

## 文件連結
- [規格說明書 (Specs)](specs.md)
- [技術白皮書 (Whitepaper)](whitepaper.md)
- [ADR 記錄](adr/)
