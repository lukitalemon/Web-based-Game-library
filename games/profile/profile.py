from flask import Blueprint, render_template, session, redirect, url_for
#import games.adapters.repository as repo # Import MemoryRepository
from games.adapters import database_repository as repo
from games.profile import services
from games.authentication.authentication import login_required


profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/profile')
@login_required
def profile():
    username = session.get('user_name')
    repository = repo.SqlAlchemyRepository(repo.session_factory)


    user = repository.get_user(session['user_name'])
    if user is None:
        return redirect(url_for('authentication_bp.login'))

    user_comments = services.get_comments_by_user(username,repository)
    # You can retrieve the user's wishlist using the MemoryRepository instance
    # Replace 'your_user_name_field' with the actual field in your User model that holds the username
    user_wishlist = repository.get_user_wishlist(session['user_name'])

    return render_template(
        'profile.html',
        wishlist=user_wishlist,  # Pass the user's wishlist to the template
        repository=repository,
        username=username,
        user_comments=user_comments

    )
