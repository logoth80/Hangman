def word_letter_composition(file_path):
    # Initialize a dictionary to count the number of words containing each letter
    letter_word_counts = {letter: 0 for letter in "aąbcćdeęfghijklłmnńoópqrsśtuvwyzźż"}
    total_words = 0

    with open(file_path, "r", encoding="UTF-8") as file:
        for line in file:
            for word in line.split():
                # Remove punctuation and convert to lowercase
                clean_word = "".join(char for char in word if char.isalpha()).lower()
                if clean_word:  # Only process non-empty words
                    total_words += 1
                    # Check which letters are present in the word
                    unique_letters = set(clean_word)
                    for letter in unique_letters:
                        if letter in letter_word_counts:
                            letter_word_counts[letter] += 1

    # Calculate percentages
    letter_probabilities = {
        letter: (count / total_words * 100) if total_words > 0 else 0
        for letter, count in letter_word_counts.items()
    }

    # Sort by probabilities in descending order
    sorted_probabilities = sorted(
        letter_probabilities.items(), key=lambda item: item[1], reverse=True
    )

    return sorted_probabilities


# Example usage:
file_path = "pruned_polish.txt"  # Replace with your file path
result = word_letter_composition(file_path)
for letter, probability in result:
    print(f"'{letter}': {probability:.2f}%    - 1 in {(100/(probability)):.0f}")
