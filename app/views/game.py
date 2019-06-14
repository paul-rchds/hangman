from flask import redirect, url_for, flash, g
from flask.views import MethodView
from app.helper import get_or_create_game, get_user
from app.mixins import HtmlMixin, ApiMixin
from settings import MAX_INCORRECT


class GameBase(MethodView):
    fail_url = ''

    def dispatch_request(self, *args, **kwargs):
        g.user = get_user()

        if not g.user:
            return redirect(url_for(self.fail_url))

        g.game = get_or_create_game(g.user)

        return super().dispatch_request(*args, **kwargs)

    def validate_input(self):
        input_data = self.get_inputs()
        letter = input_data.get('letter')

        if not letter:
            flash('Please enter a letter.', 'danger')
            return None

        if len(letter) == 1 and letter.isalnum():
            return letter.upper()

        flash('Input should be a single character between A-Z or 0-9', 'danger')


    def get_context(self):
        return {
            'game': {
                'max_incorrect': MAX_INCORRECT,
                'turn_count': g.game.turn_count,
                'start_time': g.game.start_time,
                'incorrect_count': g.game.incorrect_count,
                'blanked_word': g.game.blanked_word,
            },
            'user': {
                'username': g.user.username
            }
        }

    def get(self):
        context = self.get_context()
        return self.render_response(context)

    def post(self):
        letter = self.validate_input()

        if letter:
            g.game.add_letter(letter)

        if g.game.has_lost():
            flash("GAME OVER - You guessed 5 incorrect letters.", 'danger')

        if g.game.has_won():
            flash("Well done, you have won.", 'success')

        return self.get()


class GameApiView(ApiMixin, GameBase):
    fail_url = 'register.api-register'


class GameHtmlView(HtmlMixin, GameBase):
    template_class = 'game.html'
    fail_url = 'register.register'
