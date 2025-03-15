import sys
from PyQt5.QtWidgets import QApplication
from engine.game_logic import GameEngine

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = GameEngine()
    game.showNormal()
    sys.exit(app.exec_())