from flask import Flask
from forum.routes import rt
from forum.comments import comments
from forum.reactions import reactions
from forum.comment_reactions import comment_reactions
from forum.posts import posts
from forum.messages import messages
from forum.settings import settings
from forum.profile import profile

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    # I think more blueprints might be used to break routes up into things like
    # post_routes
    # subforum_routes
    # etc
    app.register_blueprint(posts)
    app.register_blueprint(comments)
    app.register_blueprint(reactions)
    app.register_blueprint(comment_reactions)
    app.register_blueprint(messages)
    app.register_blueprint(settings)
    app.register_blueprint(profile)
    app.register_blueprint(rt)
    # Set globals
    from forum.models import db
    db.init_app(app)
    
    with app.app_context():
        # Add some routes
        db.create_all()
        return app

