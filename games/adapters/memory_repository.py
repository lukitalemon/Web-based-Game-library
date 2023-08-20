import os
from typing import List
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game
from bisect import insort_left

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            self.__games.append(game)
            #insort_left(self.__games, game)

    def get_games(self) -> List[Game]:
        return self.__games
    
    def get_number_of_games(self):
        return len(self.__games)
    
def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")

    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    games = reader.dataset_of_games

    for game in games:
        repo.add_game(game)


    
