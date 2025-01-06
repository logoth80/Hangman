import re


def find_words(has, hasnot):
    # Convert `has` to a set of required letters
    required_letters = set(has)
    # Convert `hasnot` to a set of disallowed letters
    disallowed_letters = set(hasnot)

    result_words = set()
    file_path = "pruned_polish.txt"

    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            for line in file:
                # Find all words in the line
                words = re.findall(r"\b\w+\b", line)

                for word in words:
                    word_lower = word.lower()
                    # Check if all required letters are in the word
                    if required_letters.issubset(set(word_lower)):
                        # Check if none of the disallowed letters are in the word
                        if not disallowed_letters.intersection(set(word_lower)):
                            print(word)
                            result_words.add(word_lower)
                        else:
                            continue
                            # print(f"Excluded due to disallowed letters: {word}")
                    else:
                        continue
                        # print(f"Excluded due to missing letters: {word}")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return result_words
