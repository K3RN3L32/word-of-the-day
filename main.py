import requests
import pyautogui
import time

def query_local_model(prompt, words, output_file):

    # Combine the word list into the full prompt
    formatted_prompt = f"{prompt}\n\n" + "\n".join(words)

    # Endpoint for LM Studio
    url = "http://localhost:1234/v1/completions"

    # Request payload
    payload = {
        "model": "llama-3.2-3b-instruct",  # Replace with the model name if required
        "prompt": formatted_prompt,
        "max_tokens": 16384, # Adjust this according to your LLM and system RAM
        "temperature": 0.5
    }

    # Headers (JSON format)
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send the POST request
        response = requests.post(url, json=payload, headers=headers)

        # Check the response status
        if response.status_code == 200:
            result = response.json()
            raw_output = result['choices'][0]['text'].strip()
            print("Raw Output from LLM:")
            print(raw_output)

            sorted_words = []
            for word in raw_output.splitlines():
                word = word.strip()
                if word in matching_words:  # Retain only valid words
                    sorted_words.append(word)

            # Remove duplicates while preserving order
            sorted_words = list(dict.fromkeys(sorted_words))

            # Print and save the filtered words
            print("\nFiltered Sorted Words:")
            print("\n".join(sorted_words))

            # Write the result to the output file
            with open(output_file, 'w') as outfile:
                outfile.write("\n".join(sorted_words) + '\n')
            print(f"Sorted words written to {output_file}")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

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
    return matching_words

def type_words_from_file(file_path):
    # Open the file and read lines
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into words
            words = line.split()
            for word in words:
                time.sleep(3)
                # Type the word
                pyautogui.write(word)
                # Press Enter
                pyautogui.press('enter')
                # Wait for 15 seconds
                time.sleep(5)

if __name__ == "__main__":
    # User input for file names and criteria
    input_file = input("Enter the name of the input text file: ")
    output_file = input("Enter the name of the filtered text file: ")
    start_letter = input("Enter the starting letter: ")
    word_length = int(input("Enter the word length: "))
    result_file = input("Enter the name of the sorted text file: ")

    # Perform the search
    matching_words = search_words(input_file, output_file, start_letter, word_length)

    # Prompt
    prompt = "Given the following list of words, sort them in order from least commonly used (most obscure) to most commonly used. Consider the frequency of the word's appearance in common usage, literature, or conversation. Provide the sorted list with one word per line. Only respond with the sorted list of words and do not say anything else."

    # Query the local LM Studio model
    query_local_model(prompt=prompt, words=matching_words, output_file=result_file)

    user_input = input("Do you want to continue with typing the words from the file? (Y/N): ").strip().lower()
    if user_input == 'y':
        # Call the function to type words from the file
        type_words_from_file(result_file)
else:
    print("Operation canceled.")