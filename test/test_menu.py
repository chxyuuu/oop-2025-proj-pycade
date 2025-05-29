import unittest
from core.menu import Menu

class TestMenu(unittest.TestCase):
    def setUp(self):
        class MockScreen:
            def __init__(self):
                pass
            def fill(self, color):
                pass
            def blit(self, surface, rect):
                pass
        self.mock_screen = MockScreen()
        self.menu_options = ["Start Game", "Options", "Exit"]
        self.menu = Menu(self.mock_screen, self.menu_options)
    def test_initialization(self):
        self.assertEqual(self.menu.options, self.menu_options)
        self.assertEqual(self.menu.selected_option_index, 0)
    def test_move_selection_down(self):
        self.menu.move_selection_down()
        self.assertEqual(self.menu.selected_option_index, 1)
        self.menu.move_selection_down()
        self.assertEqual(self.menu.selected_option_index, 2)
        # 測試循環到開頭
        self.menu.move_selection_down()
        self.assertEqual(self.menu.selected_option_index, 0)
    def test_move_selection_up(self):
        self.menu.move_selection_up() # 從 0 移到最後一個
        self.assertEqual(self.menu.selected_option_index, len(self.menu_options) - 1)
        self.menu.move_selection_up()