import time
import pygame
import numpy as np

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)
COLOR_DEAD = (0, 0, 0)
COLOR_PATTERN = (255, 255, 0)

def update(screen, cells, size, pattern_count, pattern_positions, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    updated_pattern_positions = []

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
                if (row, col) in pattern_positions:
                    updated_pattern_positions.append((row, col))
                    color = COLOR_PATTERN
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
                if (row, col) in pattern_positions:
                    updated_pattern_positions.append((row, col))
                    color = COLOR_PATTERN

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    # Check if the pattern appears and increment the pattern count
    if pattern_count is not None and not with_progress:
        pattern = np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]])
        pattern_detected = False
        for row in range(cells.shape[0] - 3):
            for col in range(cells.shape[1] - 3):
                if np.array_equal(cells[row:row+4, col:col+4], pattern):
                    if (row+1, col+1) not in pattern_positions:
                        pattern_count += 1
                        updated_pattern_positions.extend([(row+1, col+1), (row+1, col+2), (row+2, col+1), (row+2, col+2)])
                        pattern_detected = True
                    break
            if pattern_detected:
                break
        if not pattern_detected:
            pattern_positions.clear()

    return updated_cells, pattern_count, updated_pattern_positions


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    pattern_count = 0
    pattern_positions = []

    update(screen, cells, 10, pattern_count, pattern_positions)

    pygame.display.flip()
    pygame.display.update()

    running = False
    cell_deactivation = False
    prev_pattern_count = pattern_count
    pattern_detected = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                elif event.key == pygame.K_d:
                    cell_deactivation = not cell_deactivation
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if cell_deactivation:
                    cells[pos[1] // 10, pos[0] // 10] = 0
                else:
                    cells[pos[1] // 10, pos[0] // 10] = 1

        screen.fill(COLOR_GRID)

        if running:
            cells, pattern_count, pattern_positions = update(screen, cells, 10, pattern_count, pattern_positions, with_progress=True)
            pygame.display.update()

        if prev_pattern_count != pattern_count:
            prev_pattern_count = pattern_count
            print("Pattern Count:", pattern_count)

        if not pattern_detected and pattern_count > 0:
            pattern_detected = True
            print("Pattern Detected!")

        time.sleep(0.001)

if __name__ == '__main__':
    main()
