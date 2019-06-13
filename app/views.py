from flask import session, redirect, url_for, request, render_template, flash, g
from flask.views import MethodView
from app.extensions import db
from app.helper import get_or_create
from app.models import User, Game, HighScore
from app.helper import initialize_fixtures
from app.decorators import wrap_game
from app.helper import get_user


class BaseView(MethodView):

    def render_response(self, context):
        return render_template(self.template_class, **context)


class RegisterView(BaseView):
    template_class = 'register.html'

    def get(self):
        # initialize_fixtures(db)
        g.user = get_user()

        if g.user:
            return redirect(url_for('game'))

        return render_template(self.template_class)

    def post(self):
        username = request.form.get('username')
        user = get_or_create(db.session, User, username=username)
        session['user_id'] = user.id
        return redirect(url_for('game'))


class GameView(BaseView):
    template_class = 'game.html'
    decorators = [wrap_game]

    @staticmethod
    def validate_input():
        letter = request.form.get('letter')

        if not letter:
            flash('Please enter a letter.', 'danger')
            return None

        if len(letter) == 1 and letter.isalpha():
            return letter

        flash('Input should be a single character between A-Z.', 'danger')

    def get(self):
        return self.render_response({'game': g.game})

    def post(self):
        letter = self.validate_input()

        if letter:
            g.game.add_letter(letter)

        if g.game.has_lost():
            flash("GAME OVER - You guessed 5 incorrect letters. Click 'Reset Game' below to start again.", 'danger')

        if g.game.has_won():
            flash("Well done, you have won. Click 'Reset Game' below to play again or view your score under the 'High Scores' tab.", 'success')
            HighScore.save_high_score_from_game(g.game)

        return self.get()


class HighScoresView(BaseView):
    template_class = 'high_scores.html'

    def get(self):
        high_scores = HighScore.query.all()
        return self.render_response({'high_scores': high_scores})


class ResetView(BaseView):
    decorators = [wrap_game]

    def get(self):
        db.session.delete(g.game)
        session.pop('user_id', None)
        return redirect(url_for('register'))