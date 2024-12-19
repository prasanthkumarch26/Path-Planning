import pygame
import numpy as np
from heapq import heappush, heappop

# Initialize pygame
pygame.init()

# Grid dimensions
GRID_WIDTH = 20
GRID_HEIGHT = 20
CELL_SIZE = 20

# Screen dimensions
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Draw on Grid with Start and Goal")

# Create a 2D array for the grid
grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)

# Start and Goal positions
start_pos = (0, 0)
goal_pos = (GRID_WIDTH - 1, GRID_HEIGHT - 1)

# Function to draw the grid and the cells
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            elif (x, y) == start_pos:
                pygame.draw.rect(screen, RED, rect)
            elif (x, y) == goal_pos:
                pygame.draw.rect(screen, GREEN, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)  # Grid lines

# Main loop
running = True
dragging_start = False
dragging_goal = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // CELL_SIZE
            grid_y = mouse_y // CELL_SIZE

            if (grid_x, grid_y) == start_pos:
                dragging_start = True
            elif (grid_x, grid_y) == goal_pos:
                dragging_goal = True
            elif 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                grid[grid_y][grid_x] = 1  # Draw on the grid

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_start = False
            dragging_goal = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging_start or dragging_goal:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE
                if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                    if dragging_start:
                        start_pos = (grid_x, grid_y)
                    elif dragging_goal:
                        goal_pos = (grid_x, grid_y)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grid
    draw_grid()

    # Update the display
    pygame.display.flip()

# Output the grid and the positions
print("Final Grid:")
print(grid)
print("Start Position:", start_pos)
print("Goal Position:", goal_pos)

# Quit pygame
pygame.quit()


# A* Pathfinding
def a_star(grid, start, goal):
    rows, cols = grid.shape
    open_set = []
    heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        _, current = heappop(open_set)
        
        if current == goal:
            return reconstruct_path(came_from, current)
        
        neighbors = get_neighbors(current, rows, cols)
        for neighbor in neighbors:
            if grid[neighbor] == 1:  # Skip obstacles
                continue
            
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))
    
    return None  # No path found

# Heuristic: Manhattan distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Get neighbors (4-directional movement)
def get_neighbors(node, rows, cols):
    x, y = node
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < rows and 0 <= ny < cols]

# Reconstruct path from 'came_from' dictionary
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


# Define start and goal positions
start = start_pos  # Starting grid cell
x, y = goal_pos   # Target grid cell
goal = (y, x)

# Run A*
path = a_star(grid, start, goal)

if path:
    print("Shortest Path:", path)
else:
    print("No path found!")



import matplotlib.pyplot as plt

def save_grid_as_image(grid, path=None, filename="path_planning.png"):
    plt.imshow(grid, cmap="gray")
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, color="red", linewidth=2)
    plt.title("Path Planning")
    plt.savefig(filename, dpi=300)  # Save the figure with high resolution
    plt.close()  # Close the figure to avoid showing it in interactive environments


# Example usage
save_grid_as_image(grid, path, filename="path_planning.png")
