# oop-2025-proj-pycade/settings.py
import pygame
import os

FORCE_SHOW_TOUCH_CONTROLS = True
# -----------------------------------------------------------------------------
# 遊戲基本設定 (General Game Settings)
# -----------------------------------------------------------------------------
TITLE = "Pycade Bomber"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# -----------------------------------------------------------------------------
# 顏色定義 (Colors)
# -----------------------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
LIGHT_GREY = (192, 192, 192)
DARK_GREY = (40, 40, 40)
LIGHT_BROWN = (222, 193, 179)

# -----------------------------------------------------------------------------
# 遊戲機制設定 (Gameplay Mechanics)
# -----------------------------------------------------------------------------
# 遊戲時間與計時器
GAME_DURATION_SECONDS = 11
GAME_TIME_UP_MESSAGE_COLOR = (200, 0, 0)
TIMER_COLOR = (220, 0, 0)
TIMER_URGENT_COLOR = (255, 0, 0)
TIMER_URGENT_THRESHOLD_SECONDS = 10

# 地圖設定
TILE_SIZE = 32
DESTRUCTIBLE_WALL_CHANCE = 0.55 # 可破壞牆壁在地圖上生成的機率
CLASSIC_DESTRUCTIBLE_WALL_CHANCE = 0.55 # 經典地圖的結構更固定，可以有更高的密度

# -----------------------------------------------------------------------------
# 玩家角色設定 (Player Settings)
# -----------------------------------------------------------------------------
MAX_LIVES = 3
INITIAL_BOMBS = 1
INITIAL_BOMB_RANGE = 1

# 玩家 SpriteSheet 與動畫
PLAYER_SPRITE_FRAME_WIDTH = 32
PLAYER_SPRITE_FRAME_HEIGHT = 32
PLAYER_ANIMATION_SPEED = 0.1  # 秒/幀
PLAYER_NUM_WALK_FRAMES = 6
PLAYER_VISUAL_SCALE_FACTOR = 0.95

# 玩家碰撞與移動
PLAYER_HITBOX_WIDTH_REDUCTION = 10
PLAYER_HITBOX_HEIGHT_REDUCTION = 10
HUMAN_GRID_MOVE_ACTION_DURATION = 0.2
PLAYER_INVINCIBLE_DURATION = 1000 # 毫秒

# -----------------------------------------------------------------------------
# 炸彈與爆炸設定 (Bomb & Explosion Settings)
# -----------------------------------------------------------------------------
BOMB_TIMER = 3000  # 毫秒
EXPLOSION_DURATION = 500  # 毫秒
USE_EXPLOSION_IMAGES = True
EXPLOSION_COLOR = (255, 165, 0) # 如果 USE_EXPLOSION_IMAGES 為 False

# -----------------------------------------------------------------------------
# 道具設定 (Item Settings)
# -----------------------------------------------------------------------------
# 道具類型 (字串常數)
ITEM_TYPE_SCORE = "score"
ITEM_TYPE_LIFE = "life"
ITEM_TYPE_BOMB_CAPACITY = "bomb_capacity"
ITEM_TYPE_BOMB_RANGE = "bomb_range"

# 道具掉落權重
ITEM_DROP_WEIGHTS = {
    ITEM_TYPE_LIFE: 30,
    ITEM_TYPE_BOMB_CAPACITY: 20,
    ITEM_TYPE_BOMB_RANGE: 10,
    ITEM_TYPE_SCORE: 40
}
WALL_ITEM_DROP_CHANCE = 0.8 # 牆壁被摧毀時，是否有道具掉落的總體機率

# 道具效果值
SCORE_ITEM_VALUE = 50
GENERIC_ITEM_SCORE_VALUE = 20 # 非分數道具拾取時額外增加的分數

# -----------------------------------------------------------------------------
# AI 設定 (AI Settings)
# -----------------------------------------------------------------------------
# AI 類型選擇
AVAILABLE_AI_ARCHETYPES = {
    "道具型": "item_focused",
    "保守型": "conservative",
    "攻擊型": "aggressive",
    "標準型": "original"
}
AI_OPPONENT_ARCHETYPE = "item_focused" # 預設或在選單中選擇的 AI 原型

# AI 通用行為參數
AI_MOVE_DELAY = 200 # AI 決策間隔 (毫秒)
AI_GRID_MOVE_ACTION_DURATION = 0.2 # AI 格子移動動畫持續時間 (秒)

# AI 戰術參數 (範例，這些可能分散在各 AI 控制器或 AI_BASE 中使用)
AI_ENGAGE_MIN_DIST_TO_PLAYER_FOR_DIRECT_PATH = 2
AI_EVASION_SAFETY_CHECK_FUTURE_SECONDS = 0.3
AI_RETREAT_SPOT_OTHER_DANGER_FUTURE_SECONDS = 1.5
AI_CLOSE_QUARTERS_BOMB_CHANCE = 0.6
AI_OSCILLATION_STUCK_THRESHOLD = 3

# 特定 AI 類型參數 (例如保守型 AI)
AI_CONSERVATIVE_RETREAT_DEPTH = 8
AI_CONSERVATIVE_MIN_RETREAT_OPTIONS = 3
AI_CONSERVATIVE_EVASION_URGENCY_MULTIPLIER = 1.5

# -----------------------------------------------------------------------------
# UI 與顯示設定 (UI & Display Settings)
# -----------------------------------------------------------------------------
# 文字輸入框 (若有，例如排行榜輸入姓名)
TEXT_INPUT_FONT_SIZE = 32 # 這個設定目前在 game.py 中直接使用，可以考慮移到這裡
TEXT_INPUT_BOX_COLOR_INACTIVE = pygame.Color('lightskyblue3')
TEXT_INPUT_BOX_COLOR_ACTIVE = pygame.Color('dodgerblue2')
TEXT_INPUT_PROMPT_COLOR = BLACK
TEXT_INPUT_TEXT_COLOR = BLACK
TEXT_INPUT_MAX_LENGTH = 10
HUD_AI_OFFSET_X = 205 # HUD 中 AI 資訊相對於 P1 的水平偏移 (game.py draw_hud 中使用)
THANK_YOU_BG_COLOR = (253, 246, 227)
THANK_YOU_FONT_COLOR = (44, 62, 80) 

# -----------------------------------------------------------------------------
# 排行榜設定 (Leaderboard Settings)
# -----------------------------------------------------------------------------
LEADERBOARD_FILE = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "data"), "leaderboard.json") # 確保路徑正確
LEADERBOARD_MAX_ENTRIES = 10

# -----------------------------------------------------------------------------
# 資源路徑 (Asset Paths)
# -----------------------------------------------------------------------------
# 基本目錄路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# 各類資源子目錄
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds") 
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")   
DATA_DIR = os.path.join(ASSETS_DIR, "data")     # 用於存放 leaderboard.json 等數據檔案
SOUND_DIR = os.path.join(ASSETS_DIR, "sounds") # 確保聲音目錄正確

# 特定字體路徑
CHINESE_FONT_PATH = os.path.join(FONTS_DIR, "NotoSansTC-Regular.ttf") # 確保字體檔案在此路徑
TITLE_FONT_PATH = os.path.join(FONTS_DIR, "oldenglishtextmt.ttf") # 標題字體
SUB_TITLE_FONT_PATH = os.path.join(FONTS_DIR, "Lora-VariableItalic.ttf") # 副標題字體
PIXEL_FONT_PATH = os.path.join(FONTS_DIR, "Minecraftia-Regular.ttf") # 像素風格字體

# 音樂
MENU_MUSIC_VOLUME = 0.8
MENU_MUSIC_PATH = os.path.join(SOUNDS_DIR, "Undertale_Home.mp3") # 菜單音樂
GAME_MUSIC_PATH = os.path.join(SOUNDS_DIR, "Undertale_Battle_Against_a_True_Hero.mp3") # 遊戲音樂（死亡時）
MENU_HOVER_SOUND_PATH = os.path.join(SOUNDS_DIR, "menu_hover.mp3") # 菜單懸停音效
BOMB_TICK_PATH = os.path.join(SOUNDS_DIR, "bomb_tick.mp3") # 炸彈倒數音效
EXPLOSION_PATH = os.path.join(SOUNDS_DIR, "explosion.mp3") # 爆炸音效
BLING_PATH = os.path.join(SOUNDS_DIR, "bling.mp3") # 拾取道具音效
HURT_PATH = os.path.join(SOUNDS_DIR, "hurt.mp3") # 受傷音效
PLACE_BOMB_SOUND_PATH = os.path.join(SOUNDS_DIR, "place_bomb.mp3") # 放置炸彈音效
GAME_VICTORY_PATH = os.path.join(SOUNDS_DIR, "Undertale_Hopes_and_Dreams.mp3") # 遊戲勝利音效
GAME_OVER_PATH = os.path.join(SOUNDS_DIR, "Undertale_An_Ending.mp3") # 遊戲結束音效
THANKS_YOU_PATH = os.path.join(SOUNDS_DIR, "Undertale_His_Themes.mp3") # 感謝畫面音樂

# 特定圖片路徑
# 地圖背景
VICTORY_BACKGROUND_IMG = os.path.join(IMAGES_DIR, "background", "victory_background.jpg") # 流水背景圖片
# 牆壁
WALL_SOLID_IMG = os.path.join(IMAGES_DIR, "walls", "wall_solid_placeholder.png")
WALL_DESTRUCTIBLE_IMG = os.path.join(IMAGES_DIR, "walls", "wall_destructible_placeholder.png")
STONE_0_IMG = os.path.join(IMAGES_DIR, "walls", "stone0.png") # 石頭牆壁圖片
STONE_1_IMG = os.path.join(IMAGES_DIR, "walls", "stone1.png") # 石頭牆壁圖片
STONE_2_IMG = os.path.join(IMAGES_DIR, "walls", "stone2.png") # 石頭牆壁圖片
STONE_3_IMG = os.path.join(IMAGES_DIR, "walls", "stone3.png") # 石頭牆壁圖片
# 玩家
PLAYER_IMG = os.path.join(IMAGES_DIR, "player", "player_placeholder.png") # 備用/單幀圖片
PLAYER1_SPRITESHEET_PATH = os.path.join(IMAGES_DIR, "player", "player.png") 
PLAYER2_AI_SPRITESHEET_PATH = os.path.join(IMAGES_DIR, "player", "player2.png")
AI_RETREAT_IMG = os.path.join(IMAGES_DIR, "player", "ai_retreat.png") # AI 退後時的圖片
# 炸彈與爆炸
BOMB_IMG = os.path.join(IMAGES_DIR, "bomb", "bomb_placeholder.png")
BOMB_PLAYER_1_IMG = os.path.join(IMAGES_DIR, "bomb", "bomb_player_1.png")
BOMB_PLAYER_2_IMG = os.path.join(IMAGES_DIR, "bomb", "bomb_player_2.png")
PLAYER1_BOMB_IMAGES = [BOMB_PLAYER_1_IMG, BOMB_PLAYER_2_IMG]
BOMB_AI_PLAYER_1_IMG = os.path.join(IMAGES_DIR, "bomb", "bomb_ai_player_1.png")
BOMB_AI_PLAYER_2_IMG = os.path.join(IMAGES_DIR, "bomb", "bomb_ai_player_2.png")
AI_PLAYER_BOMB_IMAGES = [BOMB_AI_PLAYER_1_IMG, BOMB_AI_PLAYER_2_IMG]
# EXPLOSION_PARTICLE_IMG = os.path.join(IMAGES_DIR, "explosion", "explosion_particle.png")
EXPLOSION_1_IMG = os.path.join(IMAGES_DIR, "explosion", "explosion_1.png")
EXPLOSION_2_IMG = os.path.join(IMAGES_DIR, "explosion", "explosion_2.png")
EXPLOSION_3_IMG = os.path.join(IMAGES_DIR, "explosion", "explosion_3.png")
EXPLOSION_IMGS = [EXPLOSION_1_IMG, EXPLOSION_2_IMG, EXPLOSION_3_IMG]
# 道具
ITEM_SCORE_IMG = os.path.join(IMAGES_DIR, "items", "item_score_placeholder.png")
ITEM_LIFE_IMG = os.path.join(IMAGES_DIR, "items", "item_life_placeholder.png")
ITEM_BOMB_CAPACITY_IMG = os.path.join(IMAGES_DIR, "items", "item_bomb_capacity_placeholder.png")
ITEM_BOMB_RANGE_IMG = os.path.join(IMAGES_DIR, "items", "item_bomb_range_placeholder.png")

# Menu 圖片
MENU_BACKGROUND_IMG = os.path.join(IMAGES_DIR, "menu", "background.jpg")
MENU_AI_LIGHT_BUTTON_IMG = os.path.join(IMAGES_DIR, "menu", "ai_light_button.png")
MENU_AI_LIGHT_BUTTON_HOVER_IMG = os.path.join(IMAGES_DIR, "menu", "ai_light_button_hover.png")
MENU_AI_BLUE_BUTTON_IMG = os.path.join(IMAGES_DIR, "menu", "ai_blue_button.png")
MENU_AI_BLUE_BUTTON_HOVER_IMG = os.path.join(IMAGES_DIR, "menu", "ai_blue_button_hover.png")
MENU_RETURN_BUTTON_IMG = os.path.join(IMAGES_DIR, "menu", "return_button.png")
MENU_RETURN_BUTTON_HOVER_IMG = os.path.join(IMAGES_DIR, "menu", "return_button_hover.png")
MENU_CONTINUE_BUTTON_IMG = os.path.join(IMAGES_DIR, "menu", "continue_button.png")
MENU_CONTINUE_BUTTON_HOVER_IMG = os.path.join(IMAGES_DIR, "menu", "continue_button_hover.png")

# 玩家 SpriteSheet 動畫影格對應 (範例)
PLAYER_SPRITESHEET_ROW_MAP = {
    "DOWN": 3,
    "RIGHT": 4,
    "UP": 5,
    # "LEFT" will be derived by flipping "RIGHT" in Player class
}

# -----------------------------------------------------------------------------
# 備註與待辦 (Notes & TODOs - 僅為範例，您可以移除或修改)
# -----------------------------------------------------------------------------
# TODO: 確認所有 placeholder 圖片路徑已替換為最終資源
# TODO: 考慮將更多硬編碼在遊戲邏輯中的數值移到 settings.py (例如地圖預設大小 grid_width, grid_height)
# GRID_WIDTH = 15 # 預設地圖寬度（格子數）
# GRID_HEIGHT = 11 # 預設地圖高度（格子數）

# --- Game Over Screen ---
GAME_OVER_BACKGROUND_IMG = os.path.join(IMAGES_DIR, "game_over", "game_over_background.jpg")