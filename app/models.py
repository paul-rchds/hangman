from datetime import datetime
from random import randint
from flask import flash
from app.constants import IN_PROGRESS, LOST, COMPLETE
from app.extensions import db
from settings import MAX_INCORRECT, BLANK_CHARACTER, POSSIBLE_ANSWERS


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


class User(Base):
    username = db.Column(db.String(255), unique=True, nullable=False)
    games = db.relationship('Game', backref='user', lazy='dynamic')

    def serialize(self):
        return {'username': self.username}


class HighScore(Base):
    score = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Interval, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), unique=True, nullable=False)

    @staticmethod
    def calculate_score(game):
        return MAX_INCORRECT - game.incorrect_count

    @classmethod
    def save_high_score_from_game(cls, game):
        now = datetime.now()
        score = cls.calculate_score(game)
        game.status = COMPLETE

        new_high_score = cls(
            score=score,
            created=now,
            duration=now - game.start_time,
            game_id=game.id
        )
        db.session.add(new_high_score)
        db.session.commit()

    def serialize(self):
        return {
            'username': self.game.user.username,
            'score': self.score,
            'duration': str(self.duration),
            'created': self.created,
        }


class Game(Base):
    turn_count = db.Column(db.Integer, default=0)
    incorrect_count = db.Column(db.Integer, default=0)
    guessed_letters = db.Column(db.String(255), default='')
    blanked_word = db.Column(db.String(255), default='')
    status = db.Column(db.String(255), default=IN_PROGRESS)
    start_time = db.Column(db.DateTime, default=datetime.now)
    answer = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    high_score = db.relationship('HighScore', backref='game', uselist=False, lazy=True)

    def add_letter(self, letter):

        if letter in self.guessed_letters:
            flash(f"You have already guessed the letter '{letter}'", 'danger')
            return None

        self.guessed_letters += letter
        self.turn_count += 1

        if letter not in self.answer:
            self.incorrect_count += 1
        else:
            self.blanked_word = self.get_blanked_word()

        db.session.commit()

    def has_lost(self):
        if self.incorrect_count >= MAX_INCORRECT:
            self.status = LOST
            db.session.commit()
            return True
        else:
            return False

    def has_won(self):
        if BLANK_CHARACTER in self.blanked_word:
            return False
        else:
            HighScore.save_high_score_from_game(self)
            return True

    def get_blanked_word(self):
        blanked_word = []

        for letter in self.answer:
            if letter in self.guessed_letters:
                blanked_word.append(letter)
            else:
                blanked_word.append(BLANK_CHARACTER)

        return ' '.join(blanked_word)

    @classmethod
    def get_random_answer(cls):
        answer = None

        if POSSIBLE_ANSWERS:
            random_int = randint(0, len(POSSIBLE_ANSWERS) - 1)
            answer = POSSIBLE_ANSWERS[random_int].upper()
        else:
            flash("No words found. 'POSSIBLE_ANSWERS' needs to be populated in the 'settings.py' file.", 'danger')

        return answer

    def start_new_game(self):
        answer = self.get_random_answer()
        if answer:
            self.answer = answer
            self.blanked_word = ' '.join([BLANK_CHARACTER]*len(answer))
            self.guessed_letters = ''
            db.session.add(self)
        else:
            return None

        return db.session.commit()

    def serialize(self):
        return {
            'max_incorrect': MAX_INCORRECT,
            'turn_count': self.turn_count,
            'start_time': self.start_time,
            'incorrect_count': self.incorrect_count,
            'blanked_word': self.blanked_word,
        }
