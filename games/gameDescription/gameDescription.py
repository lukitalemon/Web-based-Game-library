from flask import Blueprint
from flask import request, render_template, redirect, url_for, session, flash
from games.domainmodel.model import Wishlist

from games.gameDescription import services
from games.adapters import repository as repo

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from better_profanity import profanity
import games.gameDescription.services as services

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
    
    comments = services.get_comments_for_game( game_id,  repo.repo_instance )
    
    game = services.get_game(repo.repo_instance, game_id)

    print("Comments for Game ID:", game_id)
    for comment in game['reviews']:
            print(comment.comment)

    games = services.get_games(repo.repo_instance)

    for game in games:
        game['view_comment_url'] = url_for('gameDescription_bp.gameDescription', game_id=game['game_id'])  # Change view_comments_for to game_id
        game['add_comment_url'] = url_for('gameDescription_bp.comment_on_game', game=game['game_id'])

    form = CommentForm()
    form.game_id.data = game_id
    average_rating = services.average_rating(comments)


    return render_template(
    'gameDescription.html',
    game=game_details,
    show_comments_for_game=game_to_show_comments,
    form=form,
    games=games,
    comments = comments,
    average_rating = average_rating
    )


user_wishlists = {}

@gameDescription_blueprint.route('/add_to_wishlist/<int:game_id>', methods=['POST'])
@login_required
def add_to_wishlist(game_id):
    user = repo.repo_instance.get_user(session['user_name'])
    if user is None:
        return redirect(url_for('authentication_bp.login'))

    game = repo.repo_instance.get_game(game_id)
    if game is None:
        return redirect(url_for('home_bp.home'))

    # Add the game to the user's wishlist
    if not repo.repo_instance.wishlist_exists(user.username):
        wishlist = Wishlist(user)
        repo.repo_instance.add_wishlist(user.username, wishlist)
    repo.repo_instance.add_game_to_wishlist(user.username, game)

    return redirect(url_for('gameDescription_bp.gameDescription', game_id=game_id))

@gameDescription_blueprint.route('/remove_from_wishlist/<int:game_id>', methods=['POST'])
@login_required
def remove_from_wishlist(game_id):
    user = repo.repo_instance.get_user(session['user_name'])
    if user is None:
        return redirect(url_for('authentication_bp.login'))

    game = repo.repo_instance.get_game(game_id)
    if game is None:
        return redirect(url_for('home_bp.home'))

    # Remove the game from the user's wishlist
    repo.repo_instance.remove_game_from_wishlist(user.username, game)

    return redirect(url_for('gameDescription_bp.gameDescription', game_id=game_id))



@login_required
@gameDescription_blueprint.route('/comment', methods=['GET', 'POST'])
def comment_on_game():
    # Obtain the user name of the currently logged in user.
    username = session['user_name']

    

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        game_id = int(form.game_id.data)
        rating = int(form.rating.data)

        print("Received comment:", form.comment.data)
        print("Received rating:", rating)

        # Use the service layer to store the new comment.
        services.add_comment(game_id, form.comment.data, rating, username, repo.repo_instance)

        # Retrieve the article in dict form.
        game = services.get_game(repo.repo_instance, game_id )

        print("Comments after adding a new comment:")
        for comment in game['reviews']:
            print(comment.comment)
            print("Rating:", comment.rating)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('gameDescription_bp.gameDescription', game_id=game_id, view_comments_for=game_id))



    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        game_id = int(request.args.get('game'))

        # Store the article id in the form.
        form.game_id.data = game_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        game_id = int(form.game_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    game = services.get_game(game_id, repo.repo_instance)
    return render_template(
        'review.html',
        title='Edit article',
        game=game,
        form=form,
        handler_url=url_for('gameDescription_bp.comment_on_game')
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
    rating = IntegerField('Rating', [
        DataRequired(),
        NumberRange(min=1, max=5, message="Rating must be between 1 and 5")])
    game_id = HiddenField("Game id")
    submit = SubmitField('Submit')

