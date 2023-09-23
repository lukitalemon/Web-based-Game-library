import pytest
import os
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.gameDescription import services as gameDescription_services
from games.gameDescription.services import NonExistentGameException, UnknownUserException
from games.browse import services as browse_services
from games.authentication import services as authentication_services
from games.authentication.services import NameNotUniqueException, UnknownUserException, AuthenticationException
from games.profile import services as profile_services
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

    games = browse_services.get_games(in_memory_repo)
    assert games == expected_games

def test_get_num_games(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    game2 = Game(2, "Racing Game")
    game3 = Game(3, "Action Adventure")

    in_memory_repo.add_game(game1)
    in_memory_repo.add_game(game2)
    in_memory_repo.add_game(game3)
    num_games = browse_services.get_num_games(in_memory_repo)
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

    genres = browse_services.get_all_genres(in_memory_repo)
    assert len(genres) == 3

def test_get_games_by_genre(in_memory_repo):
    genre = "Action"
    games = browse_services.get_games_by_genre(in_memory_repo,genre)
    assert all(genre in game.genres for game in games)

def test_get_games_if_empty(in_memory_repo):
    games = browse_services.get_games(in_memory_repo)
    assert games == []

def test_get_all_genres_if_empty(in_memory_repo):
    genres = browse_services.get_all_genres(in_memory_repo)
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

    expected_games ={
            'game_id': 2,
            'title': 'Racing Game',
            'release_date': None,
            'image_url': None,
            'price' : None,
            'publisher' : publisher2,
            'description' : None,
            'reviews' : []
        }


    games = gameDescription_services.get_game(in_memory_repo, 2)
    assert games == expected_games

def test_add_comment(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    comment = "This is a really good game"
    rating = 3
    user_name = "asianhard123"
    password = "ET12345678"

    in_memory_repo.add_game(game1)
    authentication_services.add_user(user_name,password , in_memory_repo)
    gameDescription_services.add_comment(1, comment, rating, user_name, in_memory_repo)
    comment = gameDescription_services.get_comments_for_game(1, in_memory_repo)

    assert comment[0] == {'username': 'asianhard123', 'game_id': 1, 'comment': 'This is a really good game', 'rating': 3}

def test_add_comment_with_no_game(in_memory_repo):
    comment = "This is a really good game"
    rating = 3
    user_name = "asianHard123"

    with pytest.raises(gameDescription_services.NonExistentGameException):
        gameDescription_services.add_comment(1, comment, rating, user_name, in_memory_repo)

def test_add_comment_when_no_user(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    comment = "This is a really good game"
    rating = 3
    user_name = "asianHard123"

    in_memory_repo.add_game(game1)

    with pytest.raises(gameDescription_services.UnknownUserException):
        gameDescription_services.add_comment(1, comment, rating, user_name, in_memory_repo)

def test_get_comments_for_game(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    comment = "This is a really good game"
    comment2 = "Such a Geary Game"
    rating = 3
    user_name = "asianhard123"
    password = "ET12345678"

    in_memory_repo.add_game(game1)
    authentication_services.add_user(user_name, password, in_memory_repo)
    gameDescription_services.add_comment(1, comment, rating, user_name, in_memory_repo)
    gameDescription_services.add_comment(1, comment2, rating, user_name, in_memory_repo)

    comments = gameDescription_services.get_comments_for_game(1, in_memory_repo)

    assert comments[0] == {'username': 'asianhard123', 'game_id': 1, 'comment': 'This is a really good game', 'rating': 3}
    assert comments[1] == {'username': 'asianhard123', 'game_id': 1, 'comment': 'Such a Geary Game', 'rating': 3}

def test_get_comments_for_with_no_game(in_memory_repo):
    with pytest.raises(gameDescription_services.NonExistentGameException):
        gameDescription_services.get_comments_for_game(1, in_memory_repo)

def test_get_games(in_memory_repo):
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

    expected_games =[{
        'game_id': 1,
        'title': 'Soccer Game 1',
        'release_date': None,
        'image_url': None,
        'price': None,
        'publisher': publisher1,
        'description': None,
    }, {
        'game_id': 2,
        'title': 'Racing Game',
        'release_date': None,
        'image_url': None,
        'price': None,
        'publisher': publisher2,
        'description': None,
    }, {
        'game_id': 3,
        'title': 'Action Adventure',
        'release_date': None,
        'image_url': None,
        'price': None,
        'publisher': publisher3,
        'description': None,
    }]

    games = gameDescription_services.get_games(in_memory_repo)
    assert games == expected_games

def test_get_games_if_not_games(in_memory_repo):
    games = gameDescription_services.get_games(in_memory_repo)
    assert games == []

def test_game_to_dict(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    publisher1 = Publisher("publisher1")
    game1.publisher = publisher1
    in_memory_repo.add_game(game1)
    expected_games = {
        'game_id': 1,
        'title': 'Soccer Game 1',
        'release_date': None,
        'image_url': None,
        'price': None,
        'publisher': publisher1,
        'description': None,
    }
    game = gameDescription_services.game_to_dict(game1)
    assert game == expected_games

def test_games_to_dict(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    game2 = Game(2, "Racing Game")
    game3 = Game(3, "Action Adventure")

    games_list = [game1, game2, game3]
    games_dict = gameDescription_services.games_to_dict(games_list)

    expected_games = [{
        'game_id': 1,
        'title': 'Soccer Game 1',
        'release_date': None,
        'image_url': None,
        'price': None,
        'publisher': None,
        'description': None,
    }, {
        'game_id': 2,
        'title': 'Racing Game',
        'release_date': None,
        'image_url': None,
        'price': None,
        'publisher': None,
        'description': None,
    }, {
        'game_id': 3,
        'title': 'Action Adventure',
        'release_date': None,
        'image_url': None,
        'price': None,
        'publisher': None,
        'description': None,
    }]

    assert games_dict == expected_games

def test_comment_to_dict(in_memory_repo):
    user = User("asianhard123", "ET1234567")
    game1 = Game(1, "Soccer Game 1")
    review = Review(user, game1, 4, "Wow amazing red bull campus clutch")
    review_list = [review]

    expected = [{
        'username': "asianhard123",
        'game_id': 1,
        'comment': "Wow amazing red bull campus clutch",
        'rating': 4
    }]

    comment_dict = gameDescription_services.comments_to_dict(review_list)

    assert comment_dict == expected

def test_comments_to_dict(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    game2 = Game(2, "Racing Game")
    game3 = Game(3, "Action Adventure")

    user1 = User("asianhard123", "ET1234567")
    user2 = User("greenalien", "MR1234567")
    user3 = User("lukivatas", "LV1234567")

    review1 = Review(user1, game1, 4, "Wow amazing red bull campus clutch")
    review2 = Review(user2, game2, 3, "Good campus clutch finals")
    review3 = Review(user3, game3, 2, "Was a bad day for me and my team")
    review_list = [review1, review2, review3]
    review_dict = gameDescription_services.comments_to_dict(review_list)


    expected_games = [{
        'username': "asianhard123",
        'game_id': 1,
        'comment': "Wow amazing red bull campus clutch",
        'rating': 4
    }, {
        'username': "greenalien",
        'game_id': 2,
        'comment': "Good campus clutch finals",
        'rating': 3
    }, {
        'username': "lukivatas",
        'game_id': 3,
        'comment': "Was a bad day for me and my team",
        'rating': 2
    }]

    assert review_dict == expected_games

def test_average_rating(in_memory_repo):
    game1 = Game(1, "Soccer Game 1")
    game2 = Game(2, "Racing Game")
    game3 = Game(3, "Action Adventure")

    user1 = User("asianhard123", "ET1234567")
    user2 = User("greenalien", "MR1234567")
    user3 = User("lukivatas", "LV1234567")

    review1 = Review(user1, game1, 4, "Wow amazing red bull campus clutch")
    review2 = Review(user2, game2, 3, "Good campus clutch finals")
    review3 = Review(user3, game3, 2, "Was a bad day for me and my team")

    review_list = [review1, review2, review3]
    review_dict = gameDescription_services.comments_to_dict(review_list)

    average = gameDescription_services.average_rating(review_dict)

    assert average == 3

def test_average_rating_it_no_reviews(in_memory_repo):
    review_list = []
    review_dict = gameDescription_services.average_rating(review_list)

    assert review_dict == "No Current Ratings"


def test_add_user(in_memory_repo):
    username = "asianhard123"
    password = "ET1234567"
    authentication_services.add_user(username, password, in_memory_repo)

    user_as_dict = authentication_services.get_user(username, in_memory_repo)

    assert user_as_dict['user_name'] == username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')

def test_cannot_add_user_with_existing_name(in_memory_repo):
    username1 = 'asianhard123'
    password1 = 'ET1234567'

    username2 = "asianhard123"
    password2 = "ET1234567"

    authentication_services.add_user(username1, password1, in_memory_repo)

    with pytest.raises(authentication_services.NameNotUniqueException):
        authentication_services.add_user(username2, password2, in_memory_repo)

def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    authentication_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        authentication_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False

def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    authentication_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(authentication_services.AuthenticationException):
        authentication_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)

def test_get_user(in_memory_repo):
    username = "asianhard123"
    password = "ET1234567"
    user1 = User("asianhard123", "ET1234567")
    authentication_services.add_user(username, password, in_memory_repo)
    expected = authentication_services.get_user(username, in_memory_repo)
    user_as_dict = authentication_services.user_to_dict(user1)


    assert user_as_dict['user_name'] == expected['user_name']

def test_get_user_when_no_user(in_memory_repo):
    with pytest.raises(authentication_services.UnknownUserException):
        authentication_services.get_user("asianhard123", in_memory_repo)

def test_user_to_dict(in_memory_repo):
    username = "asianhard123"
    password = "ET1234567"
    user1 = User("asianhard123", "ET1234567")
    authentication_services.add_user(username, password, in_memory_repo)
    expected = {
        'user_name': "asianhard123",
        'password': "ET1234567"
    }
    user_as_dict = authentication_services.user_to_dict(user1)

    assert user_as_dict['user_name'] == expected['user_name']

def test_get_comments_by_user(in_memory_repo):
    username1 = "asianhard123"
    username2 = 'lukevitas123'
    password1 = "ET1234567"
    password2 = "LV1234567"

    user1 = User("asianhard123", "ET1234567")
    user2 = User("lukevitas123", "LV1234567")

    authentication_services.add_user(username1, password1, in_memory_repo)
    authentication_services.add_user(username2, password2, in_memory_repo)

    game1 = Game(1, "Soccer Game 1")
    in_memory_repo.add_game(game1)

    gameDescription_services.add_comment(1, "Wow amazing red bull campus clutch", 4, "asianhard123", in_memory_repo)
    gameDescription_services.add_comment(1, "Such a fun game to play", 4, "lukevitas123", in_memory_repo)

    comment_user = profile_services.get_comments_by_user(username1, in_memory_repo)
    expected = ["Wow amazing red bull campus clutch"]
    comment = [comment.comment for comment in comment_user]

    assert comment == expected



