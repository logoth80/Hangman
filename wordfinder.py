import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Pygame Button Example")

# Define button colors and dimensions
button_color = (255, 165, 0)
button_x = 150
button_y = 100
button_width = 100
button_height = 50

# Define font for button text
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                button_x <= mouse_x <= button_x + button_width
                and button_y <= mouse_y <= button_y + button_height
            ):
                print("Button clicked!")

    # Draw everything
    screen.fill((255, 255, 255))
    pygame.draw.rect(
        screen, button_color, (button_x, button_y, button_width, button_height)
    )
    text = font.render("Click Me", True, (0, 0, 0))
    screen.blit(
        text,
        (
            button_x + button_width // 2 - text.get_width() // 2,
            button_y + button_height // 2 - text.get_height() // 2,
        ),
    )

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
