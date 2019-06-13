from app.extensions import db
from datetime import datetime
from random import randint
from flask import flash
from app.constants import IN_PROGRESS, GAME_STATUS_CHOICES, LOST, COMPLETE


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


class User(Base):
    username = db.Column(db.String(255), unique=True, nullable=False)
    games = db.relationship('Game', backref='user', lazy='dynamic')


class HighScore(Base):
    score = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Interval, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    @staticmethod
    def calculate_score(game):
        return 5 - game.incorrect_count

    @classmethod
    def save_high_score_from_game(cls, game):
        now = datetime.now()
        score = cls.calculate_score(game)

        new_high_score = cls(
            score=score,
            created=now,
            duration=now - game.start_time,
            game_id=game.id
        )
        db.session.add(new_high_score)
        game.status = COMPLETE
        db.session.commit()


class Game(Base):
    turn_count = db.Column(db.Integer, default=0)
    incorrect_count = db.Column(db.Integer, default=0)
    guessed_letters = db.Column(db.String(255), default='')
    blanked_word = db.Column(db.String(255), default='')
    status = db.Column(db.String(255), default=IN_PROGRESS)
    start_time = db.Column(db.DateTime, default=datetime.now)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    high_score = db.relationship('HighScore', backref='game', uselist=False, lazy=True)

    # def get_incorrect_count(self):
    #     print(self.guessed_letters)
    #     print(len(self.guessed_letters))
    #
    #     return self.turn_count - len(self.guessed_letters)

    def add_letter(self, letter):

        if letter in self.guessed_letters:
            flash(f"You have already guessed the letter '{letter}'", 'danger')
            return None

        self.guessed_letters += letter
        self.turn_count += 1

        if letter not in self.answer.word:
            self.incorrect_count += 1
        else:
            self.blanked_word = self.get_blanked_word()

        # self.save()
        db.session.commit()

    def has_lost(self):
        if self.incorrect_count >= 5:  # TODO 5 should be a setting.
            self.status = LOST
            db.session.commit()
            return True
        else:
            return False

    def has_won(self):
        if '_' in self.blanked_word:  # TODO blank character could be setting.
            return False
        else:
            HighScore.save_high_score_from_game(self)
            return True

    def get_blanked_word(self):
        blanked_word = []

        for letter in self.answer.word:
            if letter in self.guessed_letters:
                blanked_word.append(letter)
            else:
                blanked_word.append('_')

        return ' '.join(blanked_word)

    def save(self):
        if self.id is None:
            answer = Answer.get_random_word()
            if answer:
                self.answer_id = answer.id
                self.blanked_word = ('_ '*len(answer.word)).strip()
                self.guessed_letters = ''
                db.session.add(self)
            else:
                return None

        return db.session.commit()


class Answer(Base):
    word = db.Column(db.String(255), unique=True, nullable=False)
    games = db.relationship('Game', backref='answer', lazy=True)

    @classmethod
    def get_random_word(cls):
        word = None
        words = cls.query.all()

        if words:
            random_int = randint(0, len(words) - 1)
            word = words[random_int]
        else:
            flash('No words found. You need to initialize db with words before you play.', 'danger')

        return word
