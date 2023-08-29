from flask import Blueprint, render_template
from games.gameDescription import services
from games.adapters import repository as repo

gameDescription_blueprint = Blueprint('gameDescription_bp', __name__)

@gameDescription_blueprint.route('/GameDescription/<int:game_id>', methods=['GET'])
def gameDescription(game_id):
    game_details = services.get_game(repo.repo_instance, game_id)

    if game_details is None:
        # Handle the case where the game is not found
        return render_template('game_not_found.html')

    return render_template(
        'gameDescription.html',
        game=game_details,
    )
