from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game

# def get_number_of_games(repo: AbstractRepository):
#     return repo.get_number_of_games()


def get_games(repo: AbstractRepository, sorting_key=None):
    games = repo.get_games()

    if sorting_key:
        games = sorted(games, key=sorting_key)

    game_dicts = []
    for game in games:
        game_dict = {
            'game_id' : game.game_id, 
            'title' : game.title, 
            'game_url' : game.release_date, 
            'image_url' : game.image_url
        }
        game_dicts.append(game_dict)
    return game_dicts 

def get_num_games(repo: AbstractRepository):
    games = repo.get_games()
    number_of_games = 0
    for game in games:
        number_of_games += 1
    return number_of_games

