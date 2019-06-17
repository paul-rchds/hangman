from datetime import datetime
from random import randint
from flask import flash
from app.constants import IN_PROGRESS, LOST, COMPLETE
from app.extensions import db
from settings import MAX_INCORRECT, BLANK_CHARACTER, POSSIBLE_ANSWERS


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def serialize(self):
        raise NotImplementedError()


class User(Base):
    username = db.Column(db.String(255), unique=True, nullable=False)
    games = db.relationship('Game', backref='user', lazy='dynamic')

    def serialize(self):
        return {'username': self.username}


# class HighScore(Base):
#     score = db.Column(db.Integer)
#     created = db.Column(db.DateTime, nullable=False)
#     duration = db.Column(db.Interval, nullable=False)
#     game_id = db.Column(db.Integer, db.ForeignKey('game.id'), unique=True, nullable=False)
#
#     def serialize(self):
#         return {
#             'username': self.game.user.username,
#             'score': self.score,
#             'duration': str(self.duration),
#             'created': self.created,
#         }


class Game(Base):
    turn_count = db.Column(db.Integer, default=0)
    incorrect_count = db.Column(db.Integer, default=0)
    guessed_letters = db.Column(db.String(255), default='')
    blanked_word = db.Column(db.String(255), default='')
    status = db.Column(db.String(255), default=IN_PROGRESS)
    answer = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    high_score = db.Column(db.Integer, default=None, nullable=True)
    start_time = db.Column(db.DateTime, default=datetime.now)
    complete_time = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        game = {
            'username': self.user.username,
            'max_incorrect': MAX_INCORRECT,
            'turn_count': self.turn_count,
            'start_time': self.start_time,
            'complete_time': self.complete_time,
            'incorrect_count': self.incorrect_count,
            'blanked_word': self.blanked_word,
        }

        if self.high_score:
            game['high_score'] = self.high_score

        return game

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
            self.answer = answer,
            self.blanked_word = ' '.join([BLANK_CHARACTER]*len(answer)),
            self.guessed_letters = '',
            db.session.add(self)
            db.session.commit()
        else:
            return None

        return self
