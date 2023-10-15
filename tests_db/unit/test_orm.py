import pytest
from games.domainmodel.model import Publisher, Genre, Game, User, Review, Wishlist
from tests_db.conftest import empty_session
from sqlalchemy.exc import IntegrityError

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "JohnHard123"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT user_id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_publisher(empty_session, name = "pub_name"):
    empty_session.execute("INSERT INTO publishers (name) VALUES (:name)", {"name" : name})
    row = empty_session.execute("SELECT name FROM publishers WHERE name = :name ", {"name": name}).fetchone()
    return row[0]

def insert_genre(empty_session, name = "test_genre" ):
    empty_session.execute("INSERT INTO genres (genre_name) VALUES (:genre_name)", {"genre_name" : name})
    row = empty_session.execute("SELECT genre_name FROM genres WHERE genre_name = :genre_name", {"genre_name" : name}).fetchone()
    return row[0]

def insert_game(empty_session):
    game = {
        "game_title" : "test",
        "game_price" : 2,
        "release_date" : "Aug 24, 2006",
        "game_description" : "testing game",
        "game_image_url" : "https://jjj.com/header.jpg?t=1639506578",
        "game_website_url" : "https://jjj.com",
        "publisher_name" : "publisher",
    }
    empty_session.execute(
        "INSERT INTO games (game_title, game_price, release_date, game_description, game_image_url, game_website_url, publisher_name)"
        "VALUES (:game_title, :game_price, :release_date, :game_description, :game_image_url, :game_website_url, :publisher_name) ",
        game
    )

    row = empty_session.execute("SELECT game_id FROM games").fetchone()
    return row[0]

def insert_review(empty_session):
    review = {
        "comment" : "Noice",
        "rating" : 3,
        "game_id" : 2,
        "user_id" : 1
    }
    empty_session.execute(
        "INSERT INTO reviews (comment, rating, game_id, user_id)"
        "VALUES (:comment, :rating, :game_id, :user_id)",
        review
    )

    row = empty_session.execute("SELECT review_id FROM reviews ").fetchone()
    return row[0]

def insert_wishlist(empty_session):
    wishlist = {
        "username" : "AsianHard123",
        "game_id" : 12
    }
    empty_session.execute(
        "INSERT INTO wishlists (username, game_id)"
        "VALUES (:username, :rating",
        wishlist
    )

def make_user():
    user = User("AsianHard123", "Potty231")
    return user
def make_publisher():
    publisher = Publisher("pub_name")
    return publisher

def make_genre():
    genre = Genre("test_genre")
    return genre

def make_game():
    game = Game(1, "test")
    game.price = 2
    game.release_date = "Aug 24, 2006"
    game.game_description = "testing game"
    game.game_image_url = "https://jjj.com/header.jpg?t=1639506578"
    game.game_website_url = "https://jjj.com"
    game.publisher_name = "publisher"
    return game

def make_review():
    user = make_user()
    game = make_game()
    review = Review(user, game, 3, "Good Game")
    return review

def make_wishlist():
    user = make_user()
    game = make_game()
    wishlist = Wishlist(user)
    wishlist.add_game(game)
    return wishlist

def test_loading_of_users(empty_session):
    users = list()
    users.append(("ethan", "Popplod123"))
    users.append(("minluke", "Dopelore123"))
    insert_users(empty_session, users)

    expected = [
        User("ethan", "Popplod123"),
        User("minluke", "Dopelore123")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("AsianHard123", "Potty231")]

def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("AsianHard123", "Potty231"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("AsianHard123", "Potty2312")
        empty_session.add(user)
        empty_session.commit()

def test_saving_of_publishers(empty_session):
    publisher = make_publisher()
    empty_session.add(publisher)
    empty_session.commit()

    rows = list(empty_session.execute("SELECT name FROM publishers"))
    assert rows == [("pub_name",)]

def test_loading_of_publishers(empty_session):
    insert_publisher(empty_session, "pub_name" )
    expected = make_publisher()
    assert empty_session.query(Publisher).one() == expected

def test_saving_of_games(empty_session):
    game = make_game()
    empty_session.add(game)
    empty_session.commit()
    rows = list(empty_session.execute("SELECT game_id, game_title FROM games"))
    assert rows == [(1, "test")]

def test_loading_of_games(empty_session):
    game = insert_game(empty_session)
    expected = make_game()
    assert empty_session.query(Game).one() == expected

def test_loading_of_genres(empty_session):
    genre = insert_genre(empty_session)
    expected = make_genre()
    assert empty_session.query(Genre).one() == expected

def test_saving_of_genres(empty_session):
    genre = make_genre()
    empty_session.add(genre)
    empty_session.commit()
    rows = list(empty_session.execute("SELECT genre_name FROM genres"))
    assert rows == [("test_genre",)]

def test_saving_of_reviews(empty_session):
    review = make_review()
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute("SELECT comment, rating FROM reviews"))
    assert rows == [("Good Game", 3)]
