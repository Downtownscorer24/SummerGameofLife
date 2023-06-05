# There is one big difference in this version
# 1. The "neighborhood" of each cells is now 2-pixels outward, as opposed to 1-pixel in the complete normal version
# 2. Now that the 'neighborhood" of cells has increased from 8 to 24, all the rules have been multiplied by three, hence the R3 in the name
# This means that to die, "neighborhood" cells must be less that six or greater than 9, since it was previously 2 and 3.
# To stay alive, the window is "neighborhood" cells must be within 6 and 9, both inclusive.
# To become alive, any dead cells with [6,9] neighbors become alive
# Press 'd' if you want to shift into setting cells dead. Make sure to click 'd' again to switch to setting cells alive

import time
import pygame
import numpy as np

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)


def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-2:row+3, col-2:col+3]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
           if alive < 6 or alive > 9:
               if with_progress:
                   color = COLOR_DIE_NEXT
           elif 6 <= alive <= 9:
               updated_cells[row, col] = 1
               if with_progress:
                   color = COLOR_ALIVE_NEXT

        else:
            if 6 < alive < 9:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color,(col * size, row * size, size -1, size - 1))

    return updated_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False
    cell_deactivation = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
                elif event.key == pygame.K_d:
                    cell_deactivation = not cell_deactivation
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if cell_deactivation:
                    cells[pos[1] // 10, pos[0] // 10] = 0
                else:
                    cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)
if __name__ == '__main__':
    main()







