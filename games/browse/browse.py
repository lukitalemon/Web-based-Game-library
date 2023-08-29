from flask import Blueprint, render_template, request
from games.browse import services
from games.adapters import repository as repo


browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    genre = request.args.get('genre')

    all_genres = services.get_all_genres(repo.repo_instance)

    if genre:
        all_games = services.get_games_by_genre(repo.repo_instance, genre, sorting_key=lambda game :game.title)
        num_games = len(all_games)
    else:
        all_games = services.get_games(repo.repo_instance, sorting_key=lambda game: game.title)  
        num_games = services.get_num_games(repo.repo_instance)

    return render_template(
        'browse.html',
        title='Browse Games | CS235 Game Library',
        heading='Browse Games',
        games=all_games,
        number_of_games=num_games,
        all_genres = all_genres
    )


