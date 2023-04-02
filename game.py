import tkinter as tk
import random

class GuessNumberGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Guess the Number")
        self.master.geometry("500x300")

        self.num_to_guess = random.randint(1, 100)
        self.num_guesses = 0

        self.guess_label = tk.Label(self.master, text="Guess a number between 1 and 100:")
        self.guess_label.pack()

        self.guess_entry = tk.Entry(self.master)
        self.guess_entry.pack()

        self.guess_button = tk.Button(self.master, text="Guess", command=self.check_guess)
        self.guess_button.pack()

        self.result_label = tk.Label(self.master, text="")
        self.result_label.pack()

    def check_guess(self):
        guess = int(self.guess_entry.get())
        self.num_guesses += 1

        if guess < self.num_to_guess:
            self.result_label.config(text="Too low! Guess again.")
        elif guess > self.num_to_guess:
            self.result_label.config(text="Too high! Guess again.")
        else:
            self.result_label.config(text=f"Congratulations! You guessed the number in {self.num_guesses} guesses.")
            self.guess_button.config(state=tk.DISABLED)
            self.guess_entry.config(state=tk.DISABLED)

root = tk.Tk()
game = GuessNumberGame(root)
root.mainloop()
