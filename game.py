# oop-2025-proj-pycade/game.py (REVISED FOR WEBGAME)

import pygame
import settings
from core.map_manager import MapManager
from core.touch_controls import TouchControls
from sprites.player import Player
from core.leaderboard_manager import LeaderboardManager
from core.audio_manager import AudioManager
from core.pause_scene import PauseScene

# AI 控制器匯入
from core.ai_controller import AIController as OriginalAIController
from core.ai_conservative import ConservativeAIController
from core.ai_aggressive import AggressiveAIController
from core.ai_item_focused import ItemFocusedAIController
from sprites.draw_text import DIGIT_MAP
from sprites.draw_text import draw_text_with_shadow, draw_text_with_outline



class Game:
    def __init__(self, screen, clock, audio_manager,ai_archetype="original", map_type="classic", headless=False):
        self.headless = headless 
        self.screen = screen
        self.clock = clock

        self.audio_manager = audio_manager # 儲存傳入的實例
        self.audio_manager.stop_all()
        self.audio_manager.play_music(settings.GAME_MUSIC_PATH)
        
        self.running = True # 這個 self.running 仍然有用，用來標記 Game 場景是否應該繼續
        self.dt = 0 # dt 會在 run_one_frame 中更新
        self.restart_game = False # 這個旗標用來告訴 main.py 是否要回到選單
        self.game_state = "PLAYING"
        self.paused = False # 【新增】暫停狀態旗標
        self.pause_scene = None # 【新增】用於存放暫停場景實例
        self.ai_archetype = ai_archetype
        self.map_type = map_type # 【新增】儲存地圖類型
        
        self.victory_music_played = False
        self.game_over_played = False
        self.ticking_sound_playing = False

        # --- Background ---
        self.victory_background_image = pygame.image.load(settings.VICTORY_BACKGROUND_IMG).convert()
        self.victory_background_image = pygame.transform.scale(self.victory_background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.brick_tile_image = pygame.image.load(settings.STONE_0_IMG).convert()
        self.brick_tile_image = pygame.transform.smoothscale(
            self.brick_tile_image,
            (settings.TILE_SIZE, settings.TILE_SIZE)
        )
        self.border_brick = pygame.image.load(settings.WALL_SOLID_IMG).convert()
        self.border_brick = pygame.transform.smoothscale(
            self.border_brick,
            (settings.TILE_SIZE, settings.TILE_SIZE)
        )
        self.beside_brick = pygame.image.load(settings.STONE_1_IMG).convert()
        self.beside_brick = pygame.transform.smoothscale(
            self.beside_brick,
            (settings.TILE_SIZE, settings.TILE_SIZE)
        )
        self.timer_brick = pygame.image.load(settings.STONE_2_IMG).convert()
        self.timer_brick = pygame.transform.smoothscale(
            self.timer_brick,
            (settings.TILE_SIZE, settings.TILE_SIZE)
        )
        self.text_brick = pygame.image.load(settings.STONE_3_IMG).convert()
        self.text_brick = pygame.transform.smoothscale(
            self.text_brick,
            (settings.TILE_SIZE, settings.TILE_SIZE)
        )

        # --- Sprite Groups ---
        self.all_sprites = pygame.sprite.Group()
        self.players_group = pygame.sprite.Group()
        self.bombs_group = pygame.sprite.Group()
        self.explosions_group = pygame.sprite.Group()
        self.items_group = pygame.sprite.Group()
        self.solid_obstacles_group = pygame.sprite.Group()
        self.floating_texts_group = pygame.sprite.Group()

        # --- Managers and Player/AI instances ---
        self.map_manager = MapManager(self)
        self.player1 = None
        self.player2_ai = None
        self.ai_controller_p2 = None
        self.player1_bomb_toggle = 0


        # --- Timer related attributes ---
        self.time_elapsed_seconds = 0
        self.game_timer_active = False
        self.time_up_winner = None
        self.game_over_reason = ""

        # --- Leaderboard Manager ---
        self.leaderboard_manager = LeaderboardManager()

        # --- Text Input related attributes ---
        self.player_name_input = ""
        self.input_box_active = False
        self.name_input_rect = pygame.Rect(
            settings.SCREEN_WIDTH // 2 - 140,
            settings.SCREEN_HEIGHT // 2 - 20,
            280, 40
        )
        self.score_to_submit = 0

        self.score_submitted_message_timer = 0.0
        self.score_submitted_message_duration = 3.0

        # --- HUD Icons ---
        self.hud_icon_heart = None
        self.hud_icon_bomb = None
        self.hud_icon_score = None
        self.hud_icon_pause = None # 【新增】暫停按鈕圖示
        self.pause_button_rect = None # 【新增】暫停按鈕的 Rect

        # --- 觸控控制建立邏輯 ---
        self.touch_controls = None
        if not headless:
            touch_available = False
            # 1. 首先，用 hasattr() 安全地檢查 pygame 是否有 'touch' 這個模組
            if hasattr(pygame, 'touch'):
                try:
                    # 2. 如果模組存在，再嘗試呼叫函式
                    if pygame.touch.get_num_devices() > 0:
                        touch_available = True
                except pygame.error as e:
                    # 處理極端情況：模組存在但初始化失敗
                    print(f"Pygame touch module available but failed to initialize: {e}")
            else:
                # 如果連 'touch' 模組都沒有，直接印出提示
                print("Pygame 'touch' module not found (expected on non-touch desktop builds).")

            # 3. 根據偵測結果或手動設定的旗標來決定是否建立 TouchControls
            if touch_available or getattr(settings, "FORCE_SHOW_TOUCH_CONTROLS", False):
                print("Touch controls ENABLED (Touch device detected or force flag is on).")
                self.touch_controls = TouchControls(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
            else:
                print("Touch controls DISABLED (No touch device or module unavailable).")

        # --- Font attributes ---
        self.hud_font = None
        self.game_over_font = None
        self.restart_font = None
        self.ai_status_font = None
        self.timer_font_normal = None
        self.timer_font_urgent = None
        self.text_input_font = None
        self.prompt_font = None
        self.message_font = None

        # 遊戲結束畫面的按鈕
        self.continue_button_img = None
        self.continue_button_hover_img = None
        self.game_over_button_rect = None

        try:
            # --- Load HUD Icons ---
            icon_size = (32, 32) # Define a standard size for icons
            self.hud_icon_heart = pygame.image.load('assets/images/items/item_life_placeholder.png').convert_alpha()
            self.hud_icon_heart = pygame.transform.scale(self.hud_icon_heart, icon_size)
            self.hud_icon_bomb = pygame.image.load('assets/images/items/item_bomb_capacity_placeholder.png').convert_alpha()
            self.hud_icon_bomb = pygame.transform.scale(self.hud_icon_bomb, icon_size)
            self.hud_icon_score = pygame.image.load('assets/images/items/item_score_placeholder.png').convert_alpha()
            self.hud_icon_score = pygame.transform.scale(self.hud_icon_score, icon_size)
            # 【修改】載入並設定暫停按鈕圖示
            self.hud_icon_pause = pygame.image.load('assets/images/ui/pause.png').convert_alpha()
            self.hud_icon_pause = pygame.transform.scale(self.hud_icon_pause, (36, 36))
            self.pause_button_rect = self.hud_icon_pause.get_rect(topright=(settings.SCREEN_WIDTH - 10, 10))

            font_size = 30
            # font_status_size = 18
            timer_font_size_normal = 28
            timer_font_size_urgent = 36
            text_input_font_size = getattr(settings, "TEXT_INPUT_FONT_SIZE", 32)
            prompt_font_size = 48
            message_font_size = 38

            default_font_path = None
            if hasattr(settings, 'CHINESE_FONT_PATH') and settings.CHINESE_FONT_PATH:
                try:
                    font_test = pygame.font.Font(settings.CHINESE_FONT_PATH, 10)
                    if font_test:
                        default_font_path = settings.CHINESE_FONT_PATH
                except pygame.error as e:
                    print(f"Game: 中文字體 '{settings.CHINESE_FONT_PATH}' 載入失敗 ({e})，將使用預設字體。")

            self.hud_font = pygame.font.Font(settings.PIXEL_FONT_PATH, font_size)
            self.victory_font = pygame.font.Font(settings.SUB_TITLE_FONT_PATH, font_size)
            self.ai_status_font = pygame.font.Font(settings.CHINESE_FONT_PATH, 24)
            self.timer_font_normal = pygame.font.Font(default_font_path, timer_font_size_normal)
            self.timer_font_urgent = pygame.font.Font(default_font_path, timer_font_size_urgent)
            self.text_input_font = pygame.font.Font(default_font_path, text_input_font_size)
            self.prompt_font = pygame.font.Font(settings.SUB_TITLE_FONT_PATH, prompt_font_size)
            self.message_font = pygame.font.Font(settings.SUB_TITLE_FONT_PATH, message_font_size)

            self.game_over_font = pygame.font.Font(settings.TITLE_FONT_PATH, 50)
            self.restart_font = pygame.font.Font(settings.SUB_TITLE_FONT_PATH, 25)

            # 載入遊戲結束按鈕圖片
            self.continue_button_img = pygame.image.load(settings.MENU_CONTINUE_BUTTON_IMG).convert_alpha()
            self.continue_button_hover_img = pygame.image.load(settings.MENU_CONTINUE_BUTTON_HOVER_IMG).convert_alpha()
            btn_size = (280, 74) # 統一按鈕大小
            self.continue_button_img = pygame.transform.smoothscale(self.continue_button_img, btn_size)
            self.continue_button_hover_img = pygame.transform.smoothscale(self.continue_button_hover_img, btn_size)

        except Exception as e:
            print(f"Error initializing fonts in Game: {e}")
            self.hud_font = pygame.font.SysFont("arial", 24)
            self.ai_status_font = pygame.font.SysFont("arial", 20)
            self.timer_font_normal = pygame.font.SysFont("arial", 30)
            self.timer_font_urgent = pygame.font.SysFont("arial", 38)
            self.text_input_font = pygame.font.SysFont("arial", getattr(settings, "TEXT_INPUT_FONT_SIZE", 32))
            self.prompt_font = pygame.font.SysFont("arial", 48)
            self.message_font = pygame.font.SysFont("arial", 38)
            self.game_over_font = pygame.font.SysFont('arial', 74)
            self.restart_font = pygame.font.SysFont('arial', 30)

        self.setup_initial_state()

    def start_timer(self):
        self.time_elapsed_seconds = 0
        self.game_timer_active = True
    
    def game_over(self):
        if self.game_over_played == False:
            self.audio_manager.play_music(settings.GAME_OVER_PATH)
            self.game_over_played = True
    
    def victory(self):
        if self.victory_music_played == False:
            self.audio_manager.play_music(settings.GAME_VICTORY_PATH)
            self.audio_manager.set_music_volume(0.6)
            self.victory_music_played = True
    
    def setup_initial_state(self):
        # (此函式保持不變)
        self.all_sprites.empty()
        self.players_group.empty()
        self.bombs_group.empty()
        self.explosions_group.empty()
        self.items_group.empty()
        self.solid_obstacles_group.empty()

        self.time_elapsed_seconds = 0.0
        self.game_timer_active = False
        self.time_up_winner = None
        self.game_state = "PLAYING"
        self.game_over_reason = ""
        self.ticking_sound_playing = False

        self.player_name_input = ""
        self.input_box_active = False
        self.score_to_submit = 0
        self.score_submitted_message_timer = 0.0

        grid_width = getattr(settings, 'GRID_WIDTH', 15)
        grid_height = getattr(settings, 'GRID_HEIGHT', 11)

        p1_start_tile = (1, 1)
        p2_start_tile_x = grid_width - 2 if grid_width > 2 else 1
        p2_start_tile_y = grid_height - 2 if grid_height > 2 else 1
        p2_start_tile = (p2_start_tile_x, p2_start_tile_y)
        safe_radius = 2

        # 【修改】根據 map_type 選擇地圖生成函式
        if self.map_type == "random":
            print("[Game] Generating a TRULY RANDOM map.")
            map_layout = self.map_manager.get_truly_random_map_layout(
                grid_width, grid_height, p1_start_tile, p2_start_tile, safe_radius
            )
        else: # 預設或 "classic"
            print("[Game] Generating a CLASSIC map.")
            map_layout = self.map_manager.get_classic_map_layout(
                grid_width, grid_height, p1_start_tile, p2_start_tile, safe_radius
            )

        self.map_manager.load_map_from_data(map_layout)

        player1_sprite_config = {
            "ROW_MAP": settings.PLAYER_SPRITESHEET_ROW_MAP,
            "NUM_FRAMES": settings.PLAYER_NUM_WALK_FRAMES
        }
        self.player1 = Player(self, p1_start_tile[0], p1_start_tile[1],
                              spritesheet_path=settings.PLAYER1_SPRITESHEET_PATH,
                              sprite_config=player1_sprite_config,
                              is_ai=False, is_player1=True)
        self.all_sprites.add(self.player1)
        self.players_group.add(self.player1)

        ai_image_set_path = getattr(settings, 'PLAYER2_AI_SPRITESHEET_PATH', settings.PLAYER1_SPRITESHEET_PATH)
        ai_sprite_config = {
            "ROW_MAP": settings.PLAYER_SPRITESHEET_ROW_MAP,
            "NUM_FRAMES": settings.PLAYER_NUM_WALK_FRAMES
        }
        self.player2_ai = Player(self, p2_start_tile[0], p2_start_tile[1],
                                 spritesheet_path=ai_image_set_path,
                                 sprite_config=ai_sprite_config,
                                 is_ai=True)
        self.all_sprites.add(self.player2_ai)
        self.players_group.add(self.player2_ai)

        ai_controller_class = None
        if self.ai_archetype == "original": ai_controller_class = OriginalAIController
        elif self.ai_archetype == "conservative": ai_controller_class = ConservativeAIController
        elif self.ai_archetype == "aggressive": ai_controller_class = AggressiveAIController
        elif self.ai_archetype == "item_focused": ai_controller_class = ItemFocusedAIController
        else: ai_controller_class = OriginalAIController

        self.ai_controller_p2 = ai_controller_class(self.player2_ai, self)

        if hasattr(self.ai_controller_p2, 'reset_state') and callable(getattr(self.ai_controller_p2, 'reset_state')):
            self.ai_controller_p2.reset_state()

        self.player2_ai.ai_controller = self.ai_controller_p2
        if self.ai_controller_p2:
            self.ai_controller_p2.human_player_sprite = self.player1
        
        # 【新增】重置 running 和 restart_game 旗標，確保每次 Game 場景開始時都是乾淨的狀態
        self.running = True
        self.restart_game = False

    def run_one_frame(self, events_from_main_loop, dt):
        # 如果 Game 場景已經設定為不再運行 (例如，玩家按 ESC 或遊戲結束)
        if not self.running:
            from core.menu import Menu
            # ！！！～～～
            # 根據 restart_game 旗標決定返回 Menu 還是 "QUIT" 指令
            if self.restart_game:
                self.audio_manager.stop_music()
                self.audio_manager.stop_all_sounds()
                # 建立 Menu 物件時，傳遞所有必要的參數
                return Menu(self.screen, self.audio_manager, self.clock)
            else:
                self.audio_manager.stop_music()
                self.audio_manager.stop_all_sounds()
                return "QUIT"
            # ！！！～～～

        # 使用傳入的 dt
        self.dt = dt

        # 【修改】根據暫停狀態決定更新哪個部分
        if self.paused:
            action = self.pause_scene.update(events_from_main_loop)
            if action == "CONTINUE":
                self.paused = False
                self.audio_manager.unpause_music()
                self.audio_manager.unpause_all_sfx()
            elif action == "BACK_TO_MENU":
                self.running = False
                self.restart_game = True
        else:
            self._process_events_internal(events_from_main_loop)
            self._update_internal()

        # 繪製畫面
        self._draw_internal()
        
        # 【新增】如果遊戲暫停，覆蓋繪製暫停場景
        if self.paused:
            self.pause_scene.draw()

        # 檢查場景是否應該結束
        if not self.running:
            from core.menu import Menu
            if self.restart_game:
                self.audio_manager.stop_music()
                self.audio_manager.stop_all_sounds()
                # 再次檢查，確保所有退出路徑都有處理
                return Menu(self.screen, self.audio_manager, self.clock)
            else:
                 self.audio_manager.stop_music()
                 self.audio_manager.stop_all_sounds()
                 return "QUIT"
        
        return self # 返回 self 表示繼續運行 Game 場景


    # 【修改】將原本的 events() 改名為 _process_events_internal() 並接收外部傳入的事件
    def _process_events_internal(self, events_from_main_loop):
        for event in events_from_main_loop:
            # 優先處理需要獨佔輸入的遊戲狀態
            if self.game_state == "ENTER_NAME":
                self.handle_enter_name_state_events(event)
                continue  # 處理完直接跳到下一個事件

            if self.game_state == "SCORE_SUBMITTED":
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.restart_game = True
                    self.running = False
                continue
            
            # 當遊戲結束時，處理返回按鈕的點擊
            if self.game_state == "GAME_OVER" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_over_button_rect and self.game_over_button_rect.collidepoint(event.pos):
                    self.restart_game = True
                    self.running = False
                    continue # 事件已處理

            # --- 處理觸控事件 (事件型, 如單次點擊) ---
            if self.game_state == "PLAYING" and self.touch_controls:
                action = self.touch_controls.handle_event(event)
                if action == 'BOMB' and self.player1 and self.player1.is_alive:
                    self.player1.place_bomb()

            # 【新增】處理暫停按鈕點擊
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.pause_button_rect and self.pause_button_rect.collidepoint(event.pos):
                    if self.game_state == "PLAYING" and not self.paused:
                        self.paused = True
                        self.audio_manager.pause_music()
                        self.audio_manager.pause_all_sfx()
                        self.pause_scene = PauseScene(self.screen, self.audio_manager)
                        continue # 事件已處理

            # --- 處理鍵盤事件 ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "PLAYING":
                        self.paused = not self.paused
                        if self.paused:
                            self.audio_manager.pause_music()
                            self.audio_manager.pause_all_sfx()
                            self.pause_scene = PauseScene(self.screen, self.audio_manager)
                        else:
                            self.audio_manager.unpause_music()
                            self.audio_manager.unpause_all_sfx()
                    else:
                        self.running = False
                        self.restart_game = False
                
                # 'PLAYING' 狀態下的鍵盤事件
                if self.game_state == "PLAYING":
                    if event.key == pygame.K_f:
                        if self.player1 and self.player1.is_alive:
                            self.player1.place_bomb()
                
                # 'GAME_OVER' 狀態下的鍵盤事件
                elif self.game_state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        self.restart_game = True
                        self.running = False

    def _update_internal(self):
        # 【新增】如果遊戲暫停，則不更新
        if self.paused:
            return

        if self.game_state == "PLAYING":
            # --- 新增：處理持續性的觸控移動 ---
            if self.touch_controls and self.player1 and self.player1.is_alive:
                if self.touch_controls.is_pressed('UP'):
                    self.player1.attempt_move_to_tile(0, -1)
                elif self.touch_controls.is_pressed('DOWN'):
                    self.player1.attempt_move_to_tile(0, 1)
                elif self.touch_controls.is_pressed('LEFT'):
                    self.player1.attempt_move_to_tile(-1, 0)
                elif self.touch_controls.is_pressed('RIGHT'):
                    self.player1.attempt_move_to_tile(1, 0)
            # --- 觸控移動處理結束 ---

            p1_won_by_ko = False
            p1_won_by_time = False

            if self.game_timer_active:
                self.time_elapsed_seconds += self.dt
                if self.time_elapsed_seconds >= settings.GAME_DURATION_SECONDS:
                    self.game_timer_active = False
                    if self.player1.is_alive and self.player2_ai.is_alive:
                        if self.player1.lives > self.player2_ai.lives:
                            self.time_up_winner = "P1"; p1_won_by_time = True
                            self.game_over_reason = f"You had more lives ({self.player1.lives} vs {self.player2_ai.lives})"
                        elif self.player2_ai.lives > self.player1.lives:
                            self.time_up_winner = "AI"
                            self.game_over_reason = f"AI had more lives ({self.player2_ai.lives} vs {self.player1.lives})"
                        else:
                            # 生命值相同，比較分數
                            if self.player1.score > self.player2_ai.score:
                                self.time_up_winner = "P1"; p1_won_by_time = True
                                self.game_over_reason = f"You had a higher score ({self.player1.score} vs {self.player2_ai.score})"
                            elif self.player2_ai.score > self.player1.score:
                                self.time_up_winner = "AI"
                                self.game_over_reason = f"AI had a higher score ({self.player2_ai.score} vs {self.player1.score})"
                            else: self.time_up_winner = "DRAW"; self.game_over_reason = "Time ran out with a perfect draw."
                    elif self.player1.is_alive:
                        self.time_up_winner = "P1"; p1_won_by_time = True
                        self.game_over_reason = "You were the last one standing at time's up."
                    elif self.player2_ai.is_alive: self.time_up_winner = "AI"; self.game_over_reason = "The AI was the last one standing at time's up."
                    else: self.time_up_winner = "DRAW"; self.game_over_reason = "No one was left standing when time ran out."

                    self.game_state = "GAME_OVER"
                    self.audio_manager.stop_all_sounds()
                    self.game_over() # 播放遊戲結束音樂
                    
                    

            if self.player2_ai and self.player2_ai.is_alive and self.ai_controller_p2:
                self.ai_controller_p2.update()
            self.all_sprites.update(self.dt, self.solid_obstacles_group)
            self.bombs_group.update(self.dt, self.solid_obstacles_group)
            self.floating_texts_group.update()

            # --- Centralized Bomb Tick Sound Management ---
            # If there are bombs on screen and the sound is not playing, start it.
            if len(self.bombs_group) > 0 and not self.ticking_sound_playing:
                self.audio_manager.play_sound('tick', loops=-1, volume_multiplier=0.6)
                self.ticking_sound_playing = True
            # If there are no bombs but the sound is playing, stop it.
            elif len(self.bombs_group) == 0 and self.ticking_sound_playing:
                self.audio_manager.stop_sound('tick')
                self.ticking_sound_playing = False

            for player in list(self.players_group):
                if player.is_alive:
                    if pygame.sprite.spritecollide(player, self.explosions_group, False, pygame.sprite.collide_rect):
                        player.take_damage()

            if hasattr(self.map_manager, 'destructible_walls_group'):
                for d_wall in list(self.map_manager.destructible_walls_group):
                    if d_wall.alive():
                        if pygame.sprite.spritecollide(d_wall, self.explosions_group, False):
                            d_wall.take_damage()

            for player in list(self.players_group):
                if player.is_alive:
                    items_collected = pygame.sprite.spritecollide(player, self.items_group, True, pygame.sprite.collide_rect)
                    for item in items_collected: 
                        item.apply_effect(player)
                        self.audio_manager.play_sound('bling')

            if self.game_timer_active:
                human_player_alive = self.player1 and self.player1.is_alive
                ai_player_alive = self.player2_ai and self.player2_ai.is_alive
                if not human_player_alive:
                    self.game_over()
                elif not ai_player_alive:
                    self.victory()
                if not human_player_alive or not ai_player_alive:
                    if self.game_state == "PLAYING": # 只在狀態轉換時設定一次原因
                        if not human_player_alive and not ai_player_alive:
                             self.game_over_reason = "Both combatants were eliminated simultaneously."
                        elif not ai_player_alive:
                            p1_won_by_ko = True # 確保設定勝利旗標
                            self.game_over_reason = "You defeated the AI in combat!"
                        else: # not human_player_alive
                            self.game_over_reason = "You were eliminated in combat."
                    
                    self.game_state = "GAME_OVER"
                    self.audio_manager.stop_all_sounds()
                    self.game_timer_active = False
                    if human_player_alive: p1_won_by_ko = True

            if self.game_state == "GAME_OVER":
                is_p1_winner = (p1_won_by_ko or p1_won_by_time)
                if is_p1_winner and self.player1 and self.leaderboard_manager.is_score_high_enough(self.player1.score):
                    self.score_to_submit = self.player1.score
                    self.player_name_input = ""
                    self.input_box_active = True
                    self.game_state = "ENTER_NAME"
                    self.audio_manager.stop_all_sounds() # Stop any lingering sounds (like ticking)
                    self.victory()
                else:
                    # 如果玩家勝利但分數不高、或AI勝利、或平手，則建立按鈕
                    if not self.game_over_button_rect:
                        btn_w, btn_h = self.continue_button_img.get_size()
                        self.game_over_button_rect = pygame.Rect(
                            (settings.SCREEN_WIDTH - btn_w) / 2,
                            settings.SCREEN_HEIGHT / 2 + 80, # 往下移動為副標題騰出空間
                            btn_w, btn_h
                        )

        elif self.game_state == "ENTER_NAME":
            # 進入輸入姓名畫面時，建立繼續按鈕
            if not self.game_over_button_rect:
                btn_w, btn_h = self.continue_button_img.get_size()
                self.game_over_button_rect = pygame.Rect(
                    (settings.SCREEN_WIDTH - btn_w) / 2,
                    settings.SCREEN_HEIGHT / 2 + 100,
                    btn_w, btn_h
                )
            pass

        elif self.game_state == "SCORE_SUBMITTED":
            self.score_submitted_message_timer += self.dt
            if self.score_submitted_message_timer >= self.score_submitted_message_duration:
                self.restart_game = True
                self.running = False # 標記 Game 場景結束

    # 【修改】將原本的 draw() 改名為 _draw_internal()
    def _draw_internal(self):
        if self.headless:
            return
        # (draw 函式的內容保持不變)
        # self.screen.fill(settings.WHITE)
        tile_img = self.brick_tile_image
        tile_width, tile_height = tile_img.get_size()

        screen_width, screen_height = self.screen.get_size()

        for y in range(tile_height, tile_height*10, tile_height):
            for x in range(tile_width, tile_width*14, tile_width):
                self.screen.blit(tile_img, (x, y))
        for y in range(tile_height, tile_height*15, tile_height):
            for x in range(tile_width*15, screen_width-tile_width, tile_width):
                self.screen.blit(self.beside_brick, (x, y))
        for y in range(tile_height*11, screen_height-tile_height, tile_height):
            for x in range(tile_width, tile_width*15, tile_width):
                self.screen.blit(self.text_brick, (x, y))
        for y in range(tile_height*15, screen_height-tile_height, tile_height):
            for x in range(tile_width*15, screen_width-tile_width, tile_width):
                self.screen.blit(self.text_brick, (x, y))

        for y in range(0, screen_height, tile_height):
            self.screen.blit(self.border_brick, (0, y))
            self.screen.blit(self.border_brick, (screen_width - tile_width, y))
            self.screen.blit(self.border_brick, (tile_width*14, y))
        for x in range(0, screen_width, tile_width):
            self.screen.blit(self.border_brick, (x, 0))
            self.screen.blit(self.border_brick, (x, tile_height*18))
        for x in range(tile_width*15, screen_width-tile_width, tile_width):
            self.screen.blit(self.border_brick, (x, tile_height*14))


        if self.game_state == "ENTER_NAME":
            self.draw_enter_name_screen()
        elif self.game_state == "SCORE_SUBMITTED":
            self.draw_score_submitted_screen()
        else: 
            self.all_sprites.draw(self.screen) 
            self.bombs_group.draw(self.screen)
            self.floating_texts_group.draw(self.screen)
            for bomb in self.bombs_group:
                bomb.draw_timer_bar(self.screen)
            if self.game_state == "PLAYING":
                if self.player2_ai and self.player2_ai.is_alive and self.ai_controller_p2:
                    if hasattr(self.ai_controller_p2, 'debug_draw_path'):
                        self.ai_controller_p2.debug_draw_path(self.screen)
                self.draw_hud()
                # 【新增】繪製暫停按鈕
                if self.hud_icon_pause:
                    self.screen.blit(self.hud_icon_pause, self.pause_button_rect)
                if self.touch_controls:
                    self.touch_controls.draw(self.screen)
            elif self.game_state == "GAME_OVER":
                self.draw_game_over_screen()

        # pygame.display.flip() # 由 main.py 的主迴圈呼叫

    # handle_enter_name_state_events, draw_pixel_digit, draw_hud, draw_game_over_screen,
    # draw_enter_name_screen, draw_score_submitted_screen 這些方法保持不變，
    # 因為它們是被 _process_events_internal 或 _draw_internal 內部呼叫的。
    def handle_enter_name_state_events(self, event):
        # 處理滑鼠點擊事件 (點擊輸入框或繼續按鈕)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.game_over_button_rect and self.game_over_button_rect.collidepoint(event.pos):
                # 點擊繼續按鈕，提交分數
                player_name_to_save = self.player_name_input.strip() or "Player"
                self.leaderboard_manager.add_score(
                    player_name=player_name_to_save,
                    score=self.score_to_submit,
                    ai_defeated_type=self.ai_archetype
                )
                self.game_state = "SCORE_SUBMITTED"
                self.score_submitted_message_timer = 0.0
                self.input_box_active = False
                self.game_over_button_rect = None # 清除按鈕
                return # 事件已處理

            if self.name_input_rect.collidepoint(event.pos):
                self.input_box_active = not self.input_box_active
            else:
                self.input_box_active = False
        
        if event.type == pygame.KEYDOWN:
            if self.input_box_active:
                if event.key == pygame.K_RETURN:
                    player_name_to_save = self.player_name_input.strip()
                    if not player_name_to_save:
                        player_name_to_save = "Player" 
                    
                    self.leaderboard_manager.add_score(
                        player_name=player_name_to_save,
                        score=self.score_to_submit,
                        ai_defeated_type=self.ai_archetype
                    )
                    self.game_state = "SCORE_SUBMITTED"
                    self.score_submitted_message_timer = 0.0 
                    self.input_box_active = False 
                                        
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name_input = self.player_name_input[:-1]
                else:
                    if len(self.player_name_input) < getattr(settings, "TEXT_INPUT_MAX_LENGTH", 10):
                        if event.unicode.isprintable() and event.key not in (pygame.K_TAB, pygame.K_ESCAPE, pygame.K_RETURN):
                             self.player_name_input += event.unicode
            elif event.key == pygame.K_ESCAPE: 
                self.game_state = "GAME_OVER" # 這裡其實會被 _process_events_internal 的 ESC 處理覆蓋
                self.restart_game = True 
                self.running = False

    def draw_pixel_digit(self, digit_char, top_left_x, top_left_y, block_size=settings.TILE_SIZE):
        # (此函式保持不變)
        pattern = DIGIT_MAP.get(digit_char)
        if not pattern:
            return

        for row in range(len(pattern)):
            for col in range(len(pattern[0])):
                if pattern[row][col]:
                    dest_x = top_left_x + col * block_size
                    dest_y = top_left_y + row * block_size
                    self.screen.blit(self.timer_brick, (dest_x, dest_y))

    def draw_hud(self):
        if not self.hud_font:
            return

        # --- Timer (Right Side) ---
        time_left = max(0, settings.GAME_DURATION_SECONDS - self.time_elapsed_seconds)
        minutes = int(time_left) // 60
        seconds = int(time_left) % 60
        timer_text_1 = f"{minutes:02d}"
        timer_text_2 = f"{seconds:02d}"

        start_x_timer = settings.TILE_SIZE * 16
        start_y_timer = settings.TILE_SIZE * 2
        block_size = self.border_brick.get_width()
        spacing = settings.TILE_SIZE

        for i, char in enumerate(timer_text_1):
            self.draw_pixel_digit(char, top_left_x=start_x_timer + i * (3 * block_size + spacing), top_left_y=start_y_timer)
        for i, char in enumerate(timer_text_2):
            self.draw_pixel_digit(char, top_left_x=start_x_timer + i * (3 * block_size + spacing), top_left_y=start_y_timer + 5 * block_size + spacing)

        # --- Player and AI Stats (Left Side, Vertical) ---
        # Position the HUD to the right of the touch controls
        # Assuming touch controls take up about 200px on the left.
        start_x = 190
        start_y = settings.SCREEN_HEIGHT - 200 # 再次向上移動資訊
        line_height = 35 # Vertical spacing between each stat line
        icon_text_spacing = 8
        
        # --- Helper function to draw a single stat line (icon + text) vertically ---
        def draw_stat_vertical(surface, icon, text, x, y, font):
            icon_rect = icon.get_rect(topleft=(x, y))
            surface.blit(icon, icon_rect)
            
            text_surf = font.render(text, True, settings.WHITE)
            text_rect = text_surf.get_rect(midleft=(icon_rect.right + icon_text_spacing, icon_rect.centery))
            draw_text_with_shadow(surface, text, font, text_rect.topleft, text_color=settings.WHITE, shadow_color=settings.BLACK)

        # --- Draw Player 1 Stats ---
        if self.player1 and self.hud_icon_heart and self.hud_icon_bomb and self.hud_icon_score:
            p1_label_surf = self.hud_font.render("P1", True, settings.WHITE)
            draw_text_with_shadow(self.screen, "P1", self.hud_font, (start_x, start_y), text_color=settings.WHITE, shadow_color=settings.BLACK)
            
            # P1 Lives
            lives_text = f"{self.player1.lives}"
            draw_stat_vertical(self.screen, self.hud_icon_heart, lives_text, start_x, start_y + line_height * 1, self.hud_font)
            
            # P1 Bombs
            bombs_text = f"{self.player1.max_bombs - self.player1.bombs_placed_count}/{self.player1.max_bombs}"
            draw_stat_vertical(self.screen, self.hud_icon_bomb, bombs_text, start_x, start_y + line_height * 2, self.hud_font)

            # P1 Score
            score_text = f"{self.player1.score}"
            draw_stat_vertical(self.screen, self.hud_icon_score, score_text, start_x, start_y + line_height * 3, self.hud_font)

        # --- Draw AI Stats ---
        # Position AI stats to the right of Player 1 stats
        ai_start_x = start_x + 120 # 縮小與 P1 資訊的間距
        if self.player2_ai and self.hud_icon_heart and self.hud_icon_bomb and self.hud_icon_score:
            ai_label_surf = self.hud_font.render("AI", True, settings.WHITE)
            draw_text_with_shadow(self.screen, "AI", self.hud_font, (ai_start_x, start_y), text_color=settings.WHITE, shadow_color=settings.BLACK)

            # AI Lives
            if self.player2_ai.is_alive:
                lives_text = f"{self.player2_ai.lives}"
                draw_stat_vertical(self.screen, self.hud_icon_heart, lives_text, ai_start_x, start_y + line_height * 1, self.hud_font)
                
                # AI Bombs
                bombs_text = f"{self.player2_ai.max_bombs - self.player2_ai.bombs_placed_count}/{self.player2_ai.max_bombs}"
                draw_stat_vertical(self.screen, self.hud_icon_bomb, bombs_text, ai_start_x, start_y + line_height * 2, self.hud_font)

                # AI Score
                score_text = f"{self.player2_ai.score}"
                draw_stat_vertical(self.screen, self.hud_icon_score, score_text, ai_start_x, start_y + line_height * 3, self.hud_font)

            else:
                # If AI is defeated, show only that status
                defeated_text = "Defeated"
                text_surf = self.hud_font.render(defeated_text, True, settings.RED)
                text_rect = text_surf.get_rect(topleft=(ai_start_x, start_y + line_height))
                draw_text_with_shadow(self.screen, defeated_text, self.hud_font, text_rect.topleft, text_color=settings.RED, shadow_color=settings.BLACK)

        # --- Draw AI State in Bottom Right Box ---
        if self.player2_ai and self.player2_ai.is_alive and self.ai_controller_p2 and self.ai_status_font:
            # Define the bottom-right box area
            box_x = settings.TILE_SIZE * 15
            box_y = settings.TILE_SIZE * 15
            box_width = settings.SCREEN_WIDTH - box_x - settings.TILE_SIZE
            box_height = settings.SCREEN_HEIGHT - box_y - settings.TILE_SIZE
            box_center_x = box_x + box_width / 2
            box_center_y = box_y + box_height / 2

            # --- AI State Translation Map ---
            state_translation = {
                "IDLE": "閒置",
                "DEAD": "已陣亡",
                # General states
                "PLANNING_PATH": "規劃路徑",
                "ROAMING": "巡邏中",
                "EVADING_DANGER": "緊急迴避",
                "TACTICAL_RETREAT_AND_WAIT": "戰術性撤退",
                "MOVING_TO_BOMB_OBSTACLE": "清除障礙物",
                
                # Aggressive & Item-Focused states
                "PLANNING_PATH_TO_PLAYER": "規劃追擊路線",
                "EXECUTING_PATH_CLEARANCE": "清除路徑障礙",
                "ENGAGING_PLAYER": "鎖定玩家",
                "CLOSE_QUARTERS_COMBAT": "近身纏鬥",
                
                # Conservative states
                "PLANNING_ROAM": "規劃巡邏路線",
                "ASSESSING_OBSTACLE": "評估障礙物",

                # Item-Focused states
                "PLANNING_ITEM_TARGET": "搜尋道具",
                "MOVING_TO_COLLECT_ITEM": "衝向道具",
                "EXECUTING_ASTAR_PATH_TO_TARGET": "執行尋路",
                "ASSESSING_OBSTACLE_FOR_ITEM": "為道具清障",
                "ENDGAME_HUNT": "終局狩獵"
            }

            # Prepare the two lines of text
            class_name = self.ai_controller_p2.__class__.__name__
            ai_name = class_name.replace("AIController", "").replace("Conservative", "保守型").replace("Aggressive", "侵略型").replace("ItemFocused", "道具型")
            if not ai_name or ai_name == "Standard": ai_name = "標準型"
            
            state_key = getattr(self.ai_controller_p2, 'current_state', 'N/A')
            translated_state = state_translation.get(state_key, state_key) # Translate, or fallback to original
            
            line1_text = f"AI ({ai_name}):"
            line2_text = f"{translated_state}"

            # Draw the two lines centered in the box
            line1_surf = self.ai_status_font.render(line1_text, True, settings.WHITE)
            line2_surf = self.ai_status_font.render(line2_text, True, settings.WHITE)
            
            line1_rect = line1_surf.get_rect(center=(box_center_x - 50, box_center_y - self.ai_status_font.get_height() / 2))
            line2_rect = line2_surf.get_rect(center=(box_center_x - 50, box_center_y + self.ai_status_font.get_height() / 2))
            
            draw_text_with_shadow(self.screen, line1_text, self.ai_status_font, line1_rect.topleft, text_color=settings.WHITE, shadow_color=settings.BLACK)
            draw_text_with_shadow(self.screen, line2_text, self.ai_status_font, line2_rect.topleft, text_color=settings.WHITE, shadow_color=settings.BLACK)

    def draw_game_over_screen(self):
        # (此函式保持不變)
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))  # R, G, B, A (180 ≈ 70% 不透明)
        self.screen.blit(overlay, (0, 0))
        if not self.game_over_font or not self.restart_font:
            return

        msg = "GAME OVER"; color = settings.RED
        p1_alive = self.player1 and self.player1.is_alive
        ai_alive = self.player2_ai and self.player2_ai.is_alive

        if self.time_up_winner:
            if self.time_up_winner == "P1": msg = "TIME'S UP! P1 WINS!"; color = (50, 134, 138)
            elif self.time_up_winner == "AI": msg = "TIME'S UP! AI WINS!"; color = (141, 24, 23)
            else: msg = "TIME'S UP! DRAW!"; color = settings.GREY
        else:
            if not p1_alive and not ai_alive: msg = "DRAW!"; color = settings.GREY
            elif not p1_alive: msg = "GAME OVER - YOU LOST!"; color = (141, 24, 23)
            elif not ai_alive: msg = "VICTORY - AI DEFEATED!"; color = (50, 134, 138)
        
        game_over_text = self.game_over_font.render(msg, True, color)
        text_rect = game_over_text.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2 - 80))
        self.screen.blit(game_over_text, text_rect)

        # 繪製遊戲結束原因的副標題
        if self.game_over_reason and self.restart_font:
            reason_surf = self.restart_font.render(self.game_over_reason, True, settings.DARK_GREY)
            reason_rect = reason_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, text_rect.bottom + 30)) # 稍微增加間距
            self.screen.blit(reason_surf, reason_rect)
        
        # 繪製返回主選單的按鈕
        if self.game_over_button_rect:
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = self.game_over_button_rect.collidepoint(mouse_pos)
            button_img = self.continue_button_hover_img if is_hovering else self.continue_button_img
            self.screen.blit(button_img, self.game_over_button_rect)

            # 重新加入鍵盤提示文字，並修改顏色
            restart_text = self.restart_font.render("or Press 'R' to return", True, settings.DARK_GREY)
            restart_rect = restart_text.get_rect(center=(settings.SCREEN_WIDTH / 2, self.game_over_button_rect.bottom + 20))
            self.screen.blit(restart_text, restart_rect)

    def draw_enter_name_screen(self):
        # (此函式保持不變)
        if not self.text_input_font or not self.prompt_font or not self.hud_font:
            return
        self.screen.blit(self.victory_background_image, (0, 0))
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0,0))
        color = pygame.Color('white') if self.input_box_active else pygame.Color('lightskyblue3')

        prompt_text = self.prompt_font.render("You've got a high score!", True, settings.WHITE)
        prompt_rect = prompt_text.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2 - 140))
        self.screen.blit(prompt_text, prompt_rect)

        # 顯示勝利原因
        if self.game_over_reason and self.restart_font:
            reason_surf = self.restart_font.render(self.game_over_reason, True, settings.LIGHT_GREY) # 使用淺灰色
            reason_rect = reason_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, prompt_rect.bottom + 30))
            self.screen.blit(reason_surf, reason_rect)

        pygame.draw.rect(self.screen, color, self.name_input_rect, 2)
        text_surface = self.text_input_font.render(self.player_name_input, True, settings.WHITE)
        
        # 修正文字位置，使其垂直置中
        text_rect = text_surface.get_rect(midleft=(self.name_input_rect.x + 10, self.name_input_rect.centery))
        self.screen.blit(text_surface, text_rect)
        self.name_input_rect.w = max(280, text_surface.get_width() + 20)

        # 繪製繼續按鈕
        if self.game_over_button_rect:
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = self.game_over_button_rect.collidepoint(mouse_pos)
            button_img = self.continue_button_hover_img if is_hovering else self.continue_button_img
            self.screen.blit(button_img, self.game_over_button_rect)

            # 加入鍵盤提示
            submit_prompt_text = "or Press ENTER to Submit"
            if self.victory_font:
                submit_surf = self.victory_font.render(submit_prompt_text, True, settings.DARK_GREY)
                submit_rect = submit_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, self.game_over_button_rect.bottom + 20))
                self.screen.blit(submit_surf, submit_rect)

    def draw_score_submitted_screen(self):
        # (此函式保持不變)
        if not self.message_font or not self.hud_font :
            return

        self.screen.blit(self.victory_background_image, (0, 0))
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 150))  # R, G, B, A (180 ≈ 70% 不透明)
        self.screen.blit(overlay, (0, 0))

        message_text = "Score Recorded on Leaderboard!"
        message_surf = self.message_font.render(message_text, True, settings.BLACK)
        message_rect = message_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2 - 30))
        self.screen.blit(message_surf, message_rect)

        continue_prompt_text = "Press any key or click to continue..."
        continue_surf = self.message_font.render(continue_prompt_text, True, settings.DARK_GREY)
        continue_rect = continue_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, message_rect.bottom + 40))
        self.screen.blit(continue_surf, continue_rect)

        if self.restart_font:
            # 加入自動跳轉的提示副標題
            auto_return_text = "(Returning to menu automatically...)"
            auto_return_surf = self.restart_font.render(auto_return_text, True, settings.DARK_GREY) # 使用灰色以區別
            auto_return_rect = auto_return_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, continue_rect.bottom + 20))
            self.screen.blit(auto_return_surf, auto_return_rect)