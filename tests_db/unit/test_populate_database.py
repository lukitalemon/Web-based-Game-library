from sqlalchemy import select, inspect
from tests_db.conftest import database_engine
from games.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['publishers', 'games', 'genres', 'users', 'reviews','games_genres', 'wishlists' ]
