from flask import Blueprint, render_template, request
from games.browse import services
from games.adapters import repository as repo


browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    starting_page = 1
    max_games_per_page = 40  # Adjust this value as needed
    genre = request.args.get('genre')

    page = int(request.args.get('page', starting_page))  # Default to starting_page if not provided

    all_genres = services.get_all_genres(repo.repo_instance)

    # Calculate the starting index of games for the current page
    start_index = (page - 1) * max_games_per_page

    if genre:
        all_games = services.get_games_by_genre(repo.repo_instance, genre, sorting_key=lambda game: game.title)
        num_games = len(all_games)
    else:
        all_games = services.get_games(repo.repo_instance, sorting_key=lambda game: game.title)
        num_games = services.get_num_games(repo.repo_instance)


    num_pages = (num_games + max_games_per_page - 1) // max_games_per_page

    # Get the subset of games for the current page
    games_on_page = all_games[start_index:start_index + max_games_per_page]


    return render_template(
        'browse.html',
        title='Browse Games | CS235 Game Library',
        heading='Browse Games',
        games=games_on_page,
        number_of_games=num_games,
        current_page=page,
        num_pages=num_pages,
        max_games_per_page=max_games_per_page,
        all_genres = all_genres,
        genre = genre
    )