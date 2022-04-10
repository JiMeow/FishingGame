import random
import pygame
from setting import *
from player import Player
from screen import Screen
from tile_map import Tile, cut_picture, readmap
# import cProfile as cPd
pygame.init()


def main():
    global walk_speed
    crashed = False
    map = readmap()
    pygame.display.set_caption('A Fishing Game')
    screen = Screen(map)

    # play until crashed
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                screen.player.is_useItem = False
                screen.player.activity = False
                # controll player movement
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    screen.player.walk_x *= 2
                    screen.player.walk_y *= 2
                    walk_speed *= 2
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    screen.player.walk_x = -walk_speed
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    screen.player.walk_y = -walk_speed
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    screen.player.walk_x = walk_speed
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    screen.player.walk_y = walk_speed
                # open or close inventory
                if event.key == pygame.K_e:
                    screen.player.is_openinventory = not screen.player.is_openinventory
                # open or close chest
                if event.key == pygame.K_f:
                    screen.player.is_interact = not screen.player.is_interact
                    if not screen.player.is_interact:
                        screen.player.is_openshop = False
                        screen.player.is_openchest = False
                        screen.player.is_openinventory = False
                else:
                    if screen.player.is_openchest or screen.player.is_openshop:
                        screen.player.is_openinventory = False
                    screen.player.is_openshop = False
                    screen.player.is_openchest = False
                    screen.player.is_interact = False
                    # use item by num_pad
                for i in range(1, 10):
                    if event.key == eval(f"pygame.K_{i}"):
                        screen.player.selectSlot = i-1

            if event.type == pygame.KEYUP:
                # stop player movement
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    screen.player.walk_x //= 2
                    screen.player.walk_y //= 2
                    walk_speed //= 2
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    screen.player.walk_x = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    screen.player.walk_y = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    screen.player.walk_x = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    screen.player.walk_y = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                # use item by mouse
                if event.button == 4:
                    screen.player.is_useItem = False
                    screen.player.selectSlot -= 1
                    screen.player.selectSlot %= 9
                    if screen.player.selectInventory[0] == 3:
                        screen.player.selectInventory[1] = screen.player.selectSlot
                if event.button == 5:
                    screen.player.is_useItem = False
                    screen.player.selectSlot += 1
                    screen.player.selectSlot %= 9
                    if screen.player.selectInventory[0] == 3:
                        screen.player.selectInventory[1] = screen.player.selectSlot
                # use item by mouse ans wap by drag mouse and merge LastInventory-Slot
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if screen.player.is_fishing:
                        screen.player.rodspeed = -screen.player.rodspeed
                    if screen.player.is_openshop:
                        if mouse_x in range(425, 475) and mouse_y in range(450, 500):
                            screen.player.click = "shop"
                            screen.player.is_drawItemShop = True
                        elif mouse_x in range(525, 575) and mouse_y in range(450, 500):
                            screen.player.click = "shop"
                            screen.player.is_sell = True
                            screen.player.is_drawItemShop = False
                        else:
                            screen.player.is_drawItemShop = False
                    if screen.player.is_openchest:
                        if mouse_x in range(265, 684) and mouse_y in range(265, 475):
                            screen.player.click = "chest"
                            screen.player.is_drawItemChest = True
                            screen.player.selectChest[0] = (
                                mouse_y-265)//50 % 4
                            screen.player.selectChest[1] = (
                                mouse_x-265)//46 % 9
                        else:
                            screen.player.is_drawItemChest = False
                    if not screen.player.is_openinventory:
                        if mouse_y in range(860, 895) and mouse_x in range(282, 675):
                            screen.player.click = "inventory"
                            screen.player.selectSlot = (mouse_x-282)//44 % 9
                            if screen.player.selectInventory[0] == 3:
                                screen.player.selectInventory[1] = screen.player.selectSlot
                            screen.player.is_drawItemSlot = True
                        else:
                            if not screen.player.activity:
                                screen.player.is_useItem = True
                    elif screen.player.is_openinventory:
                        if mouse_x in range(268, 684) and mouse_y in range(563, 763):
                            screen.player.click = "inventory"
                            screen.player.selectInventory[0] = (
                                mouse_y-563)//50 % 4
                            screen.player.selectInventory[1] = (
                                mouse_x-268)//46 % 9
                            if screen.player.selectInventory[0] == 3:
                                screen.player.selectSlot = screen.player.selectInventory[1]
                            screen.player.is_drawItemInventory = True
                        else:
                            if not (screen.player.is_openchest or screen.player.is_openshop):
                                screen.player.is_openinventory = False

            if event.type == pygame.MOUSEBUTTONUP:
                # swap item by mouse
                if event.button == 1:
                    screen.player.is_drawItemChest = False
                    screen.player.is_drawItemInventory = False
                    screen.player.is_drawItemShop = False
                    screen.player.is_drawItemSlot = False
                    if screen.player.is_openshop:
                        if screen.player.click == "shop":
                            screen.player.is_swapshopinventory = True
                        elif screen.player.click == "inventory":
                            screen.player.is_swapinventoryshop = True
                    if screen.player.is_openchest:
                        if screen.player.click == "chest":
                            screen.player.is_swapchestinventory = True
                        elif screen.player.click == "inventory":
                            screen.player.is_swapinventorychest = True

                    if screen.player.is_openinventory:
                        screen.player.swapItemInventory()
                    else:
                        screen.player.swapItemSlot()

                    screen.player.rodspeed = -abs(screen.player.rodspeed)
            else:
                # look detail
                screen.player.checkDetail = True

        # draw bg
        screen.draw()
        # update screen
        clock.tick(60)
        gameDisplay.blit(pygame.font.Font(None, 32).render(
            f'FPS = {int(clock.get_fps())}', True, (255, 255, 255)), (20, 100))
        pygame.display.update()
        # FPS = 60
        # clock.tick(FPS)

    pygame.quit()
    quit()


# cP.run("main()")
main()
