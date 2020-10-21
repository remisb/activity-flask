import click
from activity import db
from activity.model.entities import RestaurantModel
from flask.cli import with_appcontext


def init_app(app):
    @app.cli.command("create_database")
    @with_appcontext
    def create_database():
        """Clear existing data and create new tables."""
        init_db()
        click.echo("Initialized the database.")


def init_db():
    db.drop_all()
    db.create_all()


def init_database_data():
    db.create_all()

    # createtestrestaurants
    RestaurantModel(name='Restaurant 1', address="Address 1",
                    email="e1@mail.com").save()
    RestaurantModel(name='Restaurant 2', address="Address 2",
                    email="e2@mail.com").save()
