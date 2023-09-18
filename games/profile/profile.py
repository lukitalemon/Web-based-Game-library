from flask import Blueprint, render_template, session, redirect, url_for
import games.adapters.repository as repo # Import MemoryRepository
from games.profile import services

profile_blueprint = Blueprint('profile_bp', __name__)

@profile_blueprint.route('/profile')
def profile():
    username = session.get('user_name')

    user_comments = services.get_comments_by_user(username, repo.repo_instance)
    # You can retrieve the user's wishlist using the MemoryRepository instance
    # Replace 'your_user_name_field' with the actual field in your User model that holds the username
    user_wishlist = repo.repo_instance.get_wishlist(session['user_name'])

    return render_template(
        'profile.html',
        wishlist=user_wishlist,  # Pass the user's wishlist to the template
        repo=repo,
        username=username,
        user_comments=user_comments
    )
