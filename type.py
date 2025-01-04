import pyautogui
import time

paused = False

def type_words_from_files(files, num_words):
    global paused
    # Open all files and read lines
    file_lines = [open(f, 'r').readlines() for f in files]

    # Get the longest length to avoid index errors
    max_length = max(len(lines) for lines in file_lines)

    for i in range(max_length):
        if paused:
            print("Paused. Press 'r' to resume.")
            while paused:
                time.sleep(1)

        combined_words = " ".join(
            [lines[i].strip() if i < len(lines) else '' for lines in file_lines[:num_words]]
        ).strip()

        if combined_words:
            time.sleep(3)
            pyautogui.write(combined_words)
            pyautogui.press('enter')
            time.sleep(15)

if __name__ == "__main__":
    num_words = int(input("How many words do you want to type (1 to 5)? ").strip())
    num_words = max(1, min(num_words, 5))

    files = []
    for i in range(num_words):
        files.append(input(f"Enter the name of text file {i+1}: "))
    
    user_input = input("Do you want to continue with typing the words from the files? (Y/N): ").strip().lower()
    if user_input == 'y':
        print("Press 'p' to pause and 'r' to resume during typing.")

        from threading import Thread
        import keyboard

        def pause_resume_listener():
            global paused
            while True:
                if keyboard.is_pressed('p'):
                    if not paused:
                        print("Paused")
                    paused = True
                if keyboard.is_pressed('r'):
                    if paused:
                        print("Resumed")
                    paused = False

        listener_thread = Thread(target=pause_resume_listener, daemon=True)
        listener_thread.start()
        
        # Call the function to type words from the files
        type_words_from_files(files, num_words)
    else:
        print("Operation canceled.")
