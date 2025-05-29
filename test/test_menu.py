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