import click

from mathsrace.db import init_db


def init_db_command():
    init_db()
    click.echo('Initialized the database.')
