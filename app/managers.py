from datetime import datetime
from app.constants import LOST, COMPLETE
from settings import MAX_INCORRECT, BLANK_CHARACTER
from app.errors import AlreadyGuessedError


class GameManager:

    def __init__(self, game=None):
        self.game = game

    def add_letter(self, letter):

        if letter in self.game.guessed_letters:
            raise AlreadyGuessedError

        self.game.guessed_letters += letter
        self.game.turn_count += 1

        if letter in self.game.answer:
            self.game.blanked_word = self.get_blanked_word()
        else:
            self.game.incorrect_count += 1

        self.game.save()

    def has_lost(self):
        if self.game.incorrect_count >= MAX_INCORRECT:
            self.game.status = LOST
            self.game.save()
            return True
        else:
            return False

    def has_won(self):
        if BLANK_CHARACTER in self.game.blanked_word:
            return False
        else:
            self.save_high_score()
            return True

    def get_blanked_word(self):
        blanked_word = []

        for letter in self.game.answer:
            if letter in self.game.guessed_letters:
                blanked_word.append(letter)
            else:
                blanked_word.append(BLANK_CHARACTER)

        return ' '.join(blanked_word)

    def calculate_score(self):
        return MAX_INCORRECT - self.game.incorrect_count

    def save_high_score(self):
        self.game.high_score = self.calculate_score()
        self.game.status = COMPLETE
        self.game.complete_time = datetime.now()
        self.game.save()
