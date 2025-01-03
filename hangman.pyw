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


def load_color_theme(t):
    global hangman_color, loss_color, letter_color, bg_color, theme
    if t == 2:
        # color theme2
        hangman_color = (12, 13, 13)
        loss_color = (254, 66, 63)
        letter_color = (2, 163, 136)
        bg_color = (220, 225, 225)
    elif t == 3:
        # color theme3
        hangman_color = (162, 110, 234)
        loss_color = (70, 183, 253)
        letter_color = (93, 112, 234)
        bg_color = (247, 175, 255)
    elif t == 4:
        # color theme4
        hangman_color = (104, 0, 33)
        loss_color = (147, 149, 152)
        letter_color = (0, 0, 0)
        bg_color = (255, 250, 236)
    elif t == 5:
        # color theme5
        hangman_color = (255, 250, 236)
        loss_color = (147, 149, 152)
        letter_color = (104, 0, 33)
        bg_color = (0, 0, 0)
    else:
        theme = 1
        # color theme1
        hangman_color = (0, 104, 132)
        loss_color = (250, 157, 0)
        letter_color = (0, 104, 132)
        bg_color = (255, 208, 141)


# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Load font
big_font = pygame.font.Font(None, 80)
long_font = pygame.font.Font(None, 60)
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)
very_small_font = pygame.font.Font(None, 16)


def load_dictionary(dictionary_selected):
    # Read the dictionary from file
    word_list = []

    if dictionary_selected == "polish":
        dictionary_file = "pruned_polish.txt"
    elif dictionary_selected == "english":
        dictionary_file = "pruned_english.txt"
    else:
        dictionary_file = "pruned_polish.txt"

    with open(dictionary_file, "r", encoding="UTF-8") as file:
        for line in file:
            # Split the line by ';'
            parts = line.strip().split(";")

            if len(parts) >= 0:
                word = parts[0]

                # Check if the word is not capitalized and has at least 5 letters
                if not word.isupper() and len(word) >= 5:
                    word_list.append(word)
    return word_list


# Initialize game variables
selected_language = "polish"
word_list = load_dictionary("polish")
current_word = random.choice(word_list)
guessed_letters = set()
guessed_letters.clear()
wrong_guesses = 0
max_wrong_guesses = 10
running = True
game_over = False
theme = 5
load_color_theme(theme)


# Function to reset the game
def reset_game():
    global current_word, guessed_letters, wrong_guesses, game_over
    current_word = random.choice(word_list)
    guessed_letters.clear()
    wrong_guesses = 0
    game_over = False


def change_theme():
    global theme
    theme += 1
    load_color_theme(theme)


# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            letter = event.unicode.lower()
            # letter = pygame.key.name(event.key).lower()
            if (
                letter not in guessed_letters
                and not game_over
                and letter in "aąbcćdeęfghijklłmnńoópqrstuvwxyzżź"
            ):
                guessed_letters.add(letter)
                if letter not in current_word:
                    wrong_guesses += 1
                    winsound.Beep(400, 200)
            if event.key == pygame.K_F2:
                if selected_language == "english":
                    selected_language = "polish"
                elif selected_language == "polish":
                    selected_language = "english"
                word_list = load_dictionary(selected_language)
                reset_game()
            if event.key == pygame.K_F3:
                change_theme()
            if event.key == pygame.K_F5:  # Restart game with F5 key
                reset_game()
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    # Clear the screen
    screen.fill(bg_color)
    text_surface = very_small_font.render(
        "F3 to recolor, F5 to restart, ESC to quit",
        True,
        loss_color,
    )
    screen.blit(text_surface, (WIDTH - 220, 15))

    text_surface = very_small_font.render(
        f"F2  {selected_language}",
        True,
        hangman_color,
    )
    screen.blit(text_surface, (WIDTH // 2, 15))

    # Draw the word with underscores for unguessed letters
    displayed_word = "".join(
        [letter if letter in guessed_letters else "_" for letter in current_word]
    )

    word_length = len(displayed_word)
    for placed_letter in range(0, word_length):
        if len(displayed_word) < 10:
            size_multiplier = 50
        elif len(displayed_word) <= 12:
            size_multiplier = 40
        else:
            size_multiplier = 30

        word_width = word_length * size_multiplier
        if size_multiplier > 30:
            text_surface = big_font.render(
                displayed_word[placed_letter], True, letter_color
            )
            screen.blit(
                text_surface,
                (
                    -text_surface.get_width() // 2
                    + WIDTH
                    - (word_length - placed_letter) * size_multiplier,
                    200,
                ),
            )
        elif size_multiplier <= 30:
            text_surface = font.render(
                displayed_word[placed_letter], True, letter_color
            )
            screen.blit(
                text_surface,
                (
                    -text_surface.get_width() // 2
                    + WIDTH
                    - (word_length - placed_letter) * size_multiplier,
                    200,
                ),
            )
    # Draw the hangman on the left side
    if wrong_guesses >= 1:
        pygame.draw.line(screen, hangman_color, (10, 380), (190, 380), 5)
    if wrong_guesses >= 2:
        pygame.draw.line(screen, hangman_color, (100, 30), (100, 380), 5)
    if wrong_guesses >= 3:
        pygame.draw.line(screen, hangman_color, (200, 30), (100, 30), 5)
    if wrong_guesses >= 4:
        pygame.draw.line(screen, hangman_color, (200, 30), (200, 80), 5)
    if wrong_guesses >= 5:
        pygame.draw.circle(screen, hangman_color, (200, 105), 25, 5)
    if wrong_guesses >= 6:
        pygame.draw.line(screen, hangman_color, (200, 130), (200, 250), 5)
    if wrong_guesses >= 7:
        pygame.draw.line(screen, hangman_color, (200, 150), (170, 230), 5)
    if wrong_guesses >= 8:
        pygame.draw.line(screen, hangman_color, (200, 150), (230, 230), 5)
    if wrong_guesses >= 9:
        pygame.draw.line(screen, hangman_color, (200, 250), (170, 330), 5)
    if wrong_guesses >= 10:
        pygame.draw.line(screen, hangman_color, (200, 250), (230, 330), 5)

    # Display used letters
    used_letters_text = " ".join(sorted(guessed_letters))
    text_surface = small_font.render(used_letters_text, True, letter_color)
    screen.blit(
        text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 150)
    )

    # Check for win/loss
    if "_" not in displayed_word:
        game_over = True
        text_surface = font.render("Congratulations! You won!", True, loss_color)
        screen.blit(
            text_surface,
            (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 200),
        )
    elif wrong_guesses == max_wrong_guesses:
        game_over = True
        text_surface = font.render(
            f"Game Over! The word was {current_word}.", True, RED
        )
        screen.blit(
            text_surface,
            (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 200),
        )

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
