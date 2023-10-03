import abc
from typing import List

from games.domainmodel.model import Game, User, Review, Wishlist, Publisher, Genre

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):  # Change from Abstract-repository to AbstractRepository
    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, game_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_publishers(self, publisher: List[Publisher]):
        """ Add multiple games to the repository of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_games(self, games: List[Game]):
        """ Add multiple games to the repository of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_genres(self, genres: List[Genre]):
        """ Add many genres to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_comment(self, comment: Review):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an game and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if comment.user is None or comment not in comment.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if comment.game is None or comment not in comment.game.reviews:
            raise RepositoryException('Comment not correctly attached to an game')

    @abc.abstractmethod
    def get_comments(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError

    def add_wishlist(self, username, wishlist: Wishlist):
        raise NotImplementedError

    def get_wishlist(self, username):
        raise NotImplementedError

    def wishlist_exists(self, username):
        raise NotImplementedError

    def add_game_to_wishlist(self, username, game):
        raise NotImplementedError

    def remove_game_from_wishlist(self, username, game):
        raise NotImplementedError
