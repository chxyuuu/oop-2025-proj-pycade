import unittest
from game import Game
from sprites.player import Player

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player = Player("TestPlayer")
        self.game.add_player(self.player) # 假設 Game 有 add_player 方法
    def test_initialization(self):
        self.assertFalse(self.game.is_running)
       