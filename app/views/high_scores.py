from flask.views import MethodView
from app.mixins import HtmlMixin, ApiMixin
from app.models import HighScore


class HighScoresBase(MethodView):

    def get_context(self):
        high_scores = HighScore.query.order_by(HighScore.score.desc()).all()
        results = [hs.serialize() for hs in high_scores]
        return {'results': results}

    def get(self):
        context = self.get_context()
        return self.render_response(context)


class HighScoresApiView(ApiMixin, HighScoresBase):
    pass


class HighScoresHtmlView(HtmlMixin, HighScoresBase):
    template_class = 'high_scores.html'