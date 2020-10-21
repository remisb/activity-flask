import click
import os
from flask.cli import with_appcontext
from activity import db
from activity.model.entities import RestaurantModel

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


def init_db():
    db.drop_all()
    db.create_all()


@click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose'])
    exit(rv)


@click.command()
@with_appcontext
def create_database():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Clear existing data and create new tables.")


@click.command()
@with_appcontext
def init_database_data():
    """Initialize database with data."""
    db.create_all()

    # createtestrestaurants
    RestaurantModel(name='Restaurant 1', address="Address 1",
                    email="e1@mail.com").save()
    RestaurantModel(name='Restaurant 2', address="Address 2",
                    email="e2@mail.com").save()

    click.echo("Initialize database with data.")
