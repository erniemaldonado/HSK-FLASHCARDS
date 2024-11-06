import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random

class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class FlashcardApp:
    def __init__(self, master, csv_file):
        self.master = master
        self.master.title("HSK 4 App")
        self.master.geometry("800x600")
        self.indexes=[]

        # Container Frame for Centering
        self.container = tk.Frame(master)
        self.container.pack(expand=True)  # Center the container vertically

        # Load flashcards
        self.flashcards = self.load_flashcards(csv_file)
        self.current_card = None
        self.showing_answer = False

        # Track displayed indices
        self.displayed_indices = set()
        self.index = -1  # Start with no card displayed
        self.iterator = 0
        self.new_card = False


        # Bind arrow keys to functions
        self.master.bind("<Right>", lambda event: self.next_flashcard())
        self.master.bind("<d>", lambda event: self.next_flashcard())

        self.master.bind("<Left>", lambda event: self.prev_flashcard())
        self.master.bind("<a>", lambda event: self.prev_flashcard())

        self.master.bind("<Up>", lambda event: self.show_answer())
        self.master.bind("<w>", lambda event: self.show_answer())

        self.master.bind("<Down>", lambda event: self.hide_answer())
        self.master.bind("<s>", lambda event: self.hide_answer())


        # GUI Components
        self.question_label = tk.Label(self.container, text="", wraplength=350, font=("SimHei", 40))
        self.question_label.pack(pady=20)

        self.answer_label = tk.Label(self.container, text="", wraplength=350, font=("Arial", 14), fg="blue")
        self.answer_label.pack(pady=20)

        # Frame for Buttons
        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=10)

        self.show_answer_button = tk.Button(button_frame, text="Show Answer", command=self.show_answer)
        self.show_answer_button.grid(row=0, column=0, padx=10)

        self.next_button = tk.Button(button_frame, text="Next", command=self.next_flashcard)
        self.next_button.grid(row=0, column=1, padx=10)

        self.prev_button = tk.Button(button_frame, text="Previous", command=self.prev_flashcard)
        self.prev_button.grid(row=0, column=2, padx=10)

        self.display_flashcard()  # Display the first flashcard

    def load_flashcards(self, csv_file):
        try:
            # Specify only the first two columns
            df = pd.read_csv(csv_file, encoding="utf-8", usecols=[0, 1], names=["Question", "Answer"])
            flashcards = [Flashcard(row['Question'], row['Answer']) for index, row in df.iterrows()]
            random.shuffle(flashcards)  # Shuffle the flashcards
            return flashcards
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load flashcards: {e}")
            self.master.destroy()

    def display_flashcard(self):
        if len(self.displayed_indices) == len(self.flashcards):
            messagebox.showinfo("End", "You've shown all flashcards.")
           # self.displayed_indices.clear()  # Reset for a new round

        # Select a random card that has not been displayed yet
        self.iterator+=1
        if self.iterator >= len(self.indexes):
            while True:
                self.index = random.randint(0, len(self.flashcards) - 1)
                if self.index not in self.displayed_indices:
                    self.indexes.append(self.index)
                    self.iterator = len(self.indexes)
                    self.displayed_indices.add(self.index)  # Mark as displayed
                    self.new_card = True
                    break
        else:
            self.index=self.indexes[self.iterator]
        self.current_card = self.flashcards[self.index]
        self.question_label.config(text=f"Q: {self.current_card.question}")
        self.answer_label.config(text="")
        self.showing_answer = False

    def show_answer(self):
        if self.current_card and not self.showing_answer:
            self.answer_label.config(text=f"A: {self.current_card.answer}")
            self.showing_answer = True
    
    def hide_answer(self):
      self.answer_label.config(text="")
      self.showing_answer = False
        
    def next_flashcard(self):
        self.display_flashcard()  # Simply call display_flashcard to get a new card

    def prev_flashcard(self):
        if (self.iterator>=1):
            if self.new_card==True:
              self.iterator -=2
              self.new_card=False
            else:
              self.iterator -=1
            self.index= self.indexes[self.iterator]
            self.current_card = self.flashcards[self.index]
            self.question_label.config(text=f"Q: {self.current_card.question}")
            self.answer_label.config(text="")
            self.showing_answer = False
            
        else:
            messagebox.showinfo("Start", "You're at the first flashcard.")
def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root, "cleaned_flashcards.csv")
    center(root)
    
    root.mainloop()
