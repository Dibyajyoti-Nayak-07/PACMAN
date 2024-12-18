import pygame
import random
from collections import deque
import heapq

GRID_SIZE = 10
CELL_SIZE = 50
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  
RED = (255, 0, 0)
BLUE = (0,0,255)


grid = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
]



directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
current_path = []
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption("Pac-Man Game with Pathfinding")
clock = pygame.time.Clock()

# Pac-Man starting position
pacman_pos = (0, 0)
pellets = [(1, 0), (2, 2), (4, 4), (8, 8), (0, 5)]
score = 0

def is_valid_move(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[x][y] == 0

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = WHITE if grid[x][y] == 0 else BLACK
            pygame.draw.rect(screen, color, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # Draw pellets
            if (x, y) in pellets:
                pygame.draw.circle(screen, RED, (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
            # Draw path
            if (x, y) in current_path:
                pygame.draw.rect(screen, GREEN, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE), width=3)
def draw_pacman():
    pygame.draw.circle(screen, YELLOW, (pacman_pos[1] * CELL_SIZE + CELL_SIZE // 2, pacman_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

def move_pacman(direction):
    global pacman_pos, score
    new_pos = (pacman_pos[0] + direction[0], pacman_pos[1] + direction[1])
    if is_valid_move(*new_pos):
        pacman_pos = new_pos
        if pacman_pos in pellets:
            pellets.remove(pacman_pos)
            score += 1

def bfs(start, goal):
    queue = deque([start])
    visited = set()
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
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if is_valid_move(*neighbor) and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]  

def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            return reconstruct_path(came_from, current)

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if is_valid_move(*neighbor):
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]  

def uniform_cost(start, goal):
    priority_queue = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while priority_queue:
        current_cost, current = heapq.heappop(priority_queue)

        if current == goal:
            return reconstruct_path(came_from, current)

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if is_valid_move(*neighbor):
                new_cost = current_cost + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority_queue.append((new_cost, neighbor))
                    came_from[neighbor] = current

    return []  

def main():
    global pacman_pos, score, current_path
    running = True
    pathfinding_in_progress = False  
    path_color = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_pacman(directions[0])
                elif event.key == pygame.K_DOWN:
                    move_pacman(directions[1])
                elif event.key == pygame.K_LEFT:
                    move_pacman(directions[2])
                elif event.key == pygame.K_RIGHT:
                    move_pacman(directions[3])
                elif event.key == pygame.K_b:  
                    if pellets:
                        pathfinding_in_progress = True
                        target = min(pellets, key=lambda p: abs(p[0] - pacman_pos[0]) + abs(p[1] - pacman_pos[1]))
                        current_path = bfs(pacman_pos, target)
                        path_color = GREEN
                        pathfinding_in_progress = False  
                        if len(current_path) > 1:
                            pacman_pos = current_path[1]  
                elif event.key == pygame.K_d:  
                    if pellets:
                        pathfinding_in_progress = True
                        target = min(pellets, key=lambda p: abs(p[0] - pacman_pos[0]) + abs(p[1] - pacman_pos[1]))
                        current_path = dfs(pacman_pos, target)
                        path_color = BLUE
                        pathfinding_in_progress = False
                        if len(current_path) > 1:
                            pacman_pos = current_path[1]  
                elif event.key == pygame.K_a:  
                    if pellets:
                        pathfinding_in_progress = True
                        target = min(pellets, key=lambda p: abs(p[0] - pacman_pos[0]) + abs(p[1] - pacman_pos[1]))
                        current_path = a_star(pacman_pos, target)
                        pathfinding_in_progress = False
                        if len(current_path) > 1:
                            pacman_pos = current_path[1]  
                elif event.key == pygame.K_u:  
                    if pellets:
                        pathfinding_in_progress = True
                        target = min(pellets, key=lambda p: abs(p[0] - pacman_pos[0]) + abs(p[1] - pacman_pos[1]))
                        current_path = uniform_cost(pacman_pos, target)
                        pathfinding_in_progress = False
                        if len(current_path) > 1:
                            pacman_pos = current_path[1] 
        if current_path and len(current_path) > 1:
            pacman_pos = current_path[1]  
            current_path = current_path[1:]
        screen.fill(BLACK)
        draw_grid()
        draw_pacman()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
