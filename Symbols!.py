import unicodedataplus as ud
import time

print("Python script loaded and ready!")
print("What to type except characters:")
print("Exit - exits")
print("Shortest - shows you the shortest character name info")
print("Longest - shows you the longest character name info")
print("U+XXXX - shows info for that Unicode codepoint")

def get_char_info(char):
    """Return info about a single Unicode character."""
    codepoint = f"U+{ord(char):04X}"
    try:
        name = ud.name(char)
    except ValueError:
        name = "No official Unicode name"
    age_info = ud.age(char)
    version = f"{age_info[0]}.{age_info[1]}" if age_info else "Unknown"
    return char, name, codepoint, version

def find_extreme_name(longest=True):
    """Find the character with the longest or shortest name."""
    extreme_length = 0 if longest else float('inf')
    extreme_char = None
    extreme_name = None
    extreme_codepoint = None
    extreme_version = None

    for codepoint in range(0x110000):
        char = chr(codepoint)
        try:
            name = ud.name(char)
            age_info = ud.age(char)
            version = f"{age_info[0]}.{age_info[1]}" if age_info else "Unknown"
            name_length = len(name)

            if (longest and name_length > extreme_length) or (not longest and name_length < extreme_length):
                extreme_length = name_length
                extreme_char = char
                extreme_name = name
                extreme_codepoint = f"U+{codepoint:04X}"
                extreme_version = version
        except ValueError:
            continue
    return extreme_char, extreme_name, extreme_codepoint, extreme_version, extreme_length

# Main input loop
while True:
    user_input = input("Type a character: ").strip()

    # Convert input to lowercase for commands
    lower_input = user_input.lower()

    if lower_input == "exit":
        # Animated exit
        print("Exiting")
        dots = [".", "..", "..."]
        frame_time = 0.5
        total_duration = 3
        elapsed = 0
        while elapsed < total_duration:
            for d in dots:
                print(f"\r{d}   ", end="", flush=True)
                time.sleep(frame_time)
                elapsed += frame_time
                if elapsed >= total_duration:
                    break
        print("\nExited!")
        break

    if lower_input == "longest":
        char, name, codepoint, version, length = find_extreme_name(longest=True)
        print(f"Longest Unicode character name in your Python version:")
        print(f"Symbol: {char}")
        print(f"Name: {name}")
        print(f"Codepoint: {codepoint}")
        print(f"Unicode version: {version}")
        print(f"Length: {length} characters\n")
        continue

    if lower_input == "shortest":
        char, name, codepoint, version, length = find_extreme_name(longest=False)
        print(f"Shortest Unicode character name in your Python version:")
        print(f"Symbol: {char}")
        print(f"Name: {name}")
        print(f"Codepoint: {codepoint}")
        print(f"Unicode version: {version}")
        print(f"Length: {length} characters\n")
        continue

    # Check for codepoint input like U+25C8
    if user_input.upper().startswith("U+"):
        try:
            code_hex = user_input[2:]
            code_int = int(code_hex, 16)
            if 0 <= code_int <= 0x10FFFF:
                char = chr(code_int)
                char, name, codepoint, version = get_char_info(char)
                print(f"Symbol: {char}, Name: {name}, Codepoint: {codepoint}, Unicode version: {version}\n")
                continue
            else:
                print("Invalid codepoint. Must be between U+0000 and U+10FFFF.\n")
                continue
        except ValueError:
            print("Invalid codepoint format. Use U+XXXX.\n")
            continue

    # Single character input
    if len(user_input) != 1:
        print("Please type exactly ONE character, or 'longest'/'shortest', or a codepoint like U+XXXX.\n")
        continue

    char, name, codepoint, version = get_char_info(user_input)
    print(f"Symbol: {char}, Name: {name}, Codepoint: {codepoint}, Unicode version: {version}\n")
