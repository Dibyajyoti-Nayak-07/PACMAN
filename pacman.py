import pygame
import heapq
from collections import deque

GRID_SIZE = 5
CELL_SIZE = 100
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

grid = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
]

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption("Pac-Man Search Visualization")
clock = pygame.time.Clock()

def is_valid_move(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[x][y] == 0

def bfs(start, goal):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if is_valid_move(*neighbor) and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]

def dfs(start, goal):
    stack = [start]
    visited = set()
    parent = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            break
        if current not in visited:
            visited.add(current)
            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if is_valid_move(*neighbor) and neighbor not in visited:
                    parent[neighbor] = current
                    stack.append(neighbor)

    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            break

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if is_valid_move(*neighbor):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current, None)
    return path[::-1]

def uniform_cost_search(start, goal):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while priority_queue:
        current_cost, current = heapq.heappop(priority_queue)

        if current == goal:
            break

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if is_valid_move(*neighbor):
                new_cost = current_cost + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(priority_queue, (new_cost, neighbor))

    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current, None)
    return path[::-1]

def draw_grid(path):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = WHITE if grid[x][y] == 0 else BLACK
            pygame.draw.rect(screen, color, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    for (x, y) in path:
        pygame.draw.rect(screen, GREEN, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    start = (0, 0)
    goal = (4, 4)
    
    # path = bfs(start, goal)
    # path = dfs(start, goal)
    path = a_star(start, goal)
    # path = uniform_cost_search(start, goal)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw_grid(path)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()