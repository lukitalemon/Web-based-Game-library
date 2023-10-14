import pytest

import games.adapters.database_repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Publisher, Genre, Game, User, Review, Wishlist
from games.adapters.repository import RepositoryException
from tests_db.conftest import session_factory
from sqlalchemy.exc import NoResultFound
from games.domainmodel.model import make_comment

def test_repository_can_get_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    output = repo.get_games()
    assert len(output) == 981


def test_repository_can_get_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(3010, "Xpand Rally")
    game.price = 4.99
    game.release_date = "Aug 24, 2006"
    game.game_description = "Xpand Rally is a breathtaking game that gives you the true to life experience of driving powerful rally cars amidst photorealistic sceneries. Realistic weather effects, rolling hills, and animated scenery all add to game's visual perfection. Xpand Rally also features highly detailed models of modern rally cars and handling physics developed with the help of rally sport professionals which further enhance the realism of driving experience. Xpand Rally combines the best elements of Rally and Rally Cross racing in one unique gaming experience. The game offers a career mode based on time trials during both individual races and World Championship Series which will satisfy traditional Rally fans. The Rally Cross fans won't be disappointed either - they can challenge several opponents in head to head racing during competitions based on real and fictitious race events. Xpand Rally, as the only title on the market, brings the economy factor into a rally game. The player starts with a junk car and competes in races to earn money and acquire upgrades, repair damage, tweak performance and pay the race entry fees. Along with the tuning-up, the car's condition affects its handling. Due to accurate damage system, it is highly dependent on the player's driving skills. The physical handling model is also influenced by car parts configuration and provides both authentic feel and joy of driving. The interactive race track surroundings with enhanced game physics and the innovative approach to changing daytime and weather conditions, both influencing the car handling, are other hallmarks of Xpand Rally that distinguish it from other racing games. For the first time among rally games Xpand Rally includes a complete set of easy-to-use editing tools enabling to create new tracks, cars or even game mods."
    game.game_image_url = "https://cdn.akamai.steamstatic.com/steam/apps/3010/header.jpg?t=1639506578"
    game.publisher_name = "Techland"
    repo.add_game(game)

    games = repo.get_game(3010)

    assert games == game

def test_repository_can_add_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(1, "test")
    game.price = 4.99
    game.release_date = "Aug 24, 2006"
    game.game_description = "H"
    game.game_image_url = "https://cdn.akamai.steamstatic.com/steam/apps/3010/header.jpg?t=1639506578"
    game.publisher_name = "Techland"
    repo.add_game(game)

    games = repo.get_game(1)

    assert games == game


def test_repository_can_add_multiple_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game_list = [
        Game(1, "test"),
        Game(2, "test2"),
    ]
    game_list[0].price = 4.99
    game_list[1].price = 9.99
    game_list[0].release_date = "Aug 24, 2006"
    game_list[1].release_date = "Nov 12, 2007"
    game_list[0].game_description = "h"
    game_list[0].game_description = "j"
    game_list[0].game_image_url = "https://cdn.akamai.steamstatic.com/steam/apps/3010/header.jpg?t=1639506578"
    game_list[1].game_image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    game_list[0].publisher_name = "Techland"
    game_list[1].publisher_name = "Activision"
    repo.add_multiple_games(game_list)
    game1 = repo.get_game(1)
    game2 = repo.get_game(2)

    assert game1 == game_list[0]
    assert game2 == game_list[1]

def test_repository_can_get_number_of_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = Game(1, "test")
    game.price = 4.99
    game.release_date = "Aug 24, 2006"
    game.game_description = "H"
    game.game_image_url = "https://cdn.akamai.steamstatic.com/steam/apps/3010/header.jpg?t=1639506578"
    game.publisher_name = "d"
    repo.add_game(game)
    number_of_games = repo.get_number_of_games()

    assert number_of_games == 982

def test_repository_can_get_number_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    output = repo.get_number_of_publishers()
    assert output == 892
    session = session_factory()
    publisher1 = Publisher("test")
    publisher2 = Publisher("test2")
    session.add(publisher1)
    session.add(publisher2)
    session.commit()
    output2 = repo.get_number_of_publishers()

    assert output2 == 894

def test_repository_can_get_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    output = repo.get_publishers()
    assert len(output) == 892
    session = session_factory()
    publisher1 = Publisher("test")
    publisher2 = Publisher("test2")
    session.add(publisher1)
    session.add(publisher2)
    session.commit()
    output2 = repo.get_publishers()

    assert len(output2) == 894

def test_repository_can_add_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    session = session_factory()
    publisher1 = Publisher("test")
    session.add(publisher1)
    session.commit()
    output2 = repo.get_publishers()

    assert len(output2) == 893

def test_repository_can_add_multiple_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    output = repo.get_publishers()
    assert len(output) == 892
    publisher_list = [
        Publisher("ethan"),
        Publisher("min"),
        Publisher("luke"),
    ]
    repo.add_multiple_publishers(publisher_list)
    output_after = repo.get_publishers()
    assert len(output_after) == 895

def test_repository_can_get_number_of_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    session = session_factory()
    publisher1 = Publisher("test")
    session.add(publisher1)
    session.commit()
    output2 = repo.get_number_of_publishers()

    assert output2 == 893

def test_repository_can_get_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    output = repo.get_genres()
    assert len(output) == 26


def test_repository_can_add_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    output = repo.get_genres()
    assert len(output) == 26
    session = session_factory()
    genre = Genre("test")
    session.add(genre)
    session.commit()
    output_after = repo.get_genres()
    assert len(output_after) == 27

def test_repository_can_add_multiple_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    output = repo.get_genres()
    assert len(output) == 26
    genre_list = [
        Genre("ethan"),
        Genre("min"),
        Genre("luke"),
    ]
    repo.add_multiple_genres(genre_list)
    output_after = repo.get_genres()
    assert len(output_after) == 29

def test_repository_can_search_games_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(1, "test")
    game.price = 4.99
    game.release_date = "Aug 24, 2006"
    game.game_description = "H"
    game.game_image_url = "https://cdn.akamai.steamstatic.com/steam/apps/3010/header.jpg?t=1639506578"
    game.publisher_name = "Techland"
    repo.add_game(game)
    output = repo.search_games_by_title("test")
    assert output[0] == game

