# Open the input file for reading
with open("polish a.txt", "r", encoding="UTF-8") as infile:
    # Open the output file for writing
    with open("pruned_polish_a.txt", "w", encoding="UTF-8") as outfile:
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
