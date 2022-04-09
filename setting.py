import pygame

# fov = 11
fov = 19
gameDisplay = pygame.display.set_mode((50*fov, 50*fov))
# display_width, display_height = len(map[0][0]) *50, len(map[0])*50
display_width, display_height = 5000, 5000
pygame.display.set_caption('A Fishing Game')
clock = pygame.time.Clock()
walk_speed = 5
FPS = 60
