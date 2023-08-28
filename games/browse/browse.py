from flask import Blueprint, render_template
from games.browse import services
from games.adapters import repository as repo


browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    # num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    return render_template(
        'browse.html',
        title='Browse Games | CS235 Game Library',  # Custom page title
        heading='Browse Games',  # Page heading
        games=all_games
        
    )


