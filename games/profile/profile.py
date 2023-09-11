from flask import Blueprint, render_template

profile_blueprint = Blueprint('profile_bp', __name__ )

@profile_blueprint.route('/profile')
def profile():

    return render_template(
        'profile.html',
    )

