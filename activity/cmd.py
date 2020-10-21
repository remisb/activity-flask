from flask.cli import with_appcontext
from activity import db


def register_commands(app):
    """Register Click commands."""

    import click
    from activity.commands import create_database, init_db
    from activity.cli import init_app

    # init_app(app)
    print('App:', app)

    @app.cli.command("create-user")
    @click.argument("name")
    def create_user(name):
        """Creates new user"""
        print("Command create-user is running...with name:", name)

    @app.cli.command("seed-users")
    @with_appcontext
    def create_users():
        """Seed users"""

        from activity.model.entities import UserModel
        UserModel(username="User1", email="u1@mail.com",
                  password="pass1234").save()

        print("Database seeded with user data")

    @app.cli.command("seed-restaurants")
    @with_appcontext
    def seed_restaurants():
        """Seed restaurants"""

        from activity.model.entities import RestaurantModel
        from activity.db import create_all
        print("Command seed-restaurants is running...")

        create_all()

        # createtestrestaurants
        RestaurantModel(name='Restaurant 1', address="Address 1",
                        email="e1@mail.com").save()
        RestaurantModel(name='Restaurant 2', address="Address 2",
                        email="e2@mail.com").save()

        click.echo("Initialize database with data.")
