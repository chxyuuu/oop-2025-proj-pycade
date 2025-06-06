import pygame
import pytest
import settings
from core.menu import Menu
from game import Game # Needed for asserting the type of returned scene
from core.leaderboard_manager import LeaderboardManager # For type checking

@pytest.fixture
def mock_menu_env(mocker):
    """
    Provides a basic Pygame environment (screen and clock) for menu tests.
    Mocks LeaderboardManager file operations.
    """
    pygame.display.init()  # Ensure display is initialized
    pygame.font.init()     # Ensure font system is initialized

    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    clock = pygame.time.Clock() # Menu creates its own clock, but Game might need one if we test that far

    # Mock LeaderboardManager to prevent actual file I/O during tests
    mocker.patch.object(LeaderboardManager, 'load_scores', return_value=[])
    mocker.patch.object(LeaderboardManager, 'save_scores', return_value=None)
    
    yield screen, clock # Using yield to ensure pygame.quit() can be called after tests if needed
    
    pygame.quit()

class TestMenu:
    """Test suite for the Menu class."""

    def test_menu_initialization(self, mock_menu_env):
        """Test if the Menu initializes correctly."""
        screen, _ = mock_menu_env
        menu = Menu(screen)

        assert menu.screen is screen, "Menu screen should be the one provided."
        assert menu.menu_state == "MAIN", "Initial menu state should be 'MAIN'."
        assert menu.buttons, "Menu should have buttons created."
        assert len(menu.buttons) == len(settings.AVAILABLE_AI_ARCHETYPES) + 2, \
               "Menu should have a button for each AI, plus leaderboard and quit."
        assert isinstance(menu.leaderboard_manager, LeaderboardManager), \
               "Menu should have a LeaderboardManager instance."
    
    def find_button_by_action(self, buttons, action_type, archetype_key=None):
        """Helper to find a button by its action_type and optionally archetype_key."""
        for button in buttons:
            if button.get("action_type") == action_type:
                if archetype_key:
                    if button.get("archetype") == archetype_key:
                        return button
                else:
                    return button
        return None
    
    def test_menu_shows_leaderboard(self, mock_menu_env):
        """Test if clicking the leaderboard button changes the menu state."""
        screen, _ = mock_menu_env
        menu = Menu(screen)

        leaderboard_button = self.find_button_by_action(menu.buttons, "SHOW_LEADERBOARD")
        assert leaderboard_button is not None, "Leaderboard button not found."

        # Simulate a mouse click event on the leaderboard button
        mouse_click_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'button': 1, 'pos': leaderboard_button["rect"].center}
        )
        
        # Menu's update should return self if it just changes internal state
        next_scene_or_action = menu.update([mouse_click_event])
        
        assert menu.menu_state == "LEADERBOARD", "Menu state should change to 'LEADERBOARD'."
        assert next_scene_or_action is menu, "Update should return self when changing to leaderboard."

    def test_menu_quit_game_action(self, mock_menu_env):
        """Test if clicking the quit button returns the 'QUIT' action."""
        screen, _ = mock_menu_env
        menu = Menu(screen)

        quit_button = self.find_button_by_action(menu.buttons, "QUIT_GAME")
        assert quit_button is not None, "Quit Game button not found."

        mouse_click_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'button': 1, 'pos': quit_button["rect"].center}
        )
        
        action = menu.update([mouse_click_event])
        assert action == "QUIT", "Clicking quit button should return 'QUIT' action."
    
    def test_menu_select_ai_starts_game(self, mock_menu_env):
        """Test if selecting an AI opponent returns a Game instance."""
        screen, _ = mock_menu_env # Clock is taken care of by Menu's own clock
        menu = Menu(screen)

        # Select the first AI archetype available in settings for the test
        first_ai_display_name = list(settings.AVAILABLE_AI_ARCHETYPES.keys())[0]
        first_ai_archetype_key = settings.AVAILABLE_AI_ARCHETYPES[first_ai_display_name]

        ai_button = self.find_button_by_action(menu.buttons, "SELECT_AI", first_ai_archetype_key)
        assert ai_button is not None, f"AI button for archetype '{first_ai_archetype_key}' not found."

        mouse_click_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'button': 1, 'pos': ai_button["rect"].center}
        )
        
        next_scene = menu.update([mouse_click_event])
        
        assert isinstance(next_scene, Game), "Selecting an AI should return a Game instance."
        assert next_scene.ai_archetype == first_ai_archetype_key, \
               "Game instance should be configured with the selected AI archetype."
        assert next_scene.screen is screen, "Game instance should use the same screen."
        # next_scene.clock should be menu.clock, which is fine.
    
    def test_menu_escape_from_leaderboard_returns_to_main(self, mock_menu_env):
        """Test if pressing ESC in leaderboard view returns to the main menu state."""
        screen, _ = mock_menu_env
        menu = Menu(screen)
        menu.menu_state = "LEADERBOARD" # Manually set state for the test

        escape_key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        
        # Update should return self after this internal state change
        next_scene_or_action = menu.update([escape_key_event])
        
        assert menu.menu_state == "MAIN", "Pressing ESC in leaderboard should return to 'MAIN' state."
        assert next_scene_or_action is menu, "Update should return self."
    
    def test_menu_escape_from_main_menu_quits(self, mock_menu_env):
        """Test if pressing ESC in the main menu returns the 'QUIT' action."""
        screen, _ = mock_menu_env
        menu = Menu(screen)
        
        assert menu.menu_state == "MAIN", "Menu should start in 'MAIN' state."

        escape_key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        
        action = menu.update([escape_key_event])
        assert action == "QUIT", "Pressing ESC in main menu should return 'QUIT' action."
    
    def test_menu_leaderboard_display(self, mock_menu_env):
        """Test if the leaderboard displays correctly."""
        screen, _ = mock_menu_env
        menu = Menu(screen)

        # Simulate the leaderboard button click to enter leaderboard state
        leaderboard_button = self.find_button_by_action(menu.buttons, "SHOW_LEADERBOARD")
        mouse_click_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'button': 1, 'pos': leaderboard_button["rect"].center}
        )
        menu.update([mouse_click_event])
        assert menu.menu_state == "LEADERBOARD", "Menu should be in 'LEADERBOARD' state."
        assert menu.leaderboard_manager is not None, "LeaderboardManager should be initialized."
        assert menu.leaderboard_manager.scores == [], "Leaderboard should be empty initially."
        # Check if the leaderboard is displayed correctly
        # This would typically involve checking the rendered text on the screen,
        # but since we can't render in tests, we can only check the state.
    
    def test_menu_button_positions(self, mock_menu_env):
        """Test if buttons are positioned correctly."""
        screen, _ = mock_menu_env
        menu = Menu(screen)

        # Check if the buttons are positioned within the screen bounds
        for button in menu.buttons:
            assert button["rect"].x >= 0, "Button x position should be non-negative."
            assert button["rect"].y >= 0, "Button y position should be non-negative."
            assert button["rect"].right <= settings.SCREEN_WIDTH, \
                   "Button right edge should not exceed screen width."
            assert button["rect"].bottom <= settings.SCREEN_HEIGHT, \
                   "Button bottom edge should not exceed screen height."
            # Check if the button rect is of reasonable size
            assert button["rect"].width > 0, "Button width should be positive."
            assert button["rect"].height > 0, "Button height should be positive."
    
    