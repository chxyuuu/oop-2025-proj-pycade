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
        self.assertEqual(len(self.game.players), 1) # 假設 Game 內部維護一個 players 列表
    def test_start_game(self):
        self.game.start_game()
        self.assertTrue(self.game.is_running)
    def test_end_game(self):
        self.game.start_game()
        self.game.end_game()
        self.assertFalse(self.game.is_running)
    def test_update_score(self):
        initial_score = self.player.score
        self.game.update_game_score(self.player, 100) # 假設有這個方法
        self.assertEqual(self.player.score, initial_score + 100)
    def test_game_over(self):
    # 假設遊戲結束的條件是玩家生命值為 0
         self.player.lives = 0
         self.game.check_game_over() # 假設有這個方法來檢查遊戲是否結束
         self.assertFalse(self.game.is_running)