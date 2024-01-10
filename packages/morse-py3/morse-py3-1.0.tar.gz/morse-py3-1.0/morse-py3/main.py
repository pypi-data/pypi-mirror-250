morse_code = {
    'A': '.---',
    'B': '---.',
    'C': '.--- ---.',
    'D': '---..',
    'E': '.',
    'F': '..---.',
    'G': '.--- ---.---.',
    'H': '....',
    'I': '..',
    'J': '.--- --- ---',
    'K': '---.---',
    'L': '.---..',
    'M': '.--- ---',
    'N': '---.',
    'O': '--- --- ---',
    'P': '.--- ---.',
    'Q': '.---.---',
    'R': '.---.',
    'S': '...',
    'T': '---..---',
    'U': '..---',
    'V': '...---',
    'W': '.--- ---',
    'X': '---..---',
    'Y': '---.--- ---',
    'Z': '--- ---..',
    ' ': '    ',
    '!': '---.---.--- ---'
}


def text_to_morse(text):
    morse_string = ''
    text = text.upper()
    try:
        for char in text:
            if char == ' ':
                morse_string += morse_code[char]
            else:
                morse_string += morse_code[char] + '   '
        return morse_string.strip()
    except KeyError as e:
        return f"Sorry! We found the following key wasn't recognized: {e}"


# Example usage:
print(text_to_morse("Hello% World!"))
