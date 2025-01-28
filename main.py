from random import randrange

import pygame, asyncio
from pygame import Vector2

import config

screen = pygame.display.set_mode((config.SCREEN_SIZE, config.SCREEN_SIZE))
clock = pygame.time.Clock()

time = None
snake_rect = None
snake_length = None
snake_parts = None
snake_direction = None

food_rect = None

async def main():
    begin = True
    bait = True

    while True:
        if begin:
            begin = False
            time = 0
            snake_rect = pygame.rect.Rect(
                [randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
                randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
                config.SNAKE_PART_SIZE,
                config.SNAKE_PART_SIZE])
            snake_length = 1
            snake_parts = []
            snake_direction = Vector2(0, 0)

        if bait:
            bait = False
            food_rect = pygame.rect.Rect([randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
                                        randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
                                        config.FOOD_SIZE,
                                        config.FOOD_SIZE])

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not snake_direction[1] > 0:
                    snake_direction = Vector2(0, -config.SNAKE_MOVE_LENGTH)
                if event.key == pygame.K_DOWN and not snake_direction[1] < 0:
                    snake_direction = Vector2(0, config.SNAKE_MOVE_LENGTH)
                if event.key == pygame.K_LEFT and not snake_direction[0] > 0:
                    snake_direction = Vector2(-config.SNAKE_MOVE_LENGTH, 0)
                if event.key == pygame.K_RIGHT and not snake_direction[0] < 0:
                    snake_direction = Vector2(config.SNAKE_MOVE_LENGTH, 0)

        time_now = pygame.time.get_ticks()

        screen.fill(config.BG_COLOR)

        for i in range(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE):
            pygame.draw.line(screen, config.GRID_COLOR, (i, 0), (i, config.SCREEN_SIZE))
            pygame.draw.line(screen, config.GRID_COLOR, (0, i), (config.SCREEN_SIZE, i))

        if time_now - time > config.DELAY:
            time = time_now
            snake_rect.move_ip(snake_direction)
            snake_parts.append(snake_rect.copy())
            snake_parts = snake_parts[-snake_length:]

        pygame.draw.rect(screen, config.FOOD_COLOR, food_rect, 0, 10)

        [pygame.draw.rect(screen, config.SNAKE_COLOR, snake_part, 8, 4)
        for snake_part in snake_parts]

        if (snake_rect.left < 0 or snake_rect.right > config.SCREEN_SIZE or
                snake_rect.top < 0 or snake_rect.bottom > config.SCREEN_SIZE or
                len(snake_parts) != len(set(snake_part.center for snake_part in snake_parts))):
            begin = True

        if snake_rect.center == food_rect.center:
            snake_length += 1
            bait = True

        pygame.display.flip()
        clock.tick(config.FPS)
        await asyncio.sleep(0)

asyncio.run(main())