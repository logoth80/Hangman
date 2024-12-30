import pygame
import random
import winsound
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (120, 120, 120)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Load font
big_font = pygame.font.Font(None, 80)
long_font = pygame.font.Font(None, 60)
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)
very_small_font = pygame.font.Font(None, 16)


# Read the dictionary from file
def read_dictionary(file_path):
    words = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) > 1:
                word = parts[0]
                description_parts = parts[1].split(",")
                if len(description_parts) > 1:
                    description = description_parts[1].strip()
                    words[word] = description
    return words


# Initialize game variables
dictionary = read_dictionary("Collins Scrabble Words (2019) with definitions.txt")
word_list = list(dictionary.keys())
current_word = random.choice(word_list)
guessed_letters = set()
wrong_guesses = 0
max_wrong_guesses = 10
running = True


# Function to reset the game
def reset_game():
    global current_word, guessed_letters, wrong_guesses
    current_word = random.choice(word_list)
    guessed_letters.clear()
    wrong_guesses = 0


# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            letter = event.unicode.upper()
            if letter not in guessed_letters:
                guessed_letters.add(letter)
                if letter not in current_word:
                    wrong_guesses += 1
                    winsound.Beep(400, 200)
            if event.key == pygame.K_F5:  # Restart game with F5 key
                reset_game()
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    # Clear the screen
    screen.fill(WHITE)
    text_surface = very_small_font.render("F5 to restart, ESC to quit", True, GREY)
    screen.blit(text_surface, (600, 15))
    # Draw the word with underscores for unguessed letters
    displayed_word = "".join(
        [letter if letter in guessed_letters else "_" for letter in current_word]
    )
    # text_surface = big_font.render(displayed_word, True, BLACK)
    # screen.blit(text_surface, (WIDTH // 1.5 - text_surface.get_width() // 2, HEIGHT // 2 - 100))
    word_length = len(displayed_word)
    for l in range(0, word_length):
        l_x = 0
        if displayed_word[l] == "I":
            l_x = 3
        if displayed_word[l] == "L":
            l_x = 1
        if len(displayed_word) < 10:
            word_width = word_length * 50
            text_surface = big_font.render(displayed_word[l], True, BLACK)
            screen.blit(
                text_surface,
                (l_x * 4 + WIDTH - (word_width // 9) - (word_length - l) * 50, 200),
            )
        elif len(displayed_word) <= 12:
            word_width = word_length * 40
            text_surface = long_font.render(displayed_word[l], True, BLACK)
            screen.blit(
                text_surface,
                (
                    l_x * 3 + WIDTH - (word_width // 9) - (word_length - l) * 40,
                    200,
                ),
            )
        else:
            word_width = word_length * 30
            text_surface = font.render(displayed_word[l], True, BLACK)
            screen.blit(
                text_surface,
                (l_x * 2 + WIDTH - (word_width // 9) - (word_length - l) * 30, 200),
            )

    # Draw the hangman on the left side
    if wrong_guesses >= 1:
        pygame.draw.line(screen, BLACK, (10, 380), (190, 380), 5)
    if wrong_guesses >= 2:
        pygame.draw.line(screen, BLACK, (100, 30), (100, 380), 5)
    if wrong_guesses >= 3:
        pygame.draw.line(screen, BLACK, (200, 30), (100, 30), 5)
    if wrong_guesses >= 4:
        pygame.draw.line(screen, BLACK, (200, 30), (200, 80), 5)
    if wrong_guesses >= 5:
        pygame.draw.circle(screen, BLACK, (200, 105), 25, 5)
    if wrong_guesses >= 6:
        pygame.draw.line(screen, BLACK, (200, 130), (200, 250), 5)
    if wrong_guesses >= 7:
        pygame.draw.line(screen, BLACK, (200, 150), (170, 230), 5)
    if wrong_guesses >= 8:
        pygame.draw.line(screen, BLACK, (200, 150), (230, 230), 5)
    if wrong_guesses >= 9:
        pygame.draw.line(screen, BLACK, (200, 250), (170, 330), 5)
    if wrong_guesses >= 10:
        pygame.draw.line(screen, BLACK, (200, 250), (230, 330), 5)

    # Display used letters
    used_letters_text = " ".join(sorted(guessed_letters))
    text_surface = small_font.render(used_letters_text, True, BLACK)
    screen.blit(
        text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 150)
    )

    # Check for win/loss
    if "_" not in displayed_word:
        text_surface = font.render(f"Congratulations! You won!", True, GREEN)
        screen.blit(
            text_surface,
            (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 200),
        )
        description = dictionary[current_word]
        text_surface = small_font.render(description, True, BLACK)
        screen.blit(
            text_surface,
            (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 250),
        )
    elif wrong_guesses == max_wrong_guesses:
        text_surface = font.render(
            f"Game Over! The word was {current_word}.", True, RED
        )
        screen.blit(
            text_surface,
            (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 200),
        )
        description = dictionary[current_word]
        text_surface = small_font.render(description, True, BLACK)
        screen.blit(
            text_surface,
            (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 250),
        )

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
