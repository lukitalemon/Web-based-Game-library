# services.py

from games.domainmodel.model import Review

def get_comments_by_user(username, repo):
    """
    Retrieve comments made by a specific user.

    :param username: The username of the user whose comments you want to retrieve.
    :param repo: The repository instance.
    :return: A list of Comment objects made by the user.
    """
    user_comments = []

    # Iterate through all comments in the repository.
    for comment in repo.get_comments():
        # Check if the comment was made by the specified user.
        if comment.user.username == username:
            user_comments.append(comment)

    return user_comments
