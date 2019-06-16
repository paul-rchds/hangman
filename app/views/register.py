from flask import session, redirect, url_for, g, flash
from flask.views import MethodView
from app.extensions import db
from app.helper import get_or_create
from app.helper import get_user
from app.mixins import HtmlMixin, ApiMixin
from app.models import User


class RegisterBase(MethodView):

    def validate_input(self):
        input_data = self.get_inputs()
        username = input_data.get('username')

        if not username:
            flash('Please enter a username.', 'danger')
            return None

        return username

    def get(self):
        g.user = get_user()

        if g.user:
            return redirect(url_for(self.success_url))

        return self.render_response()

    def post(self):
        username = self.validate_input()

        if username:
            user = get_or_create(db.session, User, username=username)
            session['user_id'] = user.id
            return redirect(url_for(self.success_url))

        return self.get()


class RegisterApiView(ApiMixin, RegisterBase):
    success_url = 'game.api-game'


class RegisterHtmlView(HtmlMixin, RegisterBase):
    success_url = 'game.game'
    template_class = 'register.html'
