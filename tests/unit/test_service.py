import pytest
import os
from games.datareader.repoitory.py import AbstractRepository
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.services import get_games, get_num_game, get_games_by_genre, get_all_genres, search_games

def test_return_game_object(in_memory_repo):
    
