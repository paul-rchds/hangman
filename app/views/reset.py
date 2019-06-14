from flask import session, redirect, url_for, g
from flask.views import MethodView
from app.extensions import db
from app.mixins import HtmlMixin, ApiMixin


class ResetBase(MethodView):

    def get(self):
        if hasattr(g, 'game'):
            db.session.delete(g.game)

        session.pop('user_id', None)
        return redirect(url_for(self.success_url))


class ResetApiView(ApiMixin, ResetBase):
    success_url = 'register.api-register'


class ResetHtmlView(HtmlMixin, ResetBase):
    success_url = 'register.register'
