def word_letter_composition(file_path, min_leng, max_leng):
    # Initialize a dictionary to count the number of words containing each letter
    letter_word_counts = {letter: 0 for letter in "aąbcćdeęfghijklłmnńoópqrsśtuvwyzźż"}
    total_words = 0

    with open(file_path, "r", encoding="UTF-8") as file:
        for line in file:
            for word in line.split():
                # Remove punctuation and convert to lowercase
                clean_word = "".join(char for char in word if char.isalpha()).lower()
                if (
                    clean_word
                    and len(clean_word) >= min_leng
                    and len(clean_word) <= max_leng
                ):  # Only process non-empty words
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


def find_longest_word(file):
    longest_length = 0
    longest_word = ""
    with open(file, "r", encoding="UTF-8") as f:
        for line in f:
            words = line.split()
            for word in words:
                if len(word) > longest_length:
                    longest_length = len(word)
                    longest_word = word
    return longest_word


# Example usage:
file_path = "pruned_polish.txt"  # Replace with your file path
result = word_letter_composition(file_path, 1, 99)
for letter, probability in result:
    print(
        f"'{letter}': {probability:.2f}%    - 10 in {(1000/(0.000000000001+probability)):.0f}"
    )

longest_word = find_longest_word(file_path)
print(f"longest word is: {longest_word} and has {len(longest_word)} letters")
