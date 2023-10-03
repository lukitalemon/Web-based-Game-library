"""Initialize Flask app."""

from pathlib import Path
from flask import Flask, render_template, request, url_for, redirect

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from games.domainmodel.model import Game
from games.browse import browse

# local imports
import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.adapters.repository_populate import populate
from games.adapters.orm import metadata, map_model_to_tables


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    database_uri = 'sqlite:///games.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging

    # Create a database engine and connect it to the specified database
    database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                    echo=False)

    # Create the database session factory using session-maker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo.repo_instance = SqlAlchemyRepository(session_factory)
    data_path = Path('games') / 'adapters' / 'data'

    if len(inspect(database_engine).get_table_names()) == 0:
        print("REPOPULATING DATABASE...")
        # For testing, or first-time use of the web application, reinitialise the database.
        clear_mappers()
        # Conditionally create database tables.
        metadata.create_all(database_engine)
        # Remove any data from the tables.
        for table in reversed(metadata.sorted_tables):
            with database_engine.connect() as conn:
                conn.execute(table.delete())

        # Generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

        populate(data_path, repo.repo_instance)
        print("REPOPULATING DATABASE... FINISHED")

    else:
        # Solely generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

    with app.app_context():

        from .home import home 
        app.register_blueprint(home.home_blueprint)

        from games.authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from games.browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from games.gameDescription import gameDescription
        app.register_blueprint(gameDescription.gameDescription_blueprint)

        from games.profile import profile
        app.register_blueprint(profile.profile_blueprint)

    return app
