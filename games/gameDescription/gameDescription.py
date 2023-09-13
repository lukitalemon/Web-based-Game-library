from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from games.gameDescription import services
from games.adapters import repository as repo

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from better_profanity import profanity

from games.authentication.authentication import login_required

gameDescription_blueprint = Blueprint('gameDescription_bp', __name__)

@gameDescription_blueprint.route('/GameDescription/<int:game_id>', methods=['GET', 'POST'])
def gameDescription(game_id):
    game_details = services.get_game(repo.repo_instance, game_id)

    game_to_show_comments = request.args.get('view_comments_for')

    if game_to_show_comments is None:
        game_to_show_comments = -1
    else:
        game_to_show_comments = int(game_to_show_comments)

    if game_details is None:
        # Handle the case where the game is not found
        return render_template('game_not_found.html')
    
    form = CommentForm()

    return render_template(
        'gameDescription.html',
        game=game_details,
        form = form,
        show_comments_for_game=game_to_show_comments
    )


@gameDescription_blueprint.route('/comment', methods=['GET', 'POST'])
def review():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']

    # Create form. The form maintains state, e.g., when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e., the comment text has passed data validation.
        # Extract the game_id, representing the commented game, from the form.
        game_id = int(form.game_id.data)

        # Use the service layer to store the new comment.
        services.add_comment(game_id, form.comment.data, user_name, repo.repo_instance)

        # Retrieve the game in dict form.
        game = services.get_game(game_id, repo.repo_instance)

        # Retrieve the comments for the game.
        comments = services.get_comments_for_game(game_id, repo.repo_instance)

        # Cause the web browser to display the page of the commented game and display all comments, including the new comment.
        return redirect(url_for('gameDescription_bp.review', game=game_id,view_comments_for=game_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the game_id, representing the game to comment, from a query parameter of the GET request.
        game_id = int(request.args.get('game'))

        # Store the game_id in the form.
        form.game_id.data = game_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the game_id of the game being commented from the form.
        game_id = int(form.game_id.data)

    # For a GET or an unsuccessful POST, retrieve the game to comment in dict form and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    game = services.get_game(game_id, repo.repo_instance)

    return render_template(
        'review.html',
        game=game,
        form=form,
        handler_url=url_for('gameDescription_bp.review'),
        game_id=game_id,
        comments=comments  # Add comments to the template context
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    game_id = HiddenField("Game id")
    submit = SubmitField('Submit')

