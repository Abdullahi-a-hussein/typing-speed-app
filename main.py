from random import choice
from tkinter import *

ONE_MINUTE = 60
FONT_NAME = "Courier"
BIG_FONT = 50
NORMAL_FONT = 24
MID_FONT = 34
AV_WORD_LENGHT = 5
CURRENT_WORD_TAG = "#C3FF99"
CORRECT_COLOR ="#3AB0FF"
WRONG_COLOR = "#F65A83"
BACKGROUND_COLOR = "#F5E8E4"
STARTED_TYPING = False
TYPED_WORDS = []
CORRECT_WORDS = []



def word_list():
    with open('words.txt') as words:
        words = [word.strip() for word in words.readlines()]
    return words

words = word_list()
selected = [choice(words) for _ in range(100)]
to_type = "  ".join(selected)
positions = [(0, len(selected[0]))]
for word in selected[1:]:
    starting = positions[-1][1] + 2
    ending = starting + len(word)
    positions.append((starting, ending))
    
INDEXED = 0


def timer(count):
    timer_label.config(text=f'Time Remaining: {count}')
    if count > 0:
        window.after(1000, timer, count - 1)
    else:
        clear()
        
        
def timer_call(event=None):
    global STARTED_TYPING
    if not STARTED_TYPING:
        timer(ONE_MINUTE)
        STARTED_TYPING = True

##------------------- UPDATE INPUT BOX WHEN PRESSED SPACE AND REFILL TEXT AREA WITH NEW TAG -------------------------- #
def update(event=None):
    global INDEXED, TYPED_WORDS, CORRECT_WORDS
    content = receiving_input.get()
    if content != " ":
        TYPED_WORDS.append(content.strip())
        CORRECT_WORDS.append(text.get(f'1.{positions[INDEXED][0]}', f'1.{positions[INDEXED][1]}'))
        if TYPED_WORDS[-1] == CORRECT_WORDS[-1]:
            text.tag_add("correct", f'1.{positions[INDEXED][0]}', f'1.{positions[INDEXED][1]}')
            text.tag_config("correct",foreground=CORRECT_COLOR)
        else: 
            text.tag_add("wrong", f'1.{positions[INDEXED][0]}', f'1.{positions[INDEXED][1]}')
            text.tag_config("wrong", foreground=WRONG_COLOR)
       
        receiving_input.delete(0, END)
        INDEXED += 1
        text.tag_delete('current')
        text.tag_add('current', f'1.{positions[INDEXED][0]}', f'1.{positions[INDEXED][1]}')
        text.tag_config('current', background=CURRENT_WORD_TAG)
        

def summary():
    global CORRECT_WORDS, TYPED_WORDS
    misstyped = []
    totla_characts = sum([len(word) for word in TYPED_WORDS])
    for typed, correct in zip(TYPED_WORDS, CORRECT_WORDS):
        if typed != correct:
            misstyped.append((typed, correct))
    return {'count': totla_characts, "incorrect": misstyped}
        
# ------------------------------------ Clear the Window and display Summary ---------------------------- #    
    
def clear():
    for widget in window.winfo_children():
        widget.destroy()
    
    result = summary()
    len_incorrect = sum([len(word[0]) for word in result['incorrect']])
    totals = result['count']
    
    total_label = Label(text=f"Your Total CPM is {totals}", font=(FONT_NAME, NORMAL_FONT), bg=BACKGROUND_COLOR, justify=['left'])
    total_label.grid(column=0, row=0)
    
    adjusted_label = Label(text=f"Your adjusted CPM is {totals - len_incorrect}", font=(FONT_NAME, NORMAL_FONT), bg=BACKGROUND_COLOR, justify=['right'])
    adjusted_label.grid(column=1, row=0)
    
    total_average = round(totals / 4.7, 1)
    adjusted_average = round((totals - len_incorrect) / 4.7, 1)
    
    total_average_label = Label(text=f"Average WPM: {total_average}", font=(FONT_NAME, MID_FONT, "bold"), bg=BACKGROUND_COLOR, justify=['left'])
    total_average_label.grid(column=0, row=1)
    
    adjusted_average_label = Label(text=f"Adjusted WPM: {adjusted_average}", font=(FONT_NAME, MID_FONT, 'bold'), bg=BACKGROUND_COLOR, justify=['right'])
    adjusted_average_label.grid(column=1, row=1)
    
    incorrect_words_title = Label(text="Incorrect Words", font=(FONT_NAME, MID_FONT), justify=['center'],underline=3, bg=BACKGROUND_COLOR)
    incorrect_words_title.grid(column=0, row=2, columnspan=2)
    incorrect_words = ""
    for word in result['incorrect']:
        incorrect_words += f"'{word[0]}' instead of '{word[1]}'\n"
    
    word_label = Label(text=incorrect_words, font=(FONT_NAME, NORMAL_FONT), justify=['center'], bg=BACKGROUND_COLOR)
    word_label.grid(column=0, row=3, columnspan=2)

# ------------------------------------- UI SETUP ------------------------ #
 
window = Tk()
window.title("Typing Speed App")
window.config(width=600, height=600, padx=50, pady=50, bg=BACKGROUND_COLOR)
window.geometry("880x700+800+300")

title_label = Label(text="Start Typing", font=(FONT_NAME, BIG_FONT, 'bold'), highlightthickness=0, fg='green', bg=BACKGROUND_COLOR)
title_label.grid(column=1, row=0)

text = Text(height=18, width=50, font=(FONT_NAME, NORMAL_FONT), wrap='word')
text.insert(INSERT, to_type)
text.tag_add('current', f'1.{positions[INDEXED][0]}', f'1.{positions[INDEXED][1]}')
text.tag_config('current', background=CURRENT_WORD_TAG)
text.grid(column=0, row=1, columnspan=2)

timer_label = Label(text="Remaining Time: 60",fg="#EC7272", bg='#F5E8E4', font=(FONT_NAME, 16))
timer_label.grid(column=0, row=0)


receiving_input =Entry(width=50, font=(FONT_NAME, NORMAL_FONT), justify=['center'])
receiving_input.grid(column=0, row=2, pady=10, columnspan=2)
receiving_input.focus()

# ------------------------------------ Binding keys to Functions --------------------- #
receiving_input.bind("<space>", update)
if not STARTED_TYPING:
    receiving_input.bind("<Key>", timer_call)


window.mainloop()


