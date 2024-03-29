from games.adapters import database_repository as repo
from games.domainmodel.model import Game, Publisher
from flask import  request


def get_games(repo_instance, sorting_key=None):
    games = repo_instance.get_games()

    if sorting_key:
        games = sorted(games, key=sorting_key)

    game_dicts = []
    for game in games:
        game_dict = {
            'game_id': game.game_id,
            'title': game.title,
            'game_url': game.release_date,
            'image_url': game.image_url,
            'publisher': game.publisher.publisher_name,
            'genres': [genre.genre_name for genre in game.genres]
        }
        game_dicts.append(game_dict)
    return game_dicts



def get_num_games(repo_instance):
    games = repo_instance.get_games()
    number_of_games = 0
    for game in games:
        number_of_games += 1
    return number_of_games


def get_games_by_genre(repo_instance, genre_name: str, sorting_key=None):
    games_in_genre = [game for game in repo_instance.get_games() if any(genre_name.lower() == genre.genre_name.lower() for genre in game.genres)]
    if sorting_key:
        games_in_genre = sorted(games_in_genre, key=sorting_key)
    game_dicts = []
    for game in games_in_genre:
        game_dict = {
            'game_id': game.game_id,
            'title': game.title,
            'game_url': game.release_date,
            'image_url': game.image_url,
            'genres': [genre.genre_name for genre in game.genres]
        }
        game_dicts.append(game_dict)
    return game_dicts


def get_all_genres(repo: repo.SqlAlchemyRepository):
    all_genres = set()
    
    for game in repo.get_games():
        all_genres.update(genre.genre_name for genre in game.genres)

    return sorted(all_genres)


def get_genres(repo_instance):
    return repo_instance.get_genres()


def search_games(repo_instance, query: str):
    results = []
    all_games = get_games(repo_instance, sorting_key=lambda game:game.title)
    query = query.lower()
    type = request.args.get('type')

    for game in all_games:  
        if type == 'all':
            if (query in game['title'].lower()) or (query in game['publisher'].lower()) or (any(query in genre.lower() for genre in game['genres'])):
                results.append(game)
        elif type == 'title':
            if query in game['title'].lower():
                results.append(game)
        elif type == 'publisher':
            if query in game['publisher'].lower():
                results.append(game)
        elif type == 'genre':
            if any(query in genre.lower() for genre in game['genres']):
                results.append(game)
    return results
