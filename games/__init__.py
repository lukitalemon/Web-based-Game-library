"""Initialize Flask app."""

from flask import Flask, render_template
from pathlib import Path
import games.adapters.repository as repo 
from games.adapters.memory_repository import populate, MemoryRepository



def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    app.config.from_object('config.Config')

    data_path = Path('games') / 'adapters' / 'data' / 'games.csv'

    #create the MemoryRepository implementation for a memory-based repository
    repo.repo_instance = MemoryRepository()

    #fill the repository from the CSV file
    populate(data_path, repo.repo_instance)

    with app.app_context():

        from .home import home 
        app.register_blueprint(home.home_blueprint)

        from games.browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from games.gameDescription import gameDescription
        app.register_blueprint(gameDescription.gameDescription_blueprint)

        from games.profile import profile
        app.register_blueprint(profile.profile_blueprint)

        from games.authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)
    
    
    return app
