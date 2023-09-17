from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Review, make_comment
from typing import List, Iterable

class NonExistentGameException(Exception):
    pass

class UnknownUserException(Exception):
    pass

def get_game(repo: AbstractRepository, game_id):
    game = repo.get_game(game_id)

    if game is None:
        return None  # Return None or handle the case where the game is not found

    game_details = {
        'game_id': game.game_id,
        'title': game.title,
        'release_date': game.release_date,
        'image_url': game.image_url,
        'price' : game.price,
        'publisher' : game.publisher,
        'description' : game.description,
        'reviews' : game.reviews
        # Add more attributes as needed
    }

    return game_details

def add_comment(game_id: int, comment: str, rating: int, user_name: str, repo: AbstractRepository):
    # Check that the article exists.
    game = repo.get_game(game_id)
    if game is None:
        raise NonExistentGameException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_comment(comment, user, game, rating)

    # Update the repository.
    repo.add_comment(comment)


def get_comments_for_game(game_id, repo: AbstractRepository):
    game = repo.get_game(game_id)

    if game is None:
        raise NonExistentGameException
    
    print("Comments for Game ID:", game_id)
    for comment in game.reviews:
        print(comment.comment)
        print(comment.rating)

    return comments_to_dict(game.reviews)

def get_games(repo: AbstractRepository) -> List[dict]:
    games = repo.get_games()

    if not games:
        return []

    # Rename the local variable to avoid the name conflict
    games_as_dict = games_to_dict(games)    

    return games_as_dict
    

# ============================================
# Functions to convert model entities to dicts
# ============================================

def game_to_dict(game: Game):
        game_dict = {
        'game_id': game.game_id,
        'title': game.title,
        'release_date': game.release_date,
        'image_url': game.image_url,
        'price' : game.price,
        'publisher' : game.publisher,
        'description' : game.description 
        }
        return game_dict

def games_to_dict(games: Iterable[Game]):
    return [game_to_dict(game) for game in games]

def comment_to_dict(comment: Review):
    comment_dict = {
        'username': comment.user.username,
        'game_id': comment.game.game_id,
        'comment': comment.comment,
        'rating' : comment.rating
    }
    return comment_dict


def comments_to_dict(reviews: Iterable[Review]):
    return [comment_to_dict(comment) for comment in reviews]

def average_rating(reviews):
    if not reviews:
        return "No Current Ratings"
    total = sum(review['rating'] for review in reviews)
    average = total / len(reviews)
    return average