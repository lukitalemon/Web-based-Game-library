from abc import ABC
from typing import List

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import NoResultFound

from games.adapters.repository import AbstractRepository
# from games.adapters.utils import search_string
from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wishlist
from games.adapters.orm import wishlist_table


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URI  = 'sqlite:///games.db?check_same_thread=False'


# Set up the SQLAlchemy engine and session
engine = create_engine(DATABASE_URI, echo=True, pool_pre_ping=True)
session_factory = scoped_session(sessionmaker(bind=engine))

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)
        
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region Game_data
    def get_games(self) -> List[Game]:
        games = self._session_cm.session.query(Game).order_by(Game._Game__game_id).all()
        return games

    def get_game(self, game_id: int) -> Game:
        game = None
        try:
            game = self._session_cm.session.query(
                Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')

        return game

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def add_multiple_games(self, games: List[Game]):
        with self._session_cm as scm:
            for game in games:
                scm.session.merge(game)
            scm.commit()

    def get_number_of_games(self):
        total_games = self._session_cm.session.query(Game).count()
        return total_games

    # endregion

    # region Publisher data
    def get_publishers(self) -> List[Publisher]:
        publishers = self._session_cm.session.query(Publisher).all()
        return publishers

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def add_multiple_publishers(self, publishers: List[Publisher]):
        with self._session_cm as scm:
            for publisher in publishers:
                scm.session.merge(publisher)
            scm.commit()

    def get_number_of_publishers(self) -> int:
        total_publishers = self._session_cm.session.query(Publisher).count()
        return total_publishers

    # endregion

    # region Genre_data
    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def add_multiple_genres(self, genres: List[Genre]):
        with self._session_cm as scm:
            for genre in genres:
                scm.session.merge(genre)
            scm.commit()

    # endregion

    def search_games_by_title(self, title_string: str) -> List[Game]:
        games = self._session_cm.session.query(Game).filter(Game._Game__game_title.ilike(f"%{title_string}%")).all()
        return games
    
    def add_comment(self, comment: Review):
        super().add_comment(comment)
        with self._session_cm as scm:
            scm.session.add(comment)
            scm.commit()
    
    def add_user(self, user: User):
        print(f"Adding user to database: Username={user.username}, Password={user.password}")
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def get_user(self, user_name) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__username == user_name).first()
        except NoResultFound:
            print(f'User {user_name} was not found')

        return user

    def get_comments(self) -> List[Review]:
        comments = self._session_cm.session.query(Review).all()
        return comments
    
    # Wishlist
    def add_wishlist(self, wishlist):
        with self._session_cm as scm:
            scm.session.add(wishlist)
            scm.commit()

    def add_game_to_wishlist(self, user, game_id):
        with self._session_cm as scm:
            game = self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).one()
            if user and game:
                user.add_favourite_game(game)
                scm.commit()


    def remove_game_from_wishlist(self, user, game_id):
        with self._session_cm as scm:
            game = self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).one()
            print(type(user), type(game))
            if user and game:
                user.remove_favourite_game(game)
                scm.commit()


    def wishlist_exists(self, username):
        with self._session_cm as scm:
            wishlist = scm.session.query(Game).join(wishlist_table).filter(wishlist_table.c.username == username).all()
            return wishlist is not None
        
    def get_user_wishlist(self, username):
        with self._session_cm as scm:
            wishlist = scm.session.query(Game).join(wishlist_table).filter(wishlist_table.c.username == username).all()
            return wishlist


