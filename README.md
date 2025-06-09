# 🚀 Pycade Bomber (瘋狂炸彈人 Pygame 複刻版)

![遊戲截圖](https://github.com/user-attachments/assets/10f3a9b8-f6e1-4fa7-b980-8f0a47edc155)
![遊戲截圖2](https://github.com/user-attachments/assets/22ae902f-b236-4ef4-b3ba-3c1081ca4808)

[![🚀 Build and Deploy](https://github.com/peienwu1216/oop-2025-proj-pycade/actions/workflows/deploy-to-web.yml/badge.svg)](https://github.com/peienwu1216/oop-2025-proj-pycade/actions/workflows/deploy-to-web.yml)
[![🧪 Run Pygame Tests](https://github.com/peienwu1216/oop-2025-proj-pycade/actions/workflows/run-tests.yml/badge.svg)](https://github.com/peienwu1216/oop-2025-proj-pycade/actions/workflows/run-tests.yml)

本專案是物件導向程式設計 (OOP) 課程的期末成果，旨在使用 Python 與 Pygame 函式庫，複刻經典遊戲《瘋狂炸彈人》。我們不僅重現了核心的遊戲玩法，更將重點放在實踐優雅的軟體架構、智慧的 AI 設計，以及導入業界標準的開發流程。

---

## 🎮 線上試玩 (Live Demo)

您可以直接透過以下連結，在瀏覽器中體驗最新版本的遊戲，無需任何安裝！

**[➡️ 點擊這裡開始遊戲！](https://peienwu1216.github.io/oop-2025-proj-pycade/)**

---

## ✨ 專案亮點與實踐 (Key Features & Practices)

為了讓這個專案不只是一個遊戲，我們投入了大量努力來實踐現代軟體工程方法，這也是本專案最核心的價值所在：

* **優雅的物件導向架構 (Elegant Architecture):**
    * 透過**繼承** (`GameObject` 作為基底)、**封裝** (`Manager` 類別) 與**策略模式** (`AIController`)，我們建立了清晰、可維護且易於擴充的程式碼基礎。

* **智慧的 AI 決策系統 (Intelligent AI):**
    * AI 對手並非隨機移動，而是結合了**有限狀態機 (FSM)** 來判斷當前局勢（追擊、逃跑、拾取道具），並使用 **A\* 演算法**與**曼哈頓距離**來規劃出在複雜地圖中的最佳移動路徑。

* **專業的開發與協作流程 (Professional Workflow):**
    * 我們以 **GitHub Flow** 作為協作模型，利用 **Issue** 進行任務追蹤，並在 **Pull Request** 中進行嚴謹的 **Code Review**，確保了程式碼品質與團隊溝通效率。

* **完整的 CI/CD 自動化 (Automated CI/CD):**
    * 透過 **GitHub Actions**，我們建立了完整的自動化管線。當 Pull Request 被建立時，系統會自動執行 `flake8` 風格檢查與 `pytest` 單元測試。當程式碼成功合併到 `main` 分支後，會自動將遊戲打包並部署到 GitHub Pages 網頁上。

* **經典遊戲功能複刻 (Classic Gameplay):**
    * 實現了包含多種 AI（攻擊型、保守型、道具優先型）、隨機地圖生成、道具系統與持久化本地排行榜等核心玩法。

---

## 📂 專案架構 (Project Structure)

```
.
├── .github/
│   └── workflows/
│       ├── deploy-to-web.yml    # CI/CD: 自動部署遊戲到網頁
│       └── run-tests.yml        # CI/CD: 自動執行測試與程式碼風格檢查
├── assets/
│   └── data/
│       └── leaderboard.json     # 數據：儲存排行榜資料
├── core/                        # 核心邏輯與系統
│   ├── ai_aggressive.py         # AI策略：攻擊型
│   ├── ai_controller.py         # AI控制器
│   └── ...
├── sprites/                     # 遊戲中的所有物件 (Sprite)
│   ├── player.py                # 物件：玩家
│   ├── bomb.py                  # 物件：炸彈
│   └── ...
├── test/                        # 自動化單元測試
│   ├── conftest.py              # Pytest 設定檔
│   ├── test_player.py
│   └── ...
├── .gitignore
├── README.md                    # 專案說明文件
├── game.py                      # 遊戲主迴圈與場景管理器
├── main.py                      # 程式主進入點
└── requirements.txt             # Python 相依套件清單
```

---

## 🛠️ 安裝與執行 (Getting Started)

如果您想在自己的電腦上執行這個專案，請依照以下步驟操作。

### 必要條件

* Python 3.11 (為確保與部署環境一致，建議使用此版本)
* Git

### 安裝步驟

1.  **Clone 專案庫**
    ```bash
    git clone [https://github.com/peienwu1216/oop-2025-proj-pycade.git](https://github.com/peienwu1216/oop-2025-proj-pycade.git)
    cd oop-2025-proj-pycade
    ```

2.  **建立並啟用虛擬環境 (強烈建議)**
    * 在 Windows 上:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * 在 macOS / Linux 上:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **安裝相依套件**
    ```bash
    pip install -r requirements.txt
    ```

4.  **執行遊戲！**
    ```bash
    python main.py
    ```
---

## 🕹️ 如何遊玩 (How to Play)

* **移動:** `方向鍵` (↑ ↓ ← →) 或 `W`, `A`, `S`, `D` 鍵。
* **放置炸彈:** `F` 鍵。
* **退出/返回:** `ESC` 鍵。
* **重新開始:** 在遊戲結束畫面按下 `R` 鍵。

---

## 🧪 如何測試 (Testing)

本專案使用 `pytest` 進行單元測試。若要執行測試，請在專案根目錄下執行：

```bash
pytest
```

---

## 💻 使用的技術 (Tech Stack)

* **主要語言:** Python 3.11
* **遊戲引擎:** Pygame
* **測試框架:** Pytest, Pytest-mock
* **程式碼檢查:** Flake8
* **CI/CD:** GitHub Actions
* **網頁打包:** Pygbag

---

## 📄 授權條款 (License)

本專案採用 [MIT License](LICENSE) 授權。
