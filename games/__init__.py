"""Initialize Flask app."""

from flask import Flask, render_template
from pathlib import Path
import games.adapters.memory_repository as repo 
from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository 



# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from games.domainmodel.model import Game


# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
def create_some_game():
    some_game = Game(1, "Call of Duty® 4: Modern Warfare®")
    some_game.release_date = "Nov 12, 2007"
    some_game.price = 9.99
    some_game.description = "The new action-thriller from the award-winning team at Infinity Ward, the creators of " \
                            "the Call of Duty® series, delivers the most intense and cinematic action experience ever. "
    some_game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    return some_game


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    data_path = Path('games') / 'adapters' / 'data' / 'games.csv'
    # #create the MemoryRepository implementation for a memory-based repository
    repo.repo_instance = MemoryRepository()
    # #fill the repository from the CSV file
    populate(data_path, repo.repo_instance)

    with app.app_context():
        from games.browse import browse_page
        app.register_blueprint(browse_page.browse_blueprint)

    # @app.route('/gameDesc')
    # def show_gameDescription():
    #     some_game = create_some_game()
    #     # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    #     return render_template('gameDescription.html', game=some_game)
    
    # @app.route('/')
    # def home():
    #     return render_template('home.html')
    
    # @app.route('/browse')
    # def browse():
    #     return render_template('browse.html')
    
    return app
