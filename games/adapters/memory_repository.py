import os
from pathlib import Path
from datetime import date, datetime
from typing import List
from bisect import bisect_left, insort_left
from datetime import datetime

from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Game, Genre, Publisher, User, Review
from games.adapters.datareader.csvdatareader import GameFileCSVReader

from werkzeug.security import generate_password_hash

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__genres = list()
        self.__tile = list()
        self.__publishers = list()
        self.genres_dict = dict()
        self.publishers_dict = dict()
        self.__users = list()
        self.__comments = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None)

    def add_game(self, game: Game):
        if isinstance(game, Game) and game not in self.__games:
            insort_left(self.__games, game)

    def add_publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher) and publisher not in self.__publishers:
            insort_left(self.__publishers, publisher)

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre) and genre not in self.__genres:
            insort_left(self.__genres, genre)
            genre_name_lower = genre.genre_name.lower()  # Convert the genre name to lowercase
            self.genres_dict[genre_name_lower] = []  # Initialize an empty list for this lowercase genre name


    def get_game(self, target_id: int):
        for game in self.__games:
            if game.game_id == target_id:
                return game
        return None
    
    def get_games(self):
        return self.__games
    

    
    def get_games_by_genre(self, genre_name):
        genre_name = genre_name.lower()
        games_in_genre = [game for game in self.__games if genre_name in game.genres]
        return games_in_genre

    def get_games_by_title(self, title_name):
        title_name = title_name.lower()
        games_with_title = [game for game in self.__games if title_name in game.title]
        return games_with_title

    def add_comment(self, comment: Review):
        # call parent class first, add_comment relies on implementation of code common to all derived classes
        super().add_comment(comment)
        self.__comments.append(comment)

    def get_comments(self):
        return self.__comments

    
    
    
def populate(data_path: Path, repo: MemoryRepository):
    games_file_name = str(Path(data_path))
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()

    for game in reader.dataset_of_games:
        repo.add_game(game)
        for genre in game.genres:
            if genre.genre_name not in repo.genres_dict:
                repo.genres_dict[genre.genre_name] = [game]
            else:
                repo.genres_dict[genre.genre_name].append(game)
        if game.publisher.publisher_name not in repo.publishers_dict:
            repo.publishers_dict[game.publisher.publisher_name] = [game]
        else:
            repo.publishers_dict[game.publisher.publisher_name].append(game)
    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)

    for publisher in reader.dataset_of_publishers:
        repo.add_publisher(publisher)
