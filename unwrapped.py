import time
import pygame
import numpy as np

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)
COLOR_DEAD = (0, 0, 0)

def get_neighbor_sum(cells, row, col):
    n_rows, n_cols = cells.shape

    top = max(row - 1, 0)
    bottom = min(row + 1, n_rows - 1)
    left = max(col - 1, 0)
    right = min(col + 1, n_cols - 1)

    return (
        cells[top, left] + cells[top, col] + cells[top, right] +
        cells[row, left] + cells[row, right] +
        cells[bottom, left] + cells[bottom, col] + cells[bottom, right]
    )

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros_like(cells)

    for row, col in np.ndindex(cells.shape):
        alive = get_neighbor_sum(cells, row, col)
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
                    row = pos[1] // 10
                    col = pos[0] // 10
                    if 0 <= row < cells.shape[0] and 0 <= col < cells.shape[1]:
                        cells[row, col] = 0
                else:
                    row = pos[1] // 10
                    col = pos[0] // 10
                    if 0 <= row < cells.shape[0] and 0 <= col < cells.shape[1]:
                        cells[row, col] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)

if __name__ == '__main__':
    main()
