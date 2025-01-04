def search_words(input_file, output_file, start_letter, word_length):
    try:
        with open(input_file, 'r') as infile:
            text = infile.read()

        # Split text into words
        words = text.split()

        # Find words matching criteria
        matching_words = [word for word in words if word.lower().startswith(start_letter.lower()) and len(word) == word_length]

        # Write matching words to the output file
        with open(output_file, 'w') as outfile:
            for word in matching_words:
                outfile.write(word + '\n')

        print(f"Matching words have been written to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # User input for file names and criteria
    input_file = input("Enter the name of the input text file: ")
    output_file = input("Enter the name of the filtered text file: ")
    start_letter = input("Enter the starting letter: ")
    word_length = int(input("Enter the word length: "))

    # Perform the search
    search_words(input_file, output_file, start_letter, word_length)