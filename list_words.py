import re


def find_words(has, hasnot, length):
    # Convert `has` to a set of required letters
    # required_letters = has
    # Convert `hasnot` to a set of disallowed letters
    temphas = has.replace("_", ".")
    print(f"checking <{temphas}> and without {hasnot} with length {length}")
    disallowed_letters = set(hasnot)

    result_words = set()
    file_path = "pruned_polish.txt"
    if length == 0:
        length = len(has)

    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            for line in file:
                # Find all words in the line
                words = re.findall(r"\b\w+\b", line)

                for word in words:
                    word_lower = word.lower()
                    # Check if all required letters are in the word
                    # if len(word) == length and required_letters.issubset(set(word_lower)):
                    if re.findall(temphas, word_lower) and len(word) == length:
                        # Check if none of the disallowed letters are in the word
                        if not disallowed_letters.intersection(set(word_lower)):
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


has = input("Enter the required letters (e.g., 'p.ciąg..y): ")
hasnot = input("Enter the disallowed letters (e.g., 'xjuz'): ")
length = int(input("Enter the word length: ") or "0")
print(find_words(has, hasnot, length))
input()
