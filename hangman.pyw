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


# onexit function
def onexit():
    pygame.quit()
    sys.exit(0)


def read_saved(key, filename="saved.txt"):
    try:
        with open(filename, "r", encoding="UTF-8") as file:
            for line in file:
                if line.strip():
                    k, v = line.split("=", 1)
                    if k.strip() == key:
                        return eval(v.strip())  # Safely interpret the value
    except FileNotFoundError:
        with open(filename, "w", encoding="UTF-8") as file:
            lines = []
            lines.append("highscore=0\n")
            lines.append("theme=1\n")
            lines.append('language="english"\n')
            lines.append("wrong_guesses=0\n")
            lines.append("score=0\n")
            lines.append("guessed_letters=set()\n")
            lines.append("correct_letters=set()\n")
            lines.append("current_word='helicopter'\n")

            file.writelines(lines)

        with open(filename, "r", encoding="UTF-8") as file:
            for line in file:
                if line.strip():
                    k, v = line.split("=", 1)
                    if k.strip() == key:
                        return eval(v.strip())  # Safely interpret the value

    return None


def write_saved(key, value, filename="saved.txt"):
    lines = []
    found = False
    try:
        with open(filename, "r", encoding="UTF-8") as file:
            for line in file:
                if line.strip():
                    k, v = line.split("=", 1)
                    if k.strip() == key:
                        lines.append(f"{key}={repr(value)}\n")
                        found = True
                    else:
                        lines.append(line)
    except FileNotFoundError:
        pass

    if not found:
        lines.append(f"{key}={repr(value)}\n")

    with open(filename, "w", encoding="UTF-8") as file:
        file.writelines(lines)


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
    elif t == 6:
        # color theme6
        hangman_color = (200, 200, 200)
        loss_color = (247, 149, 152)
        letter_color = (220, 220, 220)
        bg_color = (0, 50, 65)
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
fps_target = 24

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

                # Check if the word is not capitalized and has 5-18 charactersa
                if not word.isupper() and len(word) >= 5 and len(word) <= 18:
                    word_list.append(word)
    return word_list


# Initialize game variables
# selected_language = "polish"  #          DEFAULT LANGUAGE
selected_language = read_saved("language")
word_list = load_dictionary(selected_language)
current_word = random.choice(word_list)
current_word = read_saved("current_word")
empty_guessed_letters = set()
guessed_letters = set()
correct_letters = set()
correct_letters = read_saved("correct_letters")
guessed_letters = read_saved("guessed_letters")
wrong_guesses = 0
wrong_guesses = read_saved("wrong_guesses")
max_wrong_guesses = 10
running = True
game_over = False
show_score = False
score = 0
if wrong_guesses < max_wrong_guesses:
    score = read_saved("score")
theme = read_saved("theme")
highscore = read_saved("highscore")

load_color_theme(theme)


# Function to reset the game
def reset_game():
    global \
        current_word, \
        guessed_letters, \
        correct_letters, \
        wrong_guesses, \
        game_over, \
        score, \
        highscore
    if not game_over and wrong_guesses > 0:
        score = 0
        write_saved("score", score)
    elif game_over and wrong_guesses >= max_wrong_guesses:
        score = 0
        write_saved("score", score)
        write_saved("correct_letters", empty_guessed_letters)
        write_saved("guessed_letters", empty_guessed_letters)
        temp_word = random.choice(word_list)
        write_saved("current_word", temp_word)
    elif game_over and wrong_guesses < max_wrong_guesses:
        score = score - wrong_guesses + 45 - 2 * len(current_word)
        write_saved("score", score)
        if score > highscore:
            highscore = score
            write_saved("highscore", highscore)
    wrong_guesses = 0
    write_saved("wrong_guesses", wrong_guesses)
    game_over = False
    current_word = random.choice(word_list)
    write_saved("current_word", current_word)
    guessed_letters.clear()
    correct_letters.clear()
    write_saved("guessed_letters", guessed_letters)
    write_saved("correct_letters", correct_letters)


def next_theme():
    global theme
    theme += 1
    load_color_theme(theme)
    write_saved("theme", theme)


clock = pygame.time.Clock()
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
                and letter in "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź"
            ):
                guessed_letters.add(letter)
                write_saved("guessed_letters", guessed_letters)
                if letter in current_word and len(letter) == 1:
                    score += 1
                    correct_letters.add(letter)
                    write_saved("correct_letters", correct_letters)
                    write_saved("score", score)
                    if score > highscore:
                        highscore = score
                        write_saved("highscore", highscore)
                if letter not in current_word:
                    wrong_guesses += 1
                    write_saved("wrong_guesses", wrong_guesses)
                    winsound.Beep(400, 200)
                    if wrong_guesses >= max_wrong_guesses:
                        show_score = True
            if event.key == pygame.K_F2:
                if selected_language == "english":
                    selected_language = "polish"
                    write_saved("language", selected_language)
                elif selected_language == "polish":
                    selected_language = "english"
                    write_saved("language", selected_language)
                word_list = load_dictionary(selected_language)
                reset_game()
            if event.key == pygame.K_F3:
                next_theme()
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

    if score == highscore:
        tempcolor = RED
    else:
        tempcolor = hangman_color

    text_surface = small_font.render(
        f"score: {score}",
        True,
        tempcolor,
    )
    screen.blit(
        text_surface,
        (WIDTH - 5 - text_surface.get_width(), HEIGHT - 5 - text_surface.get_height()),
    )

    text_surface = very_small_font.render(
        f"high score: {highscore}",
        True,
        hangman_color,
    )
    screen.blit(
        text_surface,
        (
            WIDTH - 160 - text_surface.get_width(),
            HEIGHT - 5 - text_surface.get_height(),
        ),
    )

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
        pygame.draw.line(screen, hangman_color, (10, 370), (190, 370), 5)
    if wrong_guesses >= 2:
        pygame.draw.line(screen, hangman_color, (100, 60), (100, 370), 5)
    if wrong_guesses >= 3:
        pygame.draw.line(screen, hangman_color, (200, 60), (100, 60), 5)
    if wrong_guesses >= 4:
        pygame.draw.line(screen, hangman_color, (200, 60), (200, 110), 5)
    if wrong_guesses >= 5:
        pygame.draw.circle(screen, hangman_color, (200, 135), 25, 5)
    if wrong_guesses >= 6:
        pygame.draw.line(screen, hangman_color, (200, 160), (200, 230), 5)
    if wrong_guesses >= 7:
        pygame.draw.line(screen, hangman_color, (200, 170), (170, 230), 5)
    if wrong_guesses >= 8:
        pygame.draw.line(screen, hangman_color, (200, 170), (230, 230), 5)
    if wrong_guesses >= 9:
        pygame.draw.line(screen, hangman_color, (200, 230), (170, 310), 5)
    if wrong_guesses >= 10:
        pygame.draw.line(screen, hangman_color, (200, 230), (230, 310), 5)

    # Display used letters
    used_letters_text = " ".join(sorted(guessed_letters))

    # capitalie correct
    def capitalize_selected(string, letter_set):
        return "".join(char.upper() if char in letter_set else char for char in string)

    # used_letters_text = capitalize_selected(used_letters_text, correct_letters)

    text_surface = small_font.render(used_letters_text, True, letter_color)
    screen.blit(
        text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 150)
    )

    # Check for win/loss
    if "_" not in displayed_word:
        if not game_over:
            write_saved("score", score)
        game_over = True
        text_surface = font.render("Great! F5 to continue!", True, loss_color)
        screen.blit(
            text_surface,
            (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 200),
        )
        text_surface = font.render(
            f"Your score: {score-wrong_guesses+45-2*len(current_word)}",
            True,
            loss_color,
        )
        screen.blit(
            text_surface,
            (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 260),
        )
    elif wrong_guesses == max_wrong_guesses:
        if not game_over:
            write_saved("score", 0)
        game_over = True
        text_surface = font.render(
            f"Game Over! The word was {current_word}.", True, loss_color
        )
        screen.blit(
            text_surface,
            (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 200),
        )
        if show_score:
            text_surface = font.render(f"Your score: {score}", True, loss_color)
            screen.blit(
                text_surface,
                (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 260),
            )

    # Update the display
    pygame.display.flip()
    clock.tick(fps_target)
# Quit Pygame
pygame.quit()
