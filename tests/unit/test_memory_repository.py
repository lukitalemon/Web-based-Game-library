import pytest

from games.domainmodel.model import Game, Publisher, Genre
from games.adapters.memory_repository import MemoryRepository


test_game_id = 11
test_game_title = "Test Game"
test_publisher_name = "Test Publisher"
test_genre_name = "Test Genre"

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    return repo

def test_add_game(in_memory_repo):
    game1 = Game(2, "game")
    in_memory_repo.add_game(game)
    retrieved_game = in_memory_repo.get_game(2)
    assert retrieved_game is game1

def test_retrive_game(in_memory_repo):
    game1 = Game(2, "game")
    in_memory_repo.add_game(game1)
    retrieved_game = in_memory_repo.get_game(2)
    assert retrieved_game is game1

def test_correct_num_objects(in_memory_repo):
    game1 = Game(2, "game")
    game2 = Game(4, "game2")
    game3 = Game(6, "game3")
    in_memory_repo.add_game(game1)
    in_memory_repo.add_game(game2)
    in_memory_repo.add_game(game3)
    length = len(in_memory_repo.get_games())
    assert length == 3

def test_num_unique_genres(in_memory_repo):
    genre1 = Genre("MMO")
    genre2 = Genre("RPG")
    genre3 = Genre("Action")

    game1 = Game(2, "game")
    game2 = Game(4, "game2")
    game3 = Game(6, "game3")

    game1.add_genre(genre1)
    game1.add_genre(genre2)
    game1.add_genre(genre3)

    game2.add_genre(genre1)
    game2.add_genre(genre3)

    game3.add_genre(genre1)

    in_memory_repo.add_game(game1)
    in_memory_repo.add_game(game2)
    in_memory_repo.add_game(game3)

    list = []
    for game in in_memory_repo.get_games():
        for genre in game.genres:
            if genre not in list:
                list.append(genre)
    length = len(list)
    assert length == 3

def test_add_new_genre_and_increment_count(in_memory_repo):
    game1 = Game(2, "game")
    genre1 = Genre("RPG")
    game1.add_genre(genre1)
    in_memory_repo.add_game(game1)
    starting_list = []
    for game in in_memory_repo.get_games():
        for genre in game.genres:
            if genre not in starting_list:
                starting_list.append(genre)
    starting_length = len(starting_list)

    game2 = Game(4, "game2")
    genre2 = Genre("Action")
    in_memory_repo.add_game(game2)
    game2.add_genre(genre2)
    in_memory_repo.add_genre(genre2)
    ending_list = []
    for game in in_memory_repo.get_games():
        for genre in game.genres:
            if genre not in ending_list:
                ending_list.append(genre)
    ending_length = len(ending_list)

    assert ending_length == starting_length + 1
    assert Genre("Action") in ending_list

def test_search_by_title_or_pub(in_memory_repo):
    game1 = Game(2, "game")
    game2 = Game(4, "game2")
    game3 = Game(6, "fake")

    genre

    in_memory_repo.add_game(game1)
    in_memory_repo.add_game(game2)
    in_memory_repo.add_game(game3)

    sorted_games = in_memory_repo.get_games_by_title("game")

    assert game3 not in sorted_games
    assert game2 in sorted_games
    assert game1 in sorted_games

def test_search_by_genre(in_memory_repo):
    game1 = Game(2, "game1")
    game2 = Game(4, "game2")
    game3 = Game(6, "game3")

    genre1 = Genre("Casual")
    genre2 = Genre("Audio Production")
    genre3 = Genre("Video Production")

    game1.add_genre(genre1)

    game2.add_genre(genre2)
    game2.add_genre(genre3)

    game3.add_genre(genre3)

    in_memory_repo.add_game(game1)
    in_memory_repo.add_game(game2)
    in_memory_repo.add_game(game3)

    sorted_games = in_memory_repo.get_games_by_genre("Production")

    print(len(sorted_games))
