from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game

def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()

def get_games(repo: AbstractRepository):
    games = repo.get_games()
    game_dicts = []
    for game in games:
        game_dict = {
            'game_id' : game.game_id, 'title' : game.title, 'game_url' : game.release_date, 
        }
        game_dicts.append(game_dict)
    return game_dicts 