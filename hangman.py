# A hangman game made using Python and the Kivy gui library: https://kivy.org/
# to run the program just pip install kivy on your machine and all dependencies will be installed
# main theme font by Maknastudio at fontspace.com: https://www.fontspace.com/blomberg-font-f84442


# module imports
import random
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.button import ButtonBehavior 
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock

# font imports
LabelBase.register(name='blomberg', fn_regular="fonts/blomberg.ttf")
LabelBase.register(name='monospace', fn_regular="fonts/monospace.ttf")

# start button class
class StartButton(ButtonBehavior, Label):
    normal_color = (5/255, 100/255, 255/255, 1)
    down_color = (5/255, 40/255, 100/255, 1)

# starting screen
class StartingScreen(Screen):
    pass

# game screen
class GameScreen(Screen):
    word_list = (
        'apple', 'banana', 'cat', 'dog', 'elephant',
        'flower', 'green', 'happy', 'island', 'joy',
        'kite', 'lake', 'moon', 'nest', 'ocean',
        'piano', 'quiet', 'rainbow', 'sun', 'tree',
        'umbrella', 'volcano', 'wave', 'xylophone', 'yellow',
        'zebra', 'book', 'cloud', 'dream', 'friend',
        'guitar', 'hope', 'ice cream', 'juice', 'key',
        'lighthouse', 'mountain', 'notebook', 'orange', 'puzzle',
        'rabbit', 'star', 'train', 'umbrella', 'village',
        'waterfall', 'xylophone', 'yawn', 'zipper', 'science'
    )
    word = word_list[random.randint(0, 49)]
    dashes = ""
    if " " in word:
        for index in range(len(word)):
            if word[index] == " ":
                dashes = dashes + "  "
            else:
                dashes = dashes + "_ "
        dashes = dashes.rstrip()
    else:
        dashes = (len(word) * "_ ").rstrip()
    current_image_number = 0
    correct_guesses = []
    wrong_guesses = []
    new_label_text = ""
    first_line = True

    def set_focus(self, dt):
        self.ids.text_input.focus = True
    # core logic of the program
    def game(self, guess: str):
        dashed_word = ""
        # if user has entered a correct guess:
        # if user guessed the word in one go
        if guess.lower() == self.word.lower():
            if self.first_line:
                self.ids.hanglog.text = "you guessed the word!"
            else:    
                self.ids.hanglog.text = self.ids.hanglog.text + "\nyou guessed the word!"
            self.ids.text_input.disabled = True
            self.ids.submit_button.disabled = True
            for letter in self.word:    
                dashed_word = dashed_word + letter + " "
            self.ids.word_label.text = dashed_word.rstrip()
            self.first_line = False

        # if user has already guessed the letter:
        elif guess.lower() in self.wrong_guesses or guess.lower() in self.correct_guesses:                    
            self.ids.hanglog.text = self.ids.hanglog.text + "\nyou already guessed " f"{guess.lower()}" " try some other letter"

        # if guess is just a letter, doesn't equal an empty string and is in the word
        elif len(guess.lower()) == 1 and guess.lower().isalpha() and guess.lower() != "" and guess.lower() in self.word.lower():
            if self.first_line:
                self.ids.hanglog.text = "you guessed the letter " f"{guess.lower()}!"
            else:    
                self.ids.hanglog.text = self.ids.hanglog.text + "\nyou guessed the letter " f"{guess.lower()}!"
            self.correct_guesses.append(guess.lower())

            # if user guessed the word letter by letter
            if set(self.word.lower()) - {" "} == set(self.correct_guesses):
                    self.ids.hanglog.text = self.ids.hanglog.text + "\nyou guessed the word!"
                    self.ids.text_input.disabled = True
                    self.ids.submit_button.disabled = True
                    for letter in self.word:    
                        dashed_word = dashed_word + letter + " "

            # if user has not guessed the whole word yet
            else:
                for letter in self.word:
                    if letter.lower() in self.correct_guesses or letter == " ":
                        dashed_word = dashed_word + letter + " "
                    else:
                        dashed_word =  dashed_word + "_ "
            self.ids.word_label.text = dashed_word.rstrip()
            self.first_line = False

        # if user has entered a wrong guess:
        # if guess is just a letter, doesn't equal an empty string and is not in the word
        elif len(guess.lower()) == 1 and guess.lower().isalpha() and guess.lower() != "" and guess.lower() not in self.word.lower(): 
            self.current_image_number = self.current_image_number + 1
            if self.current_image_number < 6:
                if self.first_line:
                    self.ids.hanglog.text = "wrong guess :/"
                    self.wrong_guesses.append(guess.lower())
                else:    
                    self.ids.hanglog.text = self.ids.hanglog.text + "\nwrong guess :/"
                    self.wrong_guesses.append(guess.lower())
            if self.current_image_number == 6:
                self.ids.hanglog.text = self.ids.hanglog.text + "\nyou lost! the word was "f"{self.word} :3"
                self.ids.text_input.disabled = True
                self.ids.submit_button.disabled = True
            if self.current_image_number <= 6:
                self.ids.image_label.source = f"images/{self.current_image_number}.png"
            self.first_line = False
        self.ids.text_input.text = ""
        self.ids.hanglog.do_cursor_movement("cursor_down")
        Clock.schedule_once(self.set_focus, 0.1)
        

# app class
class HangmanApp(App):
    def build(self):
        self.title = "Hangman"
        self.icon = "images/icon.ico"
        screen_manager = ScreenManager()
        screen_manager.add_widget(StartingScreen(name="starting_screen"))
        screen_manager.add_widget(GameScreen(name="game_screen"))
        return screen_manager

# running the app
if __name__ == "__main__":
    HangmanApp().run()