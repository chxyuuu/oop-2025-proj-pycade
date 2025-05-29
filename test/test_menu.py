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