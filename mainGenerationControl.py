#This version is meant to add some features
# 1. ALlow user to see which generation the simulation is on
# 2. Allow user to input a new generation for the simulation to automatically jump to
# This is still in the works!!!

import time
import pygame
import numpy as np

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)
COLOR_DEAD = (0, 0, 0)

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def draw_grid(screen, size, rows, cols):
    screen.fill(COLOR_GRID)
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(screen, COLOR_DEAD, (col * size, row * size, size - 1, size - 1), 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    rows, cols = 60, 80
    size = 10
    cells = np.zeros((rows, cols))
    draw_grid(screen, size, rows, cols)

    pygame.display.flip()
    pygame.display.update()

    running = False
    cell_deactivation = False
    generation = 0
    updated_cells = cells.copy()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    if running:
                        generation = 0
                        updated_cells = cells.copy()
                elif event.key == pygame.K_d:
                    cell_deactivation = not cell_deactivation
                elif event.key == pygame.K_RETURN:
                    if not running:
                        try:
                            generation = int(input("Enter the desired generation: "))
                            generation = max(generation, 0)
                            for _ in range(generation):
                                updated_cells = update(screen, updated_cells, size, with_progress=True)
                        except ValueError:
                            print("Invalid input. Please enter a valid generation number.")

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if not running:
                    if cell_deactivation:
                        updated_cells[pos[1] // size, pos[0] // size] = 0
                    else:
                        updated_cells[pos[1] // size, pos[0] // size] = 1
                    draw_grid(screen, size, rows, cols)
                    pygame.display.update()

        if running:
            updated_cells = update(screen, updated_cells, size, with_progress=True)
            generation += 1
            pygame.display.update()

        time.sleep(0.001)

if __name__ == '__main__':
    main()
