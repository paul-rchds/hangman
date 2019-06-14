from flask.views import MethodView
from app.mixins import HtmlMixin, ApiMixin
from app.models import HighScore


class HighScoresBase(MethodView):

    def get_context(self):
        results = []
        high_scores = HighScore.query.order_by(HighScore.score.desc()).all()
        for high_score in high_scores:
            results.append({
                'username': high_score.game.user.username,
                'score': high_score.score,
                'duration': str(high_score.duration),
                'created': high_score.created,
            })
        return {'results': results}

    def get(self):
        context = self.get_context()
        return self.render_response(context)


class HighScoresApiView(ApiMixin, HighScoresBase):
    pass


class HighScoresHtmlView(HtmlMixin, HighScoresBase):
    template_class = 'high_scores.html'