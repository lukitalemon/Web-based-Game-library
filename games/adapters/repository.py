import abc 
from typing import List

from games.domainmodel.model import Game, User

repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):  # Change from Abstractrepository to AbstractRepository
    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_game(self, game_id : int):
        raise NotImplementedError
    




