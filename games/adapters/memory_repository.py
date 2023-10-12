import os
from pathlib import Path
from datetime import date, datetime
from typing import List
from bisect import bisect_left, insort_left
from datetime import datetime

from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Game, Genre, Publisher, User, Review, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader

from werkzeug.security import generate_password_hash

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__genres = list()
        self.__title = list()
        self.__publishers = list()
        self.genres_dict = dict()
        self.publishers_dict = dict()
        self.__users = list()
        self.__comments = list()
        self.__user_wishlists = {}

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.username == user_name), None)

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
    
    def add_wishlist(self, username, wishlist: Wishlist):
        self.__user_wishlists[username] = wishlist

    def get_wishlist(self, username):
        return self.__user_wishlists.get(username, None)

    def wishlist_exists(self, username):
        return username in self.__user_wishlists

    def add_game_to_wishlist(self, username, game):
        wishlist = self.get_wishlist(username)
        if wishlist:
            wishlist.add_game(game)

    def remove_game_from_wishlist(self, username, game):
        wishlist = self.get_wishlist(username)
        if wishlist:
            wishlist.remove_game(game)

    def add_multiple_games(self, games: List[Game]):
        for game in games:
            self.add_game(game)
    
    def add_multiple_genres(self, genres: List[Genre]):
        for genre in genres:
            self.add_genre(genre)
    
    def add_multiple_publishers(self, publishers: List[Publisher]):
        for publisher in publishers:
            self.add_publisher(publisher)


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
