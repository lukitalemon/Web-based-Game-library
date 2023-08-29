from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game

def get_game(repo: AbstractRepository, game_id):
    game = repo.get_game(game_id)

    if game is None:
        return None  # Return None or handle the case where the game is not found

    game_details = {
        'game_id': game.game_id,
        'title': game.title,
        'release_date': game.release_date,
        'image_url': game.image_url,
        'price' : game.price
        # Add more attributes as needed
    }

    return game_details

