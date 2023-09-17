from flask import Blueprint, render_template, session
from games.profile import services

from games.adapters import repository as repo


profile_blueprint = Blueprint('profile_bp', __name__ )

@profile_blueprint.route('/profile')
def profile():
    # Retrieve the currently logged-in user's username from the session.
    username = session.get('user_name')

    # Retrieve the user's comments based on their username.
    user_comments = services.get_comments_by_user(username, repo.repo_instance)

    return render_template('profile.html', username=username, user_comments=user_comments)

