import pytest
import os
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.gameDescription.services import get_game
from games.browse.services import get_games, get_num_games, get_games_by_genre, get_all_genres, search_games
from games.browse import services
from games.gameDescription import services
from games.adapters import repository as repo
from games.adapters.memory_repository import MemoryRepository

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    return repo


def test_return_game_object(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    game2 = Game(2, "Racing Game")
    game3 = Game(3, "Action Adventure")

    publisher1 = Publisher("publisher1")
    publisher2 = Publisher("publisher2")
    publisher3 = Publisher("publisher3")

    game1.publisher = publisher1
    game2.publisher = publisher2
    game3.publisher = publisher3

    in_memory_repo.add_game(game1)
    in_memory_repo.add_game(game2)
    in_memory_repo.add_game(game3)

    expected_games = [
        {
            'game_id': 1,
            'title': 'Soccer Game 1',
            'game_url': None,  # Update this with the actual release date or URL
            'image_url': None,  # Update this with the actual image URL
            'publisher': 'publisher1',  # Update this with the actual publisher name
            'genres': []  # Update this with the actual list of genres
        },
        {
            'game_id': 2,
            'title': 'Racing Game',
            'game_url': None,
            'image_url': None,
            'publisher': 'publisher2',
            'genres': []
        },
        {
            'game_id': 3,
            'title': 'Action Adventure',
            'game_url': None,
            'image_url': None,
            'publisher': 'publisher3',
            'genres': []
        }
    ]

    games = services.get_games(in_memory_repo)
    assert games == expected_games

def test_get_num_games(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    game2 = Game(2, "Racing Game")
    game3 = Game(3, "Action Adventure")

    in_memory_repo.add_game(game1)
    in_memory_repo.add_game(game2)
    in_memory_repo.add_game(game3)
    num_games = services.get_num_games(in_memory_repo)
    assert num_games == 3

def test_get_all_genres(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    game2 = Game(2, "Racing Game")
    game3 = Game(3, "Action Adventure")

    genre1 = Genre("Action")
    genre2 = Genre("Adventure")
    genre3 = Genre("War")

    game1.add_genre(genre1)
    game1.add_genre(genre3)
    game2.add_genre(genre2)
    game3.add_genre(genre3)

    in_memory_repo.add_game(game1)
    in_memory_repo.add_game(game2)
    in_memory_repo.add_game(game3)

    genres = services.get_all_genres(in_memory_repo)
    assert len(genres) == 3

def test_get_games_by_genre(in_memory_repo):
    genre = "Action"
    games = services.get_games_by_genre(in_memory_repo,genre)
    assert all(genre in game.genres for game in games)

def test_get_games_if_empty(in_memory_repo):
    games = services.get_games(in_memory_repo)
    assert games == []

def test_get_all_genres_if_empty(in_memory_repo):
    genres = services.get_all_genres(in_memory_repo)
    assert genres == []

def test_get_game(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    game2 = Game(2, "Racing Game")
    game3 = Game(3, "Action Adventure")

    publisher1 = Publisher("publisher1")
    publisher2 = Publisher("publisher2")
    publisher3 = Publisher("publisher3")

    game1.publisher = publisher1
    game2.publisher = publisher2
    game3.publisher = publisher3

    in_memory_repo.add_game(game1)
    in_memory_repo.add_game(game2)
    in_memory_repo.add_game(game3)

    expected_games = [
        {
            'game_id': 1,
            'title': 'Soccer Game 1',
            'release_date': None,
            'image_url': None,
            'price' : None,
            'publisher' : publisher1,
            'description' : None,
            'reviews' : None
        },
        {
            'game_id': 2,
            'title': 'Racing Game',
            'release_date': None,
            'image_url': None,
            'price' : None,
            'publisher' : publisher2,
            'description' : None,
            'reviews' : None
        },
        {
            'game_id': 3,
            'title': 'Action Adventure',
            'release_date': None,
            'image_url': None,
            'price' : None,
            'publisher' : publisher3,
            'description' : None,
            'reviews' : None
        }
    ]

    games = services.get_game(in_memory_repo, 2)
    assert games == expected_games





