# Binary Search Tree 數字落點演示

以 Python 和 Streamlit 製作的互動式 BST 插入視覺化工具。輸入以逗號或空格分隔的整數後，頁面會逐一播放數字從根節點落下、依大小向左或向右比較，直到插入的位置，並列出每個數字經過的節點、最終落點及深度。

相等的數字會插入在相等節點的右側。

## 本機執行

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 執行測試

```powershell
python -m unittest -v
```

## 部署至 Streamlit Community Cloud

1. 將此專案推送至 GitHub repository。
2. 登入 [Streamlit Community Cloud](https://share.streamlit.io/) 並連結 GitHub 帳號。
3. 選擇此 repository、部署分支及 `app.py` 作為主程式，即可取得公開網站網址。

Streamlit Community Cloud 會依照 `requirements.txt` 安裝執行環境。
