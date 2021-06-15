from english_words import english_words_set
from random import choice
from time import time

english_words = [word for word in english_words_set]
start = time()
words, correct_words = 0, 0
print('You have 60 seconds to type as many of these words as possible: ')
print('You should only type the first word in the sequence.')
words_list = [choice(english_words) for i in range(300)]
while time() <= start + 60:
    print(words_list[words: words+5])
    current_word = words_list[words]
    user_input = input('Type: ')
    words += 1
    if user_input == current_word:
        correct_words += 1

print(f"Okay so typing speed: {words}/per minute "
      f"and accuracy: {100 * correct_words/words}%")
