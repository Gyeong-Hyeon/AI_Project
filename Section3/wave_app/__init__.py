from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uymuxtctbleqxc:057bc69da7f9c6aab52817d60e206488bc945468bd6b3d244da795ae961ca18b@ec2-18-206-20-102.compute-1.amazonaws.com:5432/d3s6vepe1fhqcb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from wave_app.routes import (main_route, predict_route, signin_route, signup_route)
    app.register_blueprint(main_route.bp)
    app.register_blueprint(predict_route.bp)
    app.register_blueprint(signin_route.bp)
    app.register_blueprint(signup_route.bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)