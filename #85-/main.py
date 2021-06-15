import tkinter as tk
from english_words import english_words_set
import random


master_list = [word for word in english_words_set]


def generate_list():
    words_list = []
    while len(words_list) < 300:
        new_word = random.choice(master_list)
        if new_word not in words_list and len(new_word) <= 7:
            words_list.append(new_word)
    return words_list


window = tk.Tk()
window.title('Typist Be Ye?')
window.geometry('300x300')

counter = 0
correct_words = 0
list_of_words = generate_list()

display_words = tk.Label(window, text=list_of_words[counter: counter+5])
entry = tk.Entry(window)
entry.pack()


# I need a useless input variable because Tkinter for some reason feeds something into
# the gosh-darn function when I use the bind function.
# noinspection PyUnusedLocal
def update(useless=None):
    global counter, correct_words, list_of_words
    user_input = entry.get()
    if list_of_words[counter] == user_input.split()[-1]:
        correct_words += 1
    counter += 1
    display_words['text'] = list_of_words[counter: counter+5]
    print(f"Counter: {counter}")
    print(f"Correct: {correct_words}")
    print("*" * 15)


entry.bind(sequence='<space>', func=update)
display_words.pack()
window.mainloop()
