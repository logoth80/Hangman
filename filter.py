# Open the input file and read its content
with open("english.txt", "r") as file:
    lines = file.readlines()

# Process each line
processed_words = []
for line in lines:
    # Split the line into words
    words = line.split()

    # Take only the first word and convert it to lowercase
    if words:  # Ensure the line is not empty
        processed_word = words[0].lower()
        if len(processed_word) > 4:
            processed_words.append(processed_word)

# Write the processed words to the output file
with open("pruned_english.txt", "w") as file:
    for word in processed_words:
        file.write(word + "\n")

print("Processing complete. The pruned words have been saved to pruned_english.txt")

# Open the input file for reading
with open("polish.txt", "r", encoding="UTF-8") as infile:
    # Open the output file for writing
    with open("pruned_polish.txt", "w", encoding="UTF-8") as outfile:
        # Iterate over each line in the input file
        for line in infile:
            # Split the line into words based on semicolon (;)
            words = line.split(";")
            # Extract the first word (index 0) and convert it to lowercase
            first_word = words[0]
            # Write the lowercase word to the output file followed by a newline character
            if not first_word.isupper() and len(first_word) >= 5:
                outfile.write(first_word + "\n")

print("Processing complete. The pruned words have been saved to 'pruned_english.txt'.")
