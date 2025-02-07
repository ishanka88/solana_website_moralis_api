from flask import Flask, request, jsonify, current_app, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path



# Initialize extensions
db = SQLAlchemy()
DB_NAME = "database_moralis.db"
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'isharox'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Disable to avoid overhead
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # Import models and methods only after db has been initialized to avoid circular imports
    from .modles import AvailableCoinSets, CoinTransactions, MoralisApiKey, Pairs, Gainers,BackupFolder
    create_database(app)

    # Import additional methods (these should be imported after the app and db initialization)
    from .methods import findTransactions, whalesCa, pairs, gainersMethods,coinFiles,getWhalseData,getInsidersData

    return app 

def create_database(app):
    """Create database if it doesn't exist and initialize tables."""
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()  # Creates all tables based on the models
        print('Created Database')
    else:
        print('Database already exists')

    



