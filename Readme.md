# 語言模型大工廠 初版 V1.0.0
這是一個使用 Python 3.10.6 開發的語言模型大工廠，可以使用各種語言模型。<br>
目前支援 : <img src="./icons/openai.png" alt="OpenAI" width="20" style="border-radius: 10px;"> ```OpenAI```
/ <img src="./icons/ollama.png" alt="OpenAI" width="20" style="border-radius: 10px;"> ```Ollama``` 可自行擴展。

## 使用方式
### 1. 下載程式碼並解壓縮。
``` bash
git clone https://github.com/Xiaomanto/LLM_Factory.git
cd LLM_Factory
```
### 2. 下載依賴套件。
2-1. 創建一個虛擬環境。
``` bash
python -m venv .venv
```
2-2. 啟動虛擬環境。
``` bash
source .venv/bin/activate
# Windows 執行 .venv/Scripts/activate
```
2-3. 安裝依賴套件。
``` bash
pip install -r requirements.txt
```
### 3. 執行程式。
``` bash
python test.py
```
程式碼可自行引用調整。