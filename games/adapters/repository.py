import abc 
from typing import List

from games.domainmodel.model import Game

repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):  # Change from Abstractrepository to AbstractRepository
    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_game(self, game_id : int):
        raise NotImplementedError


    # @abc.abstractmethod
    # def get_number_of_games(self):
    #     raise NotImplementedError




