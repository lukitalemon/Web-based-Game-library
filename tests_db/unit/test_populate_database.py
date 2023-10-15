from sqlalchemy import select, inspect
from tests_db.conftest import database_engine
from games.adapters.orm import metadata

    def test_database_populate_inspect_table_names(database_engine):
        # Get table information
        inspector = inspect(database_engine)
        assert inspector.get_table_names() == ['games', 'games_genres', 'genres', 'publishers', 'reviews','users', 'wishlists' ]

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['username'])

        assert all_users == ['ethan', 'luke']

