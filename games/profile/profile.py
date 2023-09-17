from flask import Blueprint, render_template, session
from games.adapters import repository as repo  # Import your repository

profile_blueprint = Blueprint('profile_bp', __name__)

@profile_blueprint.route('/profile')
def profile():
    # Get the current user's wishlist (if it exists)
    wishlist = None
    if repo.repo_instance.wishlist_exists(session['user_name']):
        wishlist = repo.repo_instance.get_wishlist(session['user_name']).list_of_games()

    return render_template('profile.html', wishlist=wishlist, repo=repo)  # Pass repo to the template
