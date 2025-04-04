import sys
from PyQt5.QtWidgets import QApplication
from engine.game_logic import GameEngine

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = GameEngine()
    game.setFixedSize(1920, 1080) #game.setGeometry(0,0,1920, 1080) funny
    sys.exit(app.exec_())