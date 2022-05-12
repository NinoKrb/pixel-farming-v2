from main import Game
import os

if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
    game = Game()
    game.run()
