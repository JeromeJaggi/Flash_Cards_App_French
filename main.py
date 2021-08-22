from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    main_canvas.itemconfig(card_title, text="French", fill="black")
    main_canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    main_canvas.itemconfig(card_background, image=card_front_img)
    timer = window.after(3000, func=flip_card)


def flip_card():
    main_canvas.itemconfig(card_title, text="English", fill="white")
    main_canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    main_canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, func=flip_card)

main_canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = main_canvas.create_image(400, 263, image=card_front_img)
card_title = main_canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = main_canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
main_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
main_canvas.grid(row=0, column=0, columnspan=2)

wrong_icon = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_icon, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()



