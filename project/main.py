import pygame
from view import GameView

pygame.init()


def main():
    view = GameView()
    view.menu()


if __name__ == '__main__':
    main()
    pygame.quit()
