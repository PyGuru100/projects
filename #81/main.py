MORSE_DICT = {'a': '.-',
              'b': '-...',
              'c': '-.-.',
              'd': '-..',
              'e': '.',
              'f': '..-.',
              'g': '--.',
              'h': '....',
              'i': '..',
              'j': '.---',
              'k': '-.-',
              'l': '.-..',
              'm': '--',
              'n': '-.',
              'o': '---',
              'p': '.--.',
              'q': '--.-',
              'r': '.-.',
              's': '...',
              't': '-',
              'u': '..-',
              'v': '...-',
              'w': '.--',
              'x': '-..-',
              'y': '-.--',
              'z': '--..',
              ' ': '/',
              '.': '.-.-.-',
              ',': '--..--',
              '?': '..--..',
              "'": '.----.',
              '!': '-.-.--',
              }
# accepts only lower case letters, spaces, and select symbols . , ? ' !


def valid_characters(string: str) -> bool:
    valid = True
    for char in string:
        if char not in MORSE_DICT:
            return not valid
    return valid


print("MORSE CODE CONVERTOR 3000. Give it a string containing alphanumeric characters"
      " or any of the following symbols . , ! ? ' ! \n and it'll return it in Morse Code.")
while True:
    user_string = input("Give a string and I'll give ye some Morse Code, or type quit: ").lower()
    if user_string == 'quit':
        quit()
    if not valid_characters(user_string):
        print('INVALID CHARACTER OR CHARACTERS. PLEASE TRY AGAIN.')
    else:
        print(' '.join([MORSE_DICT[char] for char in user_string]))
