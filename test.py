import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Flow Simulation")

clock = pygame.time.Clock()

# Parameters for airflow
flow_lines = []
for y in range(50, HEIGHT, 50):
    flow_lines.append({
        "y": y,
        "offset": 0
    })

# Main loop
running = True
while running:
    screen.fill((255, 255, 255))  # white background

    for line in flow_lines:
        y = line["y"]
        offset = line["offset"]
        # Draw sine wave line
        for x in range(0, WIDTH, 5):
            dy = int(10 * math.sin((x + offset) * 0.05))
            pygame.draw.circle(screen, (0, 100, 255), (x, y + dy), 2)

        line["offset"] += 2  # animate the wave

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
