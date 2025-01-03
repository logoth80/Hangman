# # Open the input file for reading
# with open("polish a.txt", "r", encoding="UTF-8") as infile:
#     # Open the output file for writing
#     with open("pruned_polish_a.txt", "w", encoding="UTF-8") as outfile:
#         # Iterate over each line in the input file
#         for line in infile:
#             # Split the line into words based on semicolon (;)
#             words = line.split(";")
#             # Extract the first word (index 0) and convert it to lowercase
#             first_word = words[0]
#             # Write the lowercase word to the output file followed by a newline character
#             if not first_word.isupper() and len(first_word) >= 5:
#                 outfile.write(first_word + "\n")

# print("Processing complete. The pruned words have been saved to 'pruned_english.txt'.")
# Define the input and output file names
input_file1 = "polish_unique_a.txt"
input_file2 = "polish_unique_c.txt"
output_file = "pruned_polish.txt"

# Create an empty set to store unique lines
unique_lines = set()

# Open the first input file in read mode and add lines to the set
with open(input_file1, "r", encoding="utf-8") as infile:
    for line in infile:
        stripped_line = line.strip()
        if stripped_line:
            unique_lines.add(stripped_line)

# Open the second input file in read mode and add lines to the set
with open(input_file2, "r", encoding="utf-8") as infile:
    for line in infile:
        stripped_line = line.strip()
        if stripped_line:
            unique_lines.add(stripped_line)

# Sort the unique lines alphabetically
sorted_lines = sorted(unique_lines)

# Open the output file in write mode and write the sorted lines
with open(output_file, "w", encoding="utf-8") as outfile:
    for line in sorted_lines:
        outfile.write(line + "\n")

print(f"Merged dictionary has been saved to {output_file}")
