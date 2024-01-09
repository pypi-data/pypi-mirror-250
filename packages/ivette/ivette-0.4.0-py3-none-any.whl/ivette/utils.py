def print_color(text, color_code):
    """
    Function to print colored text using ANSI escape codes
    """
    print(f"\033[{color_code}m{text}\033[0m")