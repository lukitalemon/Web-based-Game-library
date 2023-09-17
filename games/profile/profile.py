from flask import Blueprint, render_template, session
from games.profile import services

from games.adapters import repository as repo

from games.adapters import repository as repo  # Import your repository

profile_blueprint = Blueprint('profile_bp', __name__)

@profile_blueprint.route('/profile')
def profile():

    return render_template(
        'profile.html',
    )

