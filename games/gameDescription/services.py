from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Review 
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
        'description' : game.description
        # Add more attributes as needed
    }

    return game_details

def add_comment(game_id: int, comment_text: str, user_name: str, repo: AbstractRepository):
    # Check that the game exists.
    game = repo.get_game(game_id)
    if game is None:
        raise NonExistentGameException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create a Review object with the provided data.
    review = Review(user, game, rating=0, comment=comment_text)

    # Add the review to the game's comments.
    game.add_review(review)

    # Update the repository.
    repo.add_review(review)


def get_reviews_for_game(game_id, repo: AbstractRepository):
    game = repo.get_game(game_id)

    if game is None:
        raise NonExistentGameException

    return reviews_to_dict(game.comments)


def review_to_dict_single(review: Review):
    review_dict = {
        'user_name': review.user.user_name,
        'game_id': review.game.game_id,
        'rating' : review.rating,
        'comment_text': review.comment
    }
    return review_dict

def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict_single(review) for review in reviews]