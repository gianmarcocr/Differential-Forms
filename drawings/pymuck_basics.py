import pymunk
import pygame
import math

r1 = 30

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (400, 400)

# Create a window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption('Rotating Wheel')

# Create a space to simulate the wheel's movement
space = pymunk.Space()

# Set the gravitational acceleration
space.gravity = (0, 0)

# Create a body to represent the wheel
wheel_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 1))

# Set the wheel's initial position
wheel_body.position = (200, 200)

# Set the wheel's angular velocity
wheel_body.angular_velocity = 0.1

# Create a shape to represent the wheel
wheel_shape = pymunk.Circle(wheel_body, r1)

# Add the wheel to the space
space.add(wheel_body, wheel_shape)

# Set the simulation step size
dt = 1 / 60

# Run the simulation loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Step the simulation forward
    space.step(dt)

    # Calculate the position of the point on the edge of the wheel
    angle = wheel_body.angle
    x = wheel_body.position.x + r1 * math.cos(angle)
    y = wheel_body.position.y + r1 * math.sin(angle)

    # Create a transparent surface for the wheel
    wheel_surface = pygame.Surface((2, 2))
    wheel_surface.set_alpha(128)
    wheel_surface.set_colorkey((0, 0, 0))

    # Draw the wheel
    pygame.draw.circle(wheel_surface, (0, 0, 0), (1, 1), r1)

    # Draw the point
    pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 4)

    # Blit the wheel onto the screen
    screen.blit(wheel_surface, (int(wheel_body.position.x) - 1, int(wheel_body.position.y) - 1))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
