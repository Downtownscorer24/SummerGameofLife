# This version of GoL introduces randomness to the rules of the game (deaths, births, staying alive)
# In this version, survival probability is dependent on the death probability, and birth probability is seperate
# The current rules still add some effect
# For example, to stay alive, you must need to have neighbors within [2,3] AND the probability
# must fall in the cell's favor.
# Click cells to make alive and set initial configuration
# Press 'd' if you want to shift into setting cells dead. Make sure to click 'd' again to switch to setting cells alive

import time
import pygame
import numpy as np
import random

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)
COLOR_DEAD = (0, 0, 0)

death_prob = 0.001
survival_prob = 1 - death_prob
birth_prob = 0.99

def update(screen, cells, size, death_prob, survival_prob, birth_prob, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if alive < 2 or alive > 3 and random.random() < death_prob:
                updated_cells[row, col] = 0
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3 and random.random() < survival_prob:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3 and random.random() < birth_prob:
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
    update(screen, cells, 10, death_prob, survival_prob, birth_prob)

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
                    update(screen, cells, 10, 0.3, 0.6, 0.4)
                    pygame.display.update()
                elif event.key == pygame.K_d:
                    cell_deactivation = not cell_deactivation
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if cell_deactivation:
                    cells[pos[1] // 10, pos[0] // 10] = 0
                else:
                    cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10, death_prob, survival_prob, birth_prob)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, death_prob, survival_prob, birth_prob, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)

if __name__ == '__main__':
    main()
