from flask import Blueprint, url_for, render_template, request, redirect
from games.browse import services
from games.adapters import database_repository as repo


browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse():

    repository = repo.SqlAlchemyRepository(repo.session_factory)

    starting_page = 1
    max_games_per_page = 40  # Adjust this value as needed
    genre = request.args.get('genre')

    page = int(request.args.get('page', starting_page))  # Default to starting_page if not provided

    all_genres = services.get_genres(repository)

    # Calculate the starting index of games for the current page
    start_index = (page - 1) * max_games_per_page

    if genre:
        all_games = services.get_games_by_genre(repository,genre, sorting_key=lambda game: game.title)
        num_games = len(all_games)
    else:
        all_games = services.get_games(repository,sorting_key=lambda game: game.title)
        num_games = services.get_num_games(repository)


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
        all_genres=all_genres,
        genre=genre,
        selected_genre=genre
    )


@browse_blueprint.route('/search', methods=['GET', 'POST'])
def search():

    repository = repo.SqlAlchemyRepository(repo.session_factory)

    query = request.args.get('search_query')
    results = []
    
    if query:
        starting_page=1
        max_games_per_page = 40
        results = services.search_games(repository, query)
        page = int(request.args.get('page', starting_page))
        all_genres = services.get_all_genres(repository)
        start_index = (page - 1) * max_games_per_page
        num_games=len(results)
        num_pages = (num_games + max_games_per_page - 1) // max_games_per_page
        games_on_page = results[start_index:start_index + max_games_per_page]

        return render_template(
            'searchBar.html',
            title='Browse Games | CS235 Game Library',
            heading='Browse Games',
            query=query,
            results=results,
            games=games_on_page,
            number_of_games=num_games,
            current_page=page,
            num_pages=num_pages,
            max_games_per_page=max_games_per_page,
            all_genres = all_genres,

        )
    else:
        return redirect(url_for('browse_bp.browse'))


