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


def draw_generation_counter(screen, current_generation):
    font = pygame.font.Font(None, 36)
    text = font.render("Generation: {}".format(current_generation), True, (255, 255, 255))
    screen.blit(text, (10, 10))


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    rows, cols = 60, 80
    cell_size = 10
    cells = np.zeros((rows, cols))
    screen.fill(COLOR_GRID)
    for x in range(0, 800, cell_size):
        pygame.draw.line(screen, (70, 70, 70), (x, 0), (x, 600))
    for y in range(0, 600, cell_size):
        pygame.draw.line(screen, (70, 70, 70), (0, y), (800, y))

    pygame.display.flip()
    pygame.display.update()

    running = False
    cell_deactivation = False
    current_generation = 0

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
                elif event.key == pygame.K_RETURN and not running:
                    try:
                        input_generation = int(input("Enter the generation to navigate: "))
                        if input_generation >= 0:
                            while current_generation < input_generation:
                                cells = update(screen, cells, cell_size, with_progress=True)
                                current_generation += 1
                                draw_generation_counter(screen, current_generation)
                                pygame.display.update()
                            draw_generation_counter(screen, current_generation)
                        else:
                            print("Invalid input. Please enter a non-negative generation number.")
                    except ValueError:
                        print("Invalid input. Please enter a valid generation number.")

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if cell_deactivation:
                    cells[pos[1] // cell_size, pos[0] // cell_size] = 0
                    pygame.draw.rect(screen, COLOR_DEAD,
                                     (pos[0] // cell_size * cell_size, pos[1] // cell_size * cell_size, cell_size - 1, cell_size - 1))
                else:
                    cells[pos[1] // cell_size, pos[0] // cell_size] = 1
                    pygame.draw.rect(screen, COLOR_ALIVE_NEXT,
                                     (pos[0] // cell_size * cell_size, pos[1] // cell_size * cell_size, cell_size - 1, cell_size - 1))
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, cell_size, with_progress=True)
            current_generation += 1
            draw_generation_counter(screen, current_generation)
            pygame.display.update()

        time.sleep(0.001)


if __name__ == '__main__':
    main()
