# Binary Search Tree 數字落點演示

互動式 BST 插入視覺化工具。網站支援自訂整數序列、數字落下動畫、插入落點，以及前序、中序和後序走訪。

相等的數字會插入在相等節點的右側。

## 線上網站

GitHub Pages（純 HTML、CSS、JavaScript）：<https://stanley0719.github.io/binary_search_tree/>

此版本在瀏覽器中執行，不需要 Python 後端。

## GitHub Pages 設定

在 GitHub repository 的 **Settings → Pages → Build and deployment**，將 **Source** 設為 **Deploy from a branch**，選擇 `main` 分支和 `/ (root)` 資料夾後儲存。GitHub Pages 會以根目錄的 `index.html` 發布網站。

## 本機執行

### 靜態網站

直接以瀏覽器開啟根目錄的 `index.html`。

### Python／Streamlit 版本

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

Streamlit Community Cloud 版本的部署方式請參閱 [Streamlit 官方文件](https://docs.streamlit.io/deploy/streamlit-community-cloud)。
