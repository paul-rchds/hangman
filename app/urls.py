from flask import Blueprint
from app.views import register, game, reset, high_scores

register_bp = Blueprint('register', __name__)
register_bp.add_url_rule('/', view_func=register.RegisterHtmlView.as_view('register'))
register_bp.add_url_rule('/api/', view_func=register.RegisterApiView.as_view('api-register'))

game_bp = Blueprint('game', __name__, url_prefix='/game')
game_bp.add_url_rule('/', view_func=game.GameHtmlView.as_view('game'))
game_bp.add_url_rule('/api/', view_func=game.GameApiView.as_view('api-game'))

high_scores_bp = Blueprint('high-scores', __name__, url_prefix='/high-scores')
high_scores_bp.add_url_rule('/', view_func=high_scores.HighScoresHtmlView.as_view('list'))
high_scores_bp.add_url_rule('/api/', view_func=high_scores.HighScoresApiView.as_view('api-list'))

reset_bp = Blueprint('reset', __name__, url_prefix='/reset')
reset_bp.add_url_rule('/', view_func=reset.ResetHtmlView.as_view('reset'))
reset_bp.add_url_rule('/api/', view_func=reset.ResetApiView.as_view('api-reset'))
