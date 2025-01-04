import requests

def query_local_model(prompt, input_file, output_file):

    with open(input_file, 'r') as infile:
        text = infile.read()
    # Split text into words
    words = text.split()
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


if __name__ == "__main__":
    input_file = input("Enter the name of the filtered text file: ")
    output_file = input("Enter the name of the output text file: ")
    prompt = "Given the following list of words, sort them in order from least commonly used (most obscure) to most commonly used. Consider the frequency of the word's appearance in common usage, literature, or conversation. Provide the sorted list with one word per line. Only respond with the sorted list of words and do not say anything else."

    query_local_model(prompt=prompt, input_file=input_file, output_file=output_file)
