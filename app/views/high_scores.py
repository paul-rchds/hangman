from flask.views import MethodView
from app.mixins import HtmlMixin, ApiMixin
from app.models import Game
from app.constants import COMPLETE


class HighScoresBase(MethodView):

    def get_context(self):
        games = Game.query.order_by(Game.high_score.desc()).filter_by(status=COMPLETE)
        results = [game.serialize() for game in games]
        return {'results': results}

    def get(self):
        context = self.get_context()
        return self.render_response(context)


class HighScoresApiView(ApiMixin, HighScoresBase):
    pass


class HighScoresHtmlView(HtmlMixin, HighScoresBase):
    template_class = 'high_scores.html'
