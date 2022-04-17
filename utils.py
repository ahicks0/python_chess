from typing import Tuple
import pygame
def centerCoords(rect:  pygame.Rect, screen_size: Tuple):
    return screen_size[0]/2 - rect.width, screen_size[1]/2 - rect.height 