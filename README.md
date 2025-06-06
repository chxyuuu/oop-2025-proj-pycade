# Pycade Bomber (瘋狂炸彈人 Pygame 複刻版)

<img src="https://github.com/user-attachments/assets/d82658bc-e547-4290-b0fb-48a8f3e954ce" width="600"/>
<img src="https://github.com/user-attachments/assets/0a8d1f0f-c46b-4f9c-9136-28bbbdbd9ed5" width="600"/>

本專案是物件導向程式設計 (OOP) 課程專案，旨在使用 Pygame 函式庫複刻經典遊戲《瘋狂炸彈人》。遊戲提供多種 AI 對手供玩家挑戰，並包含排行榜系統以記錄玩家的最佳戰績。

## Github Action 狀態
[![🚀 Build and Deploy Pycade Bomber to Web](https://github.com/peienwu1216/oop-2025-proj-pycade/actions/workflows/deploy-to-web.yml/badge.svg)](https://github.com/peienwu1216/oop-2025-proj-pycade/actions/workflows/deploy-to-web.yml)
[![🧪 Run Pygame Tests](https://github.com/peienwu1216/oop-2025-proj-pycade/actions/workflows/run-tests.yml/badge.svg)](https://github.com/peienwu1216/oop-2025-proj-pycade/actions/workflows/run-tests.yml)


## 目錄

- [Pycade Bomber (瘋狂炸彈人 Pygame 複刻版)](#pycade-bomber-瘋狂炸彈人-pygame-複刻版)
  - [目錄](#目錄)
  - [目前狀態與版本資訊](#目前狀態與版本資訊)
  - [核心功能](#核心功能)
  - [環境設定與執行](#環境設定與執行)
    - [前置需求](#前置需求)
    - [安裝依賴](#安裝依賴)
    - [執行遊戲](#執行遊戲)
  - [遊戲控制](#遊戲控制)
  - [專案架構](#專案架構)
  - [後續優化與開發方向](#後續優化與開發方向)

## 目前狀態與版本資訊

* **專案版本 (建議)**：`v0.7.0-leaderboard-input` (表示已實現排行榜、玩家輸入姓名、多樣化AI及完整的遊戲流程控制)
* **Python 版本**：3.x (開發環境為 3.13.2)
* **Pygame 版本**：2.6.1

## 核心功能

* **主選單系統 (`core/menu.py`)**：
    * 允許玩家選擇對戰的 AI 類型（標準型、保守型、侵略型、智慧道具型）。
    * 提供「排行榜」按鈕，可點閱查看歷史高分記錄。
    * 提供「退出遊戲」按鈕。
* **玩家角色 (`sprites/player.py`)**：
    * 採用瞬時格子移動系統，位置由 `tile_x`, `tile_y` 格子座標表示。
    * 人類玩家可透過鍵盤控制移動（方向鍵或 WASD）。
    * 包含生命、炸彈數量、炸彈威力、分數等屬性。
    * 具備放置炸彈、拾取道具、受到傷害等行為。
* **多樣化 AI 對手 (`core/ai_*.py`)**：
    * **標準型 (`AIController`)**：基礎的 AI 行為模式。
    * **保守型 (`ConservativeAIController`)**：行為謹慎，優先自保和安全漫遊。
    * **侵略型 (`AggressiveAIController`)**：積極追擊和攻擊玩家。
    * **智慧道具型 (`ItemFocusedAIController`)**：專注於獲取道具，並在獲得優勢後轉為攻擊性。
    * 所有 AI 基於有限狀態機 (FSM) 和路徑規劃演算法 (A*/BFS) 進行決策。
* **遊戲機制**：
    * **炸彈系統 (`sprites/bomb.py`)**：炸彈定時爆炸，火焰可摧毀可破壞牆壁及傷害玩家。炸彈在玩家離開該格後變為固態障礙物。
    * **道具系統 (`sprites/item.py`)**：包含增加生命、炸彈容量、炸彈威力、分數的道具，由牆壁被炸毀時隨機掉落。
    * **地圖系統 (`core/map_manager.py`)**：隨機生成包含固定牆壁和可破壞牆壁的地圖，並設有玩家初始安全區。牆壁被摧毀時會更新地圖數據。
    * **倒數計時系統 (`game.py`)**：每局遊戲有固定時長限制。時間到時，根據剩餘生命值（優先）和分數（次要）判斷勝負。
    * **排行榜系統 (`core/leaderboard_manager.py`, `game.py`)**：
        * 當人類玩家獲勝且分數夠高時，可以輸入姓名以記錄到排行榜。
        * 排行榜數據使用 JSON 檔案 (`assets/data/leaderboard.json`) 持久化儲存。
        * 輸入姓名後，會顯示「分數已記錄」的提示，停留數秒或按任意鍵後返回主選單。
* **遊戲流程控制 (`game.py`, `main.py`)**：
    * 包含遊戲開始、進行中、遊戲結束、輸入姓名、分數提交成功等多種狀態。
    * 遊戲結束後按 `R` 鍵或在姓名輸入/提交成功後，會返回主選單，允許玩家重新選擇 AI 或查看排行榜。
* **使用者介面 (HUD)**：
    * 遊戲中，左下角並排顯示人類玩家和 AI 的詳細狀態（生命、炸彈數、威力、分數、AI 當前狀態）。
    * 右上角顯示遊戲倒數計時，最後幾秒計時器會放大並變色以示提醒。

## 環境設定與執行

### 前置需求

* Python 3.x (建議 3.8 或更高版本)
* pip (Python 套件安裝器)
* Git (用於版本控制與協作)
* **中文字體**：為了正常顯示中文介面（如選單、排行榜），建議下載並安裝思源黑體 (Noto Sans TC) 或其他支援繁體中文的字體。將字體檔案 (如 `NotoSansTC-Regular.otf` 或 `.ttf`) 放入 `assets/fonts/` 目錄，並在 `settings.py` 中配置 `CHINESE_FONT_PATH` 指向該檔案。

### 安裝依賴

1.  克隆專案：
    ```bash
    git clone <repository_url>
    cd oop-2025-proj-pycade
    ```
2.  (建議) 建立並啟用虛擬環境：
    ```bash
    python -m venv venv
    # Windows: venv\Scripts\activate
    # Linux/macOS: source venv/bin/activate
    ```
3.  安裝 Pygame：
    ```bash
    pip install -r requirements.txt
    ```

### 執行遊戲

在專案根目錄下執行：
```bash
python main.py
```

## 遊戲控制

* **人類玩家 (Player 1)**：
    * **移動**：方向鍵 (上、下、左、右) 或 W、A、S、D 鍵。
    * **放置炸彈**：F 鍵。
* **選單/遊戲通用**：
    * **ESC 鍵**：
        * 在主選單：退出遊戲。
        * 在排行榜畫面：返回主選單。
        * 在輸入姓名畫面：跳過輸入並結束當前局次（返回主選單）。
        * 在遊戲進行中/遊戲結束畫面（非輸入姓名時）：退出遊戲。
    * **Enter 鍵**：
        * 在輸入姓名畫面：提交姓名。
    * **R 鍵**：
        * 在遊戲結束畫面（非輸入姓名時）：返回主選單重新開始。
    * **滑鼠點擊**：
        * 用於選單按鈕選擇。
        * 用於激活姓名輸入框。
        * 在「分數已記錄」提示畫面，點擊任意處可繼續（返回主選單）。

## 專案架構

* **`main.py`**: 遊戲入口，管理主應用程式迴圈、選單和遊戲實例的啟動。
* **`settings.py`**: 全域設定，如螢幕尺寸、顏色、資源路徑、遊戲參數。
* **`game.py`**: `Game` 類別，負責遊戲主邏輯、狀態管理、事件處理、更新與繪製。
* **`core/` 目錄**:
    * `menu.py`: `Menu` 類別，處理主選單、AI 選擇、排行榜顯示。
    * `map_manager.py`: `MapManager` 類別，負責地圖生成與管理。
    * `leaderboard_manager.py`: `LeaderboardManager` 類別，處理排行榜數據的載入、儲存和新增。
    * `ai_controller_base.py`: `AIControllerBase` 類別，所有 AI 控制器的基類，提供通用方法如路徑規劃、危險評估等。
    * `ai_controller.py`, `ai_conservative.py`, `ai_aggressive.py`, `ai_item_focused.py`: 各種 AI 行為模式的具體實現。
* **`sprites/` 目錄**: 遊戲物件（精靈）的類別定義。
    * `game_object.py`: 所有精靈的基類。
    * `player.py`, `bomb.py`, `explosion.py`, `item.py`, `wall.py`: 各遊戲元素的具體實現。
* **`assets/` 目錄**: 存放圖片、字體等資源檔案。
    * `assets/data/leaderboard.json`: 排行榜數據儲存檔案。
* **`requirements.txt`**: Python 依賴套件列表。
* **`README.md`**: 本檔案。

## 後續優化與開發方向

* **視覺與音效**：
    * 持續優化角色動畫、爆炸效果、道具視覺。
    * 全面整合背景音樂和各種遊戲音效。
* **遊戲內容**：
    * 設計更多樣化、具有挑戰性的地圖。
    * 引入新的道具類型，增加遊戲策略性。
* **AI 增強**：
    * 進一步提升 AI 的情境感知和戰術決策能力。
    * 研究更高級的 AI 演算法，例如更優的預判、合作或欺騙行為（若有多 AI）。
* **使用者體驗**：
    * 完善暫停選單功能（目前 ESC 多為直接退出或返回主選單）。
    * 優化排行榜的顯示介面和排序邏輯，使其更美觀易讀。
    * 提供更詳細的遊戲說明和控制提示。
* **程式碼品質**：
    * 持續進行程式碼重構和優化。
    * 完善註解和文檔。
    * 考慮引入更專業的日誌系統（如 Python `logging` 模組）。
* **長期目標**：
    * 探索強化學習 AI 的可能性。
    * 為 Pygbag 網頁化部署做準備。
* 2025/05/30: add feature/setup-ci-checks
