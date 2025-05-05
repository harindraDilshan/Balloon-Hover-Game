import pygame
import numpy as np
import sys
import math

class BalloonHoverEnv:
    def __init__(self, render_mode = False):
        self.render_mode = render_mode
        # Constants
        self.WIDTH, self.HEIGHT = 400, 600 # Set the Window size to 400 pixels wide and 600 pixels tall.
        self.BALLOON_RADIUS = 20 # Radius of the balloon (used for drawing the circle).
        self.MIN_FAN_POWER = -2.0
        self.MAX_FAN_POWER = 2.0
        self.GRAVITY = -0.5 # Gravity always pull down.
        self.TIMESTEP = 0.1 # TODO : Explain
        self.HEIGHT_OF_FAN = 50
        self.THICKNESS_FLLOW = 40
        self.THICKNESS_CEILING = 40
        self.LOWER_BOUND =  self.HEIGHT - (self.HEIGHT_OF_FAN + self.THICKNESS_FLLOW)

        # Initialize PyGame
        if self.render_mode:
            pygame.init()
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption("Baloon Hover")
            self.clock = pygame.time.Clock()
        else:
            self.screen = None

        self.reset()

    def reset(self):
        self.balloon_y = self.HEIGHT // 2 # Place the balloon in the middel of the screen
        self.velocity = 0.0
        self.fan_power = 0.0
        self.done = False # makes the game as not over
        return self.get_state()
    
    def get_state(self):
        return np.array([self.balloon_y, self.velocity, self.fan_power], dtype=np.float32)
    
    def step(self, action):
        if action == 0: # decrease power
            self.fan_power -= 0.1 # decrease fan power by 0.1
        elif action == 2: # maintain power
            self.fan_power += 0.1

        self.fan_power = np.clip(self.fan_power, self.MIN_FAN_POWER, self.MAX_FAN_POWER) # This prevents the fan power from going below -2.0 or above 2.0.

        # physics
        acceleration = self.fan_power + self.GRAVITY
        self.velocity += acceleration * self.TIMESTEP # v = u + at in physics
        self.balloon_y -= self.velocity # TODO : explain

        # Check for Terminal State (Done Condition)
        if self.balloon_y < self.THICKNESS_CEILING or self.balloon_y > self.HEIGHT - (self.HEIGHT_OF_FAN + self.THICKNESS_FLLOW): # TODO change this
            reward = -10
            self.done = True

        else:
            reward = 1
        
        return self.get_state(), reward, self.done, {}

    def fan(self, screen):
        # Fan parameters
        center = (200, 200)
        radius = 100
        start_angle = math.radians(30)
        end_angle = math.radians(150)
        num_points = 50

        # Calculate fan points
        points = [center]
        for i in range(num_points + 1):
            angle = start_angle + (end_angle - start_angle) * i / num_points
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(screen, (0, 0, 255), points)
    
    def airFlow(self):
        # Parameters for airflow
        flow_lines = []
        for y in range(10, 100, 20):
            flow_lines.append(y)

        for line in flow_lines:
            # Draw sine wave line
            for x in range(self.THICKNESS_CEILING, self.HEIGHT - (self.HEIGHT_OF_FAN + self.THICKNESS_FLLOW), 5):
                dy = int(10 * math.sin((x) * 0.05))
                pygame.draw.circle(self.screen, (0, 100, 255), (line + self.WIDTH//2.7 + dy, x), 2)

    def render(self):
        self.screen.fill((0, 0, 0)) # Black background
        # pygame.draw.line(screen, color of the line RGB, starting point of the line, end point of the line, thickness)
        pygame.draw.line(self.screen, (0, 255, 0), (0, 4.0), (self.WIDTH, 4.0), self.THICKNESS_CEILING)  # ceiling
        pygame.draw.line(self.screen, (0, 0, 255), (0, self.HEIGHT), (self.WIDTH, self.HEIGHT), self.THICKNESS_FLLOW)  # floor

        # Display a fan
        triangle_points = [(self.WIDTH/2, self.HEIGHT), (self.WIDTH/2-self.HEIGHT_OF_FAN, self.HEIGHT - self.HEIGHT_OF_FAN), (self.WIDTH/2+self.HEIGHT_OF_FAN, self.HEIGHT - self.HEIGHT_OF_FAN)]  # (x, y) coordinates
        pygame.draw.polygon(self.screen, (255, 0, 0), triangle_points)

        # Display airflow
        self.airFlow()

        pygame.draw.circle(self.screen, (255, 0, 0), (self.WIDTH//2, int(self.balloon_y)), self.BALLOON_RADIUS) # Draw balloon

        # Display Fan power
        font = pygame.font.SysFont(None, 24)
        info = font.render(f"Fan: {self.fan_power:.2f} | Vel: {self.velocity:.2f}", True, (0, 0, 0))
        self.screen.blit(info, (10, 10))

        pygame.display.flip()
        self.clock.tick(60)

        
    def close(self):
        pygame.quit()